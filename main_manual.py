from tetris import *
import random
from tkinter import *
from tensorflow import keras
from tensorflow import set_random_seed
import numpy as np


root = Tk()
root.title("Tetris")

frame = Frame(root, width=1000, height=1000)
canvas = Canvas(frame, width=400, height=600)
canvas.pack()
frame.pack()

tetris = Tetris(canvas)
# Keyboard Input

def key(event):
    print("pressed", event.keysym)
    tetris.input_c(event.keysym)
    tetris.render()


# Create frame for organizational reasons

# Callback
root.bind("<KeyPress>", key)


# thebiggay = "h, dasr, l, hd, hd, dasl, hd, cw, dasr, hd"
#tetris.run_commands(thebiggay)
# Main Loop


tetris.input_log = ['l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'hd', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'hd', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'hd', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', '180', 'hd', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'hd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'hd', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'hd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'hd', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'hd', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'hd', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'hd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'sd', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'dasr', 'hd', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'hd']

def loop():
    tetris.replay()
    root.after(50, loop)


root.after(1, loop)
root.mainloop()

root.mainloop()

