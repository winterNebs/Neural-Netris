from tetris import *
import math
import os
#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from multiprocessing.dummy import Pool as ThreadPool
import threading
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

    def __init__(self, name, c=None, file=None, weights=None):
        self.number_node = 22
        self.name = str(name)
        self.fitness = 0
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
        self.fitness = self.tetris.total_pieces

    def save(self):
        with self.graph.as_default():
            with self.sess.as_default():
                self.model.save("ais/" + self.name + ".h5", overwrite=True, include_optimizer=False)
                print("+++++SAVED " + self.name + "+++++\t" + str(self.fitness))


# Keyboard Input
def key(event):
    print("pressed", event.keysym)
    # tetris.input_c(event.keysym)
    # tetris.render()

ais = []
canvases = []
population = 100

# Main Loop
generation = 0
dead_ais = []
thread_lock = threading.Lock()
num_ais = 0
last_avg = 0
staleness = 0
fit_total = 0

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
    global generation, dead_ais, ais
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
        pool = ThreadPool(8)  # or 1?
        pool.map(check_ai, ais)

        pool.map(run_ai, ais)

        pool.close()
        pool.join()
        #print(console_output)
        if len(ais) == 0:
            generation += 1
            gaussian_cull()
        #root.after(0, loop)


def run_ai(ai):
    global console_output
    ai.ANN()
    #console_output += "(AI #" + ai.name
    #console_output += " P:" + str(ai.tetris.total_pieces)
    #console_output += " M:" + str(ai.tetris.total_moves)
    #console_output += " C:" + str(ai.tetris.total_cleared) + ") "


def check_ai(ai):
    if not ai.tetris.active:
        ai.calc_fitness()
        print("---------------------AI #" + ai.name + " DIED---------------------")
        print("------Fitness is " + str(ai.fitness) + "------")
        print("(AI #" + ai.name, " P:" + str(ai.tetris.total_pieces),
              " M:" + str(ai.tetris.total_moves),
              " C:" + str(ai.tetris.total_cleared) + ") ")
        print(ai.tetris.input_log)
        dead_ais.append(ai)
        ais.remove(ai)
        #ai.save()


def gaussian_cull():  # Fitness Evaluation (based on #moves for now)
    global dead_ais, ais, population, num_ais, fit_total, staleness, last_avg
    print("++++++++++++++++++++++++NEW GEN (" + str(generation) + ") staleness: " + str(staleness) + "++++++++++++++++++++++++")
    num_ais = 0
    pool = ThreadPool(8)  # or 1?
    print(len(dead_ais))
    if len(dead_ais) >= population:
        dead_ais.sort(key=lambda x: x.fitness, reverse=False)
        survivers = []
        for i in range(population):
            if np.random.normal(loc=int(population*0.65), scale=int(population/20)) < i:
                survivers.append(dead_ais[i])
        for ai in survivers:
            ai.save()
            fit_total += ai.fitness
        staleness = abs(fit_total / len(survivers) - last_avg)
        last_avg = fit_total / len(survivers)
        fit_total = 0
        dead_ais = survivers
    #pool.map(single_mom, range(population))
    pool.map(single_mom, range(population))
    dead_ais = []
    pool.close()
    pool.join()

def jizzmoid(x):
  return math.exp(-(x**2))

def single_mom(_):  # 1 Point Splice + Mutation
    global dead_ais, ais, num_ais, staleness
    randomizer = 200 * jizzmoid(staleness) + 50
    ai = dead_ais[np.random.randint(0, len(dead_ais))]
    ai_weights = ai.weights
    for k in range(np.random.randint(0, randomizer)):
        layer = np.random.randint(low=0, high=len(ai_weights))
        wb = np.random.randint(low=0, high=2)
        jeans = np.random.randint(low=0, high=len(ai_weights[layer][wb]))
        rand_num = np.random.uniform(low=-5, high=5)
        if wb == 0:
            wtf = np.random.randint(low=0, high=len(ai_weights[layer][wb][jeans]))
            ai_weights[layer][wb][jeans][wtf] += rand_num
        elif wb == 1:
            ai_weights[layer][wb][jeans] += rand_num

    with thread_lock:
        ais.append(Network(str(generation) + "." + str(num_ais), weights=ai_weights))
        num_ais += 1
    print("=+=" + ai.name + " is lonely on a monday night=+=")


def cross_over(_):  # 1 Point Splice + Mutation
    global dead_ais, ais
    ai1 = dead_ais[np.random.randint(0, len(dead_ais))]
    ai2 = dead_ais[np.random.randint(0, len(dead_ais))]
    ai1_weights = ai1.weights
    ai2_weights = ai2.weights
    baby = []
    for i in range(1, len(ai2.model.layers)):
        baby.append([])
    for layer in range(0, len(ai1_weights)):
        for wb in range(0, len(ai1_weights[layer])):
            rand_splice = np.random.randint(low=0, high=len(ai1_weights))
            baby[layer].append(np.concatenate((
                ai1_weights[layer][wb][:rand_splice], ai2_weights[layer][wb][rand_splice:]), axis=0))
    for k in range(np.random.randint(0, 100)):
        layer = np.random.randint(low=0, high=len(baby))
        wb = np.random.randint(low=0, high=2)
        jeans = np.random.randint(low=0, high=len(baby[layer][wb]))
        baby[layer][wb][jeans] = np.random.uniform(low=-2, high=2)
        print(baby[layer][wb][jeans])
    ais.append(Network(str(generation) + "." + str(len(ais)), weights=baby))
    print("=+=Mating " + ai1.name + "&" + ai2.name + "=+=")


if __name__ == '__main__':
    # Create Root Window
    # root = Tk()
    # root.title("Tetris")

    # Create frame for organizational reasons
    # frame = Frame(root, width=1000, height=1000)
    # Callback
    # root.bind("<KeyPress>", key)

    # frame.pack()
    # tetris.run_commands(thebiggay)

    # root.after(1, loop)
    # root.mainloop()

    loop()
