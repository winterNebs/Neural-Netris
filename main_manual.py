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
    #tetris.input_c(event.keysym)
    #tetris.render()


# Create frame for organizational reasons

# Callback
root.bind("<KeyPress>", key)


# thebiggay = "h, dasr, l, hd, hd, dasl, hd, cw, dasr, hd"
#tetris.run_commands(thebiggay)
# Main Loop


tetris.input_log = ['h', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd', 'dasl', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'hd', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd', 'dasl', 'cw', 'cw', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'hd', 'dasl', 'cw', 'cw', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'hd', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd', 'dasl', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'cw', 'hd', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd', 'dasl', 'cw', 'cw', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'hd', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'dasl', 'hd']

def loop():
    tetris.replay()
    root.after(50, loop)


root.after(1, loop)
root.mainloop()

root.mainloop()

