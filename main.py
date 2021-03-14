import time
from msvcrt import getch
from os import system
from sys import stdout


# Size of the game field
WIDTH = 100
HIGHT = 20

# Game point
POINT = 0  # только цифры!

POINT_YX = [HIGHT - 1, WIDTH - 1]

# Keymap of control
keys = {
    0x48: (-1, 0),
    0x50: (1, 0),
    0x4b: (0, -1),
    0x4d: (0, 1), }
'''
0x48: 'Up' = +1, 0
0x50: 'Down' = -1, 0
0x4b: 'Left' = 0, -1
0x4d: 'Right' = 0, 1
'''

PRINT_MAP = {0: '░', 1: '█'}

# make game field
field = [[POINT * j for j in range(WIDTH)] for i in range(HIGHT)]


def clear():
    system('CLS')


def get_coord(coord=POINT_YX) -> int:
    Y, X = map(int, coord)
    return Y, X


def print_field(start):
    clear()
    print(f'POINT_YX {get_coord()}')
    for i in field:
        # как же мне нравится это решение
        print(''.join(PRINT_MAP[e] for e in i))

    fin = time.time()
    print('TIME: ', fin - start)


def add_point():

    y, x = get_coord()
    # первичное размещение точки
    field[y][x] = 1


def timed_input(timeout=0.03):
    # функция отвечающая за обработку нажатия клвиш
    def echo():
        stdout.flush()

    start = time.monotonic()
    while time.monotonic() - start < timeout:
        prefix = ord(getch())
        if msvcrt.kbhit():
            if prefix == 0xe0:
                keycode = ord(getch())
                symbol = keys.get(keycode, 'unexpected')
                echo()
                move(symbol)
                print(f'Press {symbol}')

            elif prefix == 3:
                echo()
                exit()


def move(vector):
    Y, X = get_coord()
    VECTOR_Y, VECTOR_X = get_coord(vector)

    if VECTOR_Y + Y <= HIGHT - 1 and VECTOR_Y + Y >= 0:
        NEW_Y = VECTOR_Y + Y
    else:
        NEW_Y = Y

    if VECTOR_X + X <= WIDTH - 1 and VECTOR_X + X >= 0:
        NEW_X = VECTOR_X + X
    else:
        NEW_X = X

    field[Y][X] = 0
    field[NEW_Y][NEW_X] = 1
    POINT_YX[0], POINT_YX[1] = NEW_Y, NEW_X


def loop():

    add_point()

    while True:
        start = time.time()
        print_field(start)
        timed_input()


if __name__ == '__main__':
    loop()
