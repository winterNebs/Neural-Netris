from tetris import *
import random
from tkinter import *
from tensorflow import keras
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

    def __init__(self, name, c):
        self.number_node = 17
        self.name = str(name)
        set_random_seed(Network.seed)
        np.random.seed(Network.seed)
        Network.seed += 100
        #keras.initializers.RandomNormal(mean=0.5, stddev=0.5, seed=5)
        self.inputs = keras.Input(shape=(23,))
        self.x = keras.layers.Dense(self.number_node, kernel_initializer='random_uniform', bias_initializer='zero',
                                    activation='linear')(self.inputs)
        #self.x = keras.layers.Dropout(0.2)(self.x)
        self.outputs = keras.layers.Dense(1, activation='linear')(self.x)

        self.model = keras.models.Model(inputs=self.inputs, outputs=self.outputs)
        self.model.compile(optimizer='rmsprop',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])
        self.tetris = Tetris(c)
        self.set_weight()
        self.previous_command = 'poopy'
        self.amount = 0
        self.previous_piece = 'i'

    def lose_weight(self):
        np.set_printoptions(threshold=np.nan)
        #print(self.model.input)
        #print(len(self.model.layers))
        file = open("weights1.txt", "w")
        for layer in self.model.layers:
            file.write("----Next Layer----\n")
            if len(layer.get_weights()) > 0:
                for array in layer.get_weights():
                    file.write("----Next Weight----\n")
                    file.write(np.array2string(array))
            # print(layer)
            '''weights = np.ndarray(shape=(64, 64))
            for i in range(64):
                for j in range(64):
                    weights[i][j] = random.random'''

    def set_weight(self):
        '''
        0: 0 (none)
        1: [23x64, 64]
        2: [23x64, 64]
        3: [64x10, 10]
        '''
        bias = 1
        for i in range(1, len(self.model.layers)):
            #biases = np.ndarray(shape=(self.number_node,))
            biases = np.random.uniform(low=-bias, high=bias, size=(self.number_node,))
            if i == 1:
                weights = np.random.rand(23, self.number_node)
                #weights.fill(0.1)
                #for w in range(len(weights[22])):
                    #weights[22][w] = .95
            elif i == 2:
                weights = np.random.rand(self.number_node, 1)
                #biases = np.ndarray(shape=(10,))
                biases = np.random.uniform(low=-bias, high=bias, size=(1,))
                #biases.fill(0)
            if i is not 3333:
                self.model.layers[i].set_weights([weights, biases])

    def ANN(self):
        if self.tetris.active:
            test_input_data = self.tetris.output_data()
            # print(test_input_data)
            output_data = self.model.predict(test_input_data, 1)
            #print(output_data, "hi")
            data = output_data.flatten()
            index = np.argmax(data)
            if self.previous_command != highest[index]:
                self.previous_command = highest[index]
                self.amount = 0
            else:
                self.amount += 1
            if self.amount > 24:
                self.tetris.run_commands('hd')
                self.amount = 0
            else:
                self.tetris.run_commands(highest[index])
            #self.lose_weight()
            if self.previous_piece != self.tetris.current_piece.shapeName:
                self.amount = 0
                self.previous_piece = self.tetris.current_piece.shapeName
            #print(self.previous_command)
            # print(input_log)


# Create Root Window

root = Tk()
root.title("Tetris")


# Keyboard Input

def key(event):
    print("pressed", event.keysym)
    # tetris.input_c(event.keysym)
    # tetris.render()


# Create frame for organizational reasons
frame = Frame(root, width=1000, height=1000)


# Callback
root.bind("<KeyPress>", key)

ais = []
canvases = []
for i in range(50):
    if i < 5:
        canvases.append(Canvas(frame, width=400, height=600))
        canvases[i].pack(side=LEFT)
        ais.append(Network(i, canvases[i]))
    ais.append(Network(i, None))

frame.pack()
# thebiggay = "h, dasr, l, hd, hd, dasl, hd, cw, dasr, hd"
#tetris.run_commands(thebiggay)
# Main Loop
dead_ais = []

def loop():
    out = ""
    for ai in ais:
        if not ai.tetris.active:
            print("---------------------AI #" + ai.name + " DIED---------------------")
            print(ai.tetris.input_log)
            dead_ais.append(ai)
            ais.remove(ai)
        ai.ANN()
        out += "(AI #" + ai.name
        out += " P:" + str(ai.tetris.total_pieces)
        out += " M:" + str(ai.tetris.total_moves)
        out += " C:" + str(ai.tetris.total_cleared) + ") "
    print(out)
    if len(ais) > 0:
        root.after(0, loop)
    else:
        gaussian_cull()
        root.after(0, loop)


def gaussian_cull():  # Fitness Evaluation (based on #moves for now)
    print("++++++++++++++++++++++++NEW GEN++++++++++++++++++++++++")
    for i in range(int(len(dead_ais)/2)):
        dead_ais.pop(0)
    for ai in dead_ais:
        print("+++++SAVED " + ai.name + "+++++")
        ai.model.save(ai.name + "model.h5")
    for i in range(len(dead_ais) * 2):
        rand1 = np.random.randint(0, len(dead_ais))
        rand2 = np.random.randint(0, len(dead_ais))
        print("=+=Mating " + dead_ais[rand1].name + "&" + dead_ais[rand2].name + "=+=")
        ais.append(cross_over(dead_ais[rand1], dead_ais[rand2]))
    dead_ais.clear()

def cross_over(ai1, ai2):  # 1 Point Splice + Mutation
    ai1_weights = []
    ai2_weights = []
    baby = []
    for i in range(1, len(ai1.model.layers)):
        ai1_weights.append(ai1.model.layers[i].get_weights())
    for i in range(1, len(ai2.model.layers)):
        ai2_weights.append(ai2.model.layers[i].get_weights())
        baby.append([])
    for i in range(0, len(ai1_weights)):
        for j in range(0, len(ai1_weights[i])):
            rand_splice = np.random.randint(low=0, high=len(ai1_weights))
            baby[i].append(np.concatenate((ai1_weights[i][j][:rand_splice], ai2_weights[i][j][rand_splice:]),axis=0))
    for k in range(np.random.randint(0, 10)):
        layer = np.random.randint(low=0, high=len(baby))
        wb = np.random.randint(low=0, high=2)
        jeans = np.random.randint(low=0, high=len(baby[layer][wb]))
        baby[layer][wb][jeans] = np.random.randint(-2, 2)
    new_ai = Network(ai1.name + "." + ai2.name, None)
    for i in range(0, len(baby)):
        new_ai.model.layers[i+1].set_weights([baby[i][0], baby[i][1]])
    return new_ai


root.after(1, loop)
root.mainloop()

