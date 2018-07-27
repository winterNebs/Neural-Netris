import random
import copy
import numpy as np
import time


def v_height():
    return 20


def height():
    return 22


def width():
    return 10


def pieces():
    return ['i', 'o', 't', 's', 'z', 'j', 'l']


def size():
    return 21


class Point:
    def __init__(self, x_pos=0, y_pos=0):
        self.x = x_pos
        self.y = y_pos

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


class Tetromino:
    shapes = {
        'n': [[]],
        'i': [[[0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 1, 1, 1, 1],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]],
              [[0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 1, 0, 0]],
              [[0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [1, 1, 1, 1, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]],
              [[0, 1, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0]]],
        'o': [[[0, 1, 1],
               [0, 1, 1],
               [0, 0, 0]],
              [[0, 0, 0],
               [0, 1, 1],
               [0, 1, 1]],
              [[0, 0, 0],
               [1, 1, 0],
               [1, 1, 0]],
              [[1, 1, 0],
               [1, 1, 0],
               [0, 0, 0]]],
        't': [[[0, 1, 0],
               [1, 1, 1],
               [0, 0, 0]],
              [[0, 1, 0],
               [0, 1, 1],
               [0, 1, 0]],
              [[0, 0, 0],
               [1, 1, 1],
               [0, 1, 0]],
              [[0, 1, 0],
               [1, 1, 0],
               [0, 1, 0]]],
        's': [[[0, 1, 1],
               [1, 1, 0],
               [0, 0, 0]],
              [[0, 1, 0],
               [0, 1, 1],
               [0, 0, 1]],
              [[0, 0, 0],
               [0, 1, 1],
               [1, 1, 0]],
              [[1, 0, 0],
               [1, 1, 0],
               [0, 1, 0]]],
        'z': [[[1, 1, 0],
               [0, 1, 1],
               [0, 0, 0]],
              [[0, 0, 1],
               [0, 1, 1],
               [0, 1, 0]],
              [[0, 0, 0],
               [1, 1, 0],
               [0, 1, 1]],
              [[0, 1, 0],
               [1, 1, 0],
               [1, 0, 0]]],
        'j': [[[1, 0, 0],
               [1, 1, 1],
               [0, 0, 0]],
              [[0, 1, 1],
               [0, 1, 0],
               [0, 1, 0]],
              [[0, 0, 0],
               [1, 1, 1],
               [0, 0, 1]],
              [[0, 1, 0],
               [0, 1, 0],
               [1, 1, 0]]],
        'l': [[[0, 0, 1],
               [1, 1, 1],
               [0, 0, 0]],
              [[0, 1, 0],
               [0, 1, 0],
               [0, 1, 1]],
              [[0, 0, 0],
               [1, 1, 1],
               [1, 0, 0]],
              [[1, 1, 0],
               [0, 1, 0],
               [0, 1, 0]]]
    }
    kick_table = {
        "jlstz": {0: [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)],
                  1: [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, -2), Point(1, -2)],
                  2: [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)],
                  3: [Point(0, 0), Point(-1, 0), Point(-1, 1), Point(0, -2), Point(-1, -2)]},
        "i": {0: [Point(0, 0), Point(-1, 0), Point(2, 0), Point(-1, 0), Point(2, 0)],
              1: [Point(-1, 0), Point(0, 0), Point(0, 0), Point(0, -1), Point(0, 2)],
              2: [Point(-1, -1), Point(1, -1), Point(-2, -1), Point(1, 0), Point(-2, 0)],
              3: [Point(0, -1), Point(0, -1), Point(0, -1), Point(0, 1), Point(0, -2)]},
        "o": {0: [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)],
              1: [Point(0, 1), Point(0, 1), Point(0, 1), Point(0, 1), Point(0, 1)],
              2: [Point(-1, 1), Point(-1, 1), Point(-1, 1), Point(-1, 1), Point(-1, 1)],
              3: [Point(-1, 0), Point(-1, 0), Point(-1, 0), Point(-1, 0), Point(-1, 0)]}
    }
    icon = {
               'i': [0, 0, 40, 0, 40, 10, 0, 10],
               'o': [0, 0, 20, 0, 20, 20, 0, 20],
               't': [0, 10, 10, 10, 10, 0, 20, 0, 20, 10, 30, 10, 30, 20, 0, 20],
               's': [0, 10, 10, 10, 10, 0, 30, 0, 30, 10, 20, 10, 20, 20, 0, 20],
               'z': [0, 0, 20, 0, 20, 10, 30, 10, 30, 20, 10, 20, 10, 10, 0, 10],
               'j': [0, 0, 10, 0, 10, 10, 30, 10, 30, 20, 0, 20],
               'l': [0, 10, 20, 10, 20, 0, 30, 0, 30, 20, 0, 20],
               'none': [0, 0, 0, 0, 0, 0]
    }
    shape_int = {
        0: 'n',
        1: 'i',
        2: 'o',
        3: 't',
        4: 's',
        5: 'z',
        6: 'j',
        7: 'l'
    }
    int_shape = {
        'n': 0,
        'i': 1,
        'o': 2,
        't': 3,
        's': 4,
        'z': 5,
        'j': 6,
        'l': 7
    }

    def __init__(self, c):
        self.shape = Tetromino.shapes[c]
        self.shapeName = c
        self.shapeOrient = 0
        self.x = 3
        self.y = 0
        self.kick = Point(0, 0)
        if self.shapeName == 'i':
            self.x = 2

    def get_coords(self):
        points = [Point(), Point(), Point(), Point()]
        counter = 0
        for j, row in enumerate(Tetromino.shapes[self.shapeName][self.shapeOrient]):
            for i, value in enumerate(row):
                if value:
                    points[counter].x = i + self.x
                    points[counter].y = j + self.y
                    counter += 1
        return points

    def rotate(self, cw, nk):  # CW = 1 CCW = -1
        if self.shapeName in "jlstz":
            self.kick = Tetromino.kick_table["jlstz"][self.shapeOrient][nk] - Tetromino.kick_table["jlstz"][
                ((self.shapeOrient + cw) % 4)][nk]
        else:
            self.kick = Tetromino.kick_table[self.shapeName][self.shapeOrient][nk] - Tetromino.kick_table[self.shapeName][
                ((self.shapeOrient + cw) % 4)][nk]
        self.shapeOrient = (self.shapeOrient + cw) % 4
        self.x += self.kick.x
        self.y += self.kick.y
        self.kick = Point(0, 0)


class Block:
    block_type = 0
    color = {
        'n': "gray",
        'i': "cyan",
        'o': "yellow2",
        't': "purple1",
        's': "green2",
        'z': "firebrick1",
        'j': "blue",
        'l': "chocolate1"
    }

    def __init__(self, t):
        self.block_type = t


class Tetris:
    def __init__(self, c=None):
        random.seed(1)
        self.commands = []
        self.bag = []
        self.play_field = [[]]
        self.hold = Tetromino('n')
        self.play_field_canvas = c
        self.locked = True
        self.active = True
        self.hold = Tetromino('n')
        self.blocks = [[]]
        self.queue = []
        self.queue_display = []
        self.play_field.clear()
        self.blocks.clear()

        self.total_cleared = 0
        self.total_moves = 0
        self.total_pieces = 0
        self.input_log = []
        self.current_piece = self.next_piece()

        for j in range(height()):
            self.play_field.append([])
            for i in range(width()):
                self.play_field[j].append(Block(0))
        if self.play_field_canvas is not None:
            for j, row in enumerate(self.play_field):
                self.blocks.append([])
                for i, block in enumerate(row):
                    self.blocks[j].append(self.play_field_canvas.create_rectangle(
                        i * size() + 5 * size(),
                        j * size() + 2 * size(),
                        (i + 1) * size() + 5 * size(),
                        (j + 1) * size() + 2 * size()))

            self.hold_display = self.play_field_canvas.create_polygon(Tetromino.icon['none'])
            for i in range(0, 5):
                self.queue_display.append(self.play_field_canvas.create_polygon(Tetromino.icon[self.queue[i]]))
            self.render()

    def hold_piece(self):
        if self.locked:
            if self.hold.shapeName != 'n':
                self.current_piece, self.hold = Tetromino(self.hold.shapeName), self.current_piece
            else:
                self.hold = self.current_piece
                self.current_piece = self.next_piece()
            self.locked = False

    def next_piece(self):
        while len(self.queue) < 150:  # generate first 150 blocks
            self.bag = pieces()
            random.shuffle(self.bag)
            self.queue.extend(self.bag)
        return Tetromino(self.queue.pop(0))

    def render(self):
        for j, row in enumerate(self.play_field):
            for i, block in enumerate(row):
                self.play_field_canvas.itemconfig(self.blocks[j][i], fill=Block.color[Tetromino.shape_int[block.block_type]])
        for i, block in enumerate(self.current_piece.get_coords()):
            self.play_field_canvas.itemconfig(self.blocks[block.y][block.x], fill=Block.color[self.current_piece.shapeName])
        if self.hold.shapeName != 'n':
            self.play_field_canvas.delete(self.hold_display)
            self.hold_display = self.play_field_canvas.create_polygon(Tetromino.icon[self.hold.shapeName])
            self.play_field_canvas.move(self.hold_display, 2*size(), 2*size())
        for i in range(len(self.queue_display)):
            self.play_field_canvas.delete(self.queue_display[i])
            self.queue_display[i] = self.play_field_canvas.create_polygon(Tetromino.icon[self.queue[i]])
            self.play_field_canvas.move(self.queue_display[i], (size() * (width() + 6)), (2 * size() + (size() * i)))

    def rotate(self, direction):
        # Test Rotation Collisions
        # A->B = A - B
        # (Current) - ((Current + Direction) % 4)
        self.current_piece.kick = Point(0, 0)
        # test.rotate(direction)
        for i in range(0, 5):
            test = copy.deepcopy(self.current_piece)
            test.rotate(direction, i)
            fits = True
            for point in test.get_coords():
                if point.x + test.kick.x < 0 or point.x + test.kick.x > width() - 1 \
                        or point.y + test.kick.y < 0 or point.y + test.kick.y > height() - 1 \
                        or self.play_field[point.y + test.kick.y][point.x + test.kick.x].block_type >= 1:
                    fits = False
                    break
            if fits:
                self.current_piece.rotate(direction, i)  # 1 = CW, -1 = CCW
                return

    def move(self, direction, times=1):
        while times > 0 or times == -1:
            if direction == 1:  # Right
                collide = False
                for point in self.current_piece.get_coords():
                    if point.x == width() - 1 or self.play_field[point.y][point.x + 1].block_type >= 1:
                        return
                if not collide:
                    self.current_piece.x += 1
            elif direction == 2:  # Down
                for point in self.current_piece.get_coords():
                    if point.y == height() - 1:
                        self.lock()
                        return
                    elif self.play_field[point.y+1][point.x].block_type >= 1:
                        self.lock()
                        return
                self.current_piece.y += 1
            elif direction == 3:  # Left
                for point in self.current_piece.get_coords():
                    if point.x == 0 or self.play_field[point.y][point.x - 1].block_type >= 1:
                        return
                self.current_piece.x -= 1
            if times > 0:
                times -= 1

    def lock(self):  # For now unforgiving
        linescleared = set()
        for point in self.current_piece.get_coords():
            if point.y == 12:
                self.active = False
            self.play_field[point.y][point.x] = Block(Tetromino.int_shape[self.current_piece.shapeName])
            line = True
            for block in self.play_field[point.y]:
                if block.block_type == 0:
                    line = False
            if line:
                linescleared.add(point.y)
        if len(linescleared) > 0:
            self.total_cleared += len(linescleared)
            for line in sorted(linescleared):
                self.play_field.insert(0, self.play_field.pop(line))
                for block in self.play_field[0]:
                    block.block_type = 0
        self.current_piece = self.next_piece()
        self.locked = True
        self.total_pieces += 1

    def replay(self):
        if len(self.input_log) > 0:
            self.input_c(self.input_log.pop(0))
            self.render()

    def run_commands(self, i):
        command_list = i.split(", ")
        while len(command_list) > 0:
            self.input_log.append(command_list[0])
            self.input_c(command_list.pop(0))
        if self.play_field_canvas is not None:
            self.render()

    def double_rotate(self):
        self.rotate(1)
        self.rotate(1)

    def input_c(self, c):
        if self.active:
            commands = {
                'space': lambda: self.move(direction=2, times=-1),
                'hd': lambda: self.move(direction=2, times=-1),
                'Left': lambda: self.move(direction=3, times=1),
                'l': lambda: self.move(direction=3, times=1),
                'Right': lambda: self.move(direction=1, times=1),
                'r': lambda: self.move(direction=1, times=1),
                'Down': lambda: self.move(direction=2, times=1),
                'sd': lambda: self.move(direction=2, times=1),
                'Shift_L': lambda: self.hold_piece(),
                'h': lambda: self.hold_piece(),
                's': lambda: self.rotate(direction=-1),
                'ccw': lambda: self.rotate(direction=-1),
                'Up': lambda: self.rotate(direction=1),
                'cw': lambda: self.rotate(direction=1),
                'd': lambda: self.double_rotate(),
                '180': lambda: self.double_rotate(),
                'dasr': lambda: self.move(direction=1, times=-1),
                'dasl': lambda: self.move(direction=3, times=-1)
            }
            if commands.get(c, lambda: 5)() != 5:
                self.total_moves += 1
    mino_to_float = {
        'n': 0,
        'i': 1/7,
        'o': 2/7,
        't': 3/7,
        's': 4/7,
        'z': 5/7,
        'j': 6/7,
        'l': 1
    }

    def output_data(self):
        data = np.zeros(shape=(23, 10))
        total = 0
        for row in self.play_field:
            for block in row:
                if block.block_type > 0:
                    total += 1
        for j, row in enumerate(self.play_field):
            for i, block in enumerate(row):
                if block.block_type > 0:
                    data[j][i] = 1/total
                else:
                    data[j][i] = 0
        for i in range(5):
            data[22][i] = self.mino_to_float[self.queue[i]]
            data[22][5] = self.mino_to_float[self.hold.shapeName]
            data[22][6] = self.mino_to_float[self.current_piece.shapeName]
            data[22][7] = self.current_piece.shapeOrient/3
            data[22][8] = self.current_piece.x / 10
            data[22][9] = self.current_piece.y / 23
        # print(len(two_pac))
        return data.transpose()
