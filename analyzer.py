from main import Network
import matplotlib.pyplot as plt
import numpy as np
import os
from multiprocessing.dummy import Pool as ThreadPool
from tensorflow.keras.utils import plot_model

ais = []
generation = 0


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
                ais.append(Network(file.split(".")[0] + "." + file.split(".")[1], file="ais/" + file))
        generation += 1


def output(ai):
    fig = plt.figure()
    counter = 1
    for layer in ai.weights:
        for i, wb in enumerate(layer):
            #if i == 1:
            #    plt.hist(np.array(wb).flatten())
            #    plt.subplot(3, 2, counter)
            #   counter += 1
            #else:
            if i != 1:
                fixed = np.array(wb, dtype=float)
                plt.imshow(fixed)
                plt.subplot(3, 1, counter)
                counter += 1
    fig.savefig('ais/weights/'+ai.name+'.png')
    fig.clf()
    plt.close(fig)
    #plot_model(ai.model, to_file="weights/" + ai.name + ".png", show_shapes=True)
    #file = open("weights/" + ai.name + ".txt", "w+")
    #file.write(str(ai.weights))
    #file.close()


def analyze():
    load()
    for ai in ais:
        output(ai)


analyze()
