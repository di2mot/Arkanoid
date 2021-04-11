import time
from msvcrt import getch, kbhit
from os import system, name
from sys import stdout
import tracemalloc


# Size of the game field
WIDTH = 100
HIGHT = 20

# Game point
POINT = 0  # только цифры!

POINT_YX = [HIGHT - 1, WIDTH / 2 ]

# Keymap of control
keys = {
    0x48: (-1, 0),
    0x50: (1, 0),
    0x4b: (0, -1),
    0x4d: (0, 1), }
'''
0x48: 'Up' = -1, 0
0x50: 'Down' = 1, 0
0x4b: 'Left' = 0, -1
0x4d: 'Right' = 0, 1
'''

PRINT_MAP = {0: '░', 1: '█', 2:'▢'} # {0: '░', 1: '█', 2:'▢'}

ROUT = [-1, 1]

# make game field
field = [[POINT * j for j in range(WIDTH)] for i in range(HIGHT)]


def clear():
    system('cls' if name == 'nt' else 'clear')


def get_coord(coord=None) -> int:

    if coord is None:
        coord = POINT_YX
    Y, X = map(int, coord)
    return Y, X


def print_field(start_time):
    '''
    Выводит в консоль поле
    Обновляя консоль кажды раз
    '''
    clear()
    x, y = get_coord()
    print(f'Coordinate: [y = {y}, x = {x}] Vector {ROUT}')
    print('#' * (WIDTH + 2))

    ST = ''
    for line in field:
        # как же мне нравится это решение
        # print('#', ''.join(PRINT_MAP[e] for e in line), end='#\n')

        # работает через коннотацию строк
        ST += '#' + ''.join(PRINT_MAP[e] for e in line) + '#\n'

    # так не мерцает экран
    stdout.write(ST)

    print('#' * (WIDTH + 2))
    #fin = time.time()
    print(f'Frame time:  {time.time() - start_time:.5f}', "Current: %d, Peak %d" %
          tracemalloc.get_traced_memory())


def add_point(START_POS):

    y, x = get_coord(START_POS)
    # первичное размещение точки
    field[y][x] = 1


def rout_v(coord):
    '''
    Отвечает за отскок меняя вектор направления на противоположный
    '''
    if coord[0] != 0:
        ROUT[0] = coord[0]
    if coord[1] != 0:
        ROUT[1] = coord[1]


def timed_input(timeout=0.1):
    '''
    функция отвечающая за обработку нажатия клвиш
    timeout: отвечает за время которое скрипт ждёт
    прежде чем продолжить выполнение чем меньше значение,
    тем чаще будет обновляться экран
    '''

    def echo():
        '''
        Функция сбрасывает буфер, не давая Пиону ожадать,
        и выполняет код дальше
        '''
        stdout.flush()

    start = time.monotonic()
    while time.monotonic() - start < timeout:

        echo()

        if kbhit():
            '''
            getch() вызывается дважды не просто так, т.к. управление стрелочками
            а стрелочки при нажатии генерируют два кода, и соответственно нужно
            дважды обрабатывать
            '''
            prefix = ord(getch())
            if prefix == 0xe0:
                echo()
                keycode = ord(getch())
                symbol = keys.get(keycode, 'unexpected')

                rout_v(symbol)  # отвечает за отсткок

                print(f'Press {symbol}')
            # Отвечает за комбинацию Ctrl + C
            elif prefix == 3:
                echo()
                exit()
            else:
                pass


def move(vector=ROUT):
    '''
    '''
    Y, X = get_coord()  # нынешние координаты точки
    # коефициент который поменяет машрут
    VECTOR_Y, VECTOR_X = get_coord(vector)

    if VECTOR_Y + Y <= HIGHT - 1 and VECTOR_Y + Y >= 0:
        NEW_Y = VECTOR_Y + Y
    else:
        ROUT[0] = VECTOR_Y * -1
        NEW_Y = Y + ROUT[0]

    if VECTOR_X + X <= WIDTH - 1 and VECTOR_X + X >= 0:
        NEW_X = VECTOR_X + X
    else:
        ROUT[1] = VECTOR_X * -1
        NEW_X = X + ROUT[1]

    field[Y][X] = 0
    field[NEW_Y][NEW_X] = 1
    POINT_YX[0], POINT_YX[1] = NEW_Y, NEW_X


def loop():
    '''
    Главный цикл
    '''
    add_point(POINT_YX)

    while True:
        tracemalloc.start()
        start_time = time.time()
        print_field(start_time)
        move(ROUT)
        timed_input()


if __name__ == '__main__':
    loop()
