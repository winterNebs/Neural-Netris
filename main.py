from tetris import *
import math
import os
#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
import random
from tkinter import *
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as k
from tensorflow import set_random_seed
import numpy as np
import h5py

highest = {
    0: 'hd',
    1: '180',
    2: 'l',
    3: 'dasr',
    4: 'sd',
    5: 'h',
    6: 'ccw',
    7: 'dasl',
    8: 'cw',
    9: 'r',
}

class Network:
    seed = 2
    np.random.seed(0)

    def __init__(self, name, c=None, file=None, weights=None):
        self.number_node = 22
        self.name = str(name)
        self.fitness = 0
        set_random_seed(Network.seed)
        np.random.seed(Network.seed)
        Network.seed += 100
        self.graph = tf.Graph()
        self.weights = []
        with self.graph.as_default():
            self.sess = tf.Session()
            with self.sess.as_default():
                if file is None:
                    inputs = keras.Input(shape=(23,))
                    x = keras.layers.Dense(self.number_node, kernel_initializer='random_uniform', bias_initializer='zero',
                                                activation='linear')(inputs)
                    x = keras.layers.Dense(self.number_node, kernel_initializer='random_uniform', bias_initializer='zero',
                                                activation='relu')(x)
                    outputs = keras.layers.Dense(1, activation='linear')(x)

                    self.model = keras.models.Model(inputs=inputs, outputs=outputs)
                else:
                    self.model = keras.models.load_model(file)
                self.init = tf.global_variables_initializer()
                if weights is not None:
                    for i in range(0, len(weights)):
                        self.model.layers[i + 1].set_weights([weights[i][0], weights[i][1]])
                    self.weights = weights
                else:
                    for i in range(1, len(self.model.layers)):
                        self.weights.append(self.model.layers[i].get_weights())

        self.tetris = Tetris(c)
        self.pieces = 0
        self.amount = 0

    def ANN(self):
        if self.tetris.active:
            test_input_data = self.tetris.output_data()
            # print(test_input_data)
            with self.graph.as_default():
                with self.sess.as_default():
                    output_data = self.model.predict(test_input_data, 1)
            # print(output_data, "hi")
            data = output_data.flatten()
            index = np.argmax(data)
            if self.pieces != self.tetris.total_pieces:
                self.pieces = self.tetris.total_pieces
                self.amount = 0
            else:
                self.amount += 1
            if self.amount > 30:
                self.tetris.run_commands('hd')
            else:
                self.tetris.run_commands(highest[index])

    def calc_fitness(self):
        self.fitness = (100*(math.exp(-((self.tetris.total_pieces - 100) / 30) ** 2))) + \
                       (-math.exp((-self.tetris.total_cleared+37)/8)+100) + \
                        50/(1+math.exp(2*((self.tetris.total_moves/self.tetris.total_pieces)-4.4))) - 25
        return self.fitness

    def save(self):
        with self.graph.as_default():
            with self.sess.as_default():
                self.model.save("ais/" + self.name + ".h5", overwrite=True, include_optimizer=False)
                print("+++++SAVED " + self.name + "+++++\t" + str(self.fitness))

# Create Root Window
#root = Tk()
#root.title("Tetris")
# Keyboard Input
def key(event):
    print("pressed", event.keysym)
    # tetris.input_c(event.keysym)
    # tetris.render()
# Create frame for organizational reasons
#frame = Frame(root, width=1000, height=1000)
# Callback
#root.bind("<KeyPress>", key)


ais = []
canvases = []
population = 100

#frame.pack()
#tetris.run_commands(thebiggay)

# Main Loop
generation = 0
dead_ais = []


def load():
    global generation
    files = sorted(os.listdir("ais/"))
    if len(files) > 0:
        for file in files:
            filegen = int(file.split(".")[0])
            if generation < filegen:
                generation = filegen
        for file in files:
            filegen = int(file.split(".")[0])
            if generation == filegen:
                dead_ais.append(Network(file.split(".")[0] + "." + file.split(".")[1], file="ais/" + file))
        generation += 1

console_output = ""

def loop():
    global generation, dead_ais, ais, console_output
    generation = 0
    load()
    if generation == 0:
        for i in range(population):
            # if i < 5:
            # canvases.append(Canvas(frame, width=400, height=600))
            # canvases[i].pack(side=LEFT)
            # ais.append(Network(i, canvases[i]))
            # else:
            # ais.append(Network(i, None))
            ais.append(Network("0." + str(i), None))
    else:
        gaussian_cull()

    while True:
        console_output = ""
        pool = ThreadPool(4)  # or 1?
        pool.map(check_ai, ais)

        pool.map(run_ai, ais)

        pool.close()
        pool.join()
        print(console_output)
        if len(ais) == 0:
            generation += 1
            gaussian_cull()
        #root.after(0, loop)


def run_ai(ai):
    global console_output
    ai.ANN()
    console_output += "(AI #" + ai.name
    console_output += " P:" + str(ai.tetris.total_pieces)
    console_output += " M:" + str(ai.tetris.total_moves)
    console_output += " C:" + str(ai.tetris.total_cleared) + ") "


def check_ai(ai):
    if not ai.tetris.active:
        ai.calc_fitness()
        print("---------------------AI #" + ai.name + " DIED---------------------")
        print("------Fitness is " + str(ai.fitness) + "------")
        print(ai.tetris.input_log)
        dead_ais.append(ai)
        ais.remove(ai)


def gaussian_cull():  # Fitness Evaluation (based on #moves for now)
    print("++++++++++++++++++++++++NEW GEN (" + str(generation) + ")++++++++++++++++++++++++")
    global dead_ais, ais, population

    setattr(tf.contrib.rnn.GRUCell, '__deepcopy__', lambda self, _: self)
    setattr(tf.contrib.rnn.BasicLSTMCell, '__deepcopy__', lambda self, _: self)
    setattr(tf.contrib.rnn.MultiRNNCell, '__deepcopy__', lambda self, _: self)
    pool = ThreadPool(4)  # or 1?
    print(len(dead_ais))
    if len(dead_ais) >= population:
        dead_ais.sort(key=lambda x: x.fitness, reverse=False)
        for i in range(population-5):
            if np.random.normal(loc=int(population/2), scale=int(population/5)) > i+1:
                dead_ais.pop(0)
        for ai in dead_ais:
            ai.save()
    '''for i in range(population):
        rand1 = np.random.randint(0, len(dead_ais))
        #rand2 = np.random.randint(0, len(dead_ais))
        #print("=+=Mating " + dead_ais[rand1].name + "&" + dead_ais[rand2].name + "=+=")
        #ais.append(cross_over(dead_ais[rand1], dead_ais[rand2]))
        ais.append(single_mom(dead_ais[rand1]))'''

    pool.map(single_mom, range(population))
    dead_ais = []
    pool.close()
    pool.join()


def single_mom(_):  # 1 Point Splice + Mutation
    global dead_ais
    ai = dead_ais[np.random.randint(0, len(dead_ais))]
    ai_weights = ai.weights
    for k in range(np.random.randint(0, 50)):
        layer = np.random.randint(low=0, high=len(ai_weights))
        wb = np.random.randint(low=0, high=2)
        jeans = np.random.randint(low=0, high=len(ai_weights[layer][wb]))
        ai_weights[layer][wb][jeans] = np.random.randint(-1, 1)
    ais.append(Network(str(generation) + "." + str(len(ais)), weights=ai_weights))
    print("=+=" + ai.name + " is lonely on a monday night=+=")


def cross_over(ai1, ai2):  # 1 Point Splice + Mutation
    ai1_weights = []
    ai2_weights = []
    baby = []
    for i in range(1, len(ai1.model.layers)):
        ai1_weights.append(ai1.model.layers[i].get_weights())
    for i in range(1, len(ai2.model.layers)):
        ai2_weights.append(ai2.model.layers[i].get_weights())
        baby.append([])
    for layer in range(0, len(ai1_weights)):
        for wb in range(0, len(ai1_weights[layer])):
            rand_splice = []
            rand_splice.append(np.random.randint(low=0, high=len(ai1_weights)))
            rand_splice.append(np.random.randint(low=rand_splice[0], high=len(ai1_weights)))
            rand_splice.append(np.random.randint(low=rand_splice[1], high=len(ai1_weights)))

            baby[layer].append(np.concatenate((
                ai1_weights[layer][wb][:rand_splice[0]], ai2_weights[layer][wb][rand_splice[0]:rand_splice[1]],
                ai1_weights[layer][wb][rand_splice[1]:rand_splice[2]], ai2_weights[layer][wb][rand_splice[2]:]
            ), axis=0))
    for k in range(np.random.randint(0, 50)):
        layer = np.random.randint(low=0, high=len(baby))
        wb = np.random.randint(low=0, high=2)
        jeans = np.random.randint(low=0, high=len(baby[layer][wb]))
        baby[layer][wb][jeans] = np.random.randint(-1, 1)
    new_ai = Network(str(generation) + "." + str(len(ais)), None)
    for i in range(0, len(baby)):
        new_ai.model.layers[i+1].set_weights([baby[i][0], baby[i][1]])
    return new_ai


#root.after(1, loop)
#root.mainloop()

loop()
