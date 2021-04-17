'''
Arkanoid version 1.1.2
by Di2mot
'''


from time import perf_counter, monotonic, sleep
from msvcrt import getch, kbhit
from os import system, name
from sys import stdout
import ctypes
from ctypes import c_long, c_wchar_p, c_ulong, c_void_p
from array import array


gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))

# Size of the game FIELD
WIDTH = 100
HIGHT = 20

# Game point
POINT = 0  # только цифры, строки конноктирует!

# начальные координаты точки
POINT_YX = array('b',[0, 0])

# заготовка для платформі
PLATFORM = [0]

# Keymap of control
keys = {
    0x4b: (0, -1),
    0x4d: (0, 1), }
'''
0x48: 'Up' = -1,        0x48: (-1, 0)
0x50: 'Down' = 1, 0     0x50: (1, 0)
0x4b: 'Left' = 0, -1    0x4b: (0, -1)
0x4d: 'Right' = 0, 1    0x4d: (0, 1),
'''
# счёт
SCORE = array('b', [0])

PRINT_MAP = {
    0: '░',
    1: '▢',
    2: '■',
    3: '-',
    4: '|',
    5: '█',
    6: '=',
}  # {0: '░', 1: '█', 2:'▢', 3: '-', 4: '|',}

ROUT = [-1, 1]

# make game FIELD
FIELD = [0]


def add_point(POINT_YX):
    y, x = map(int, POINT_YX)
    FIELD[y][x] = 1                 # первичное размещение точки



def make_field():
    '''
    Здесь создаётся игровое поле о всеми вытекающими
    '''
    FIELD.clear()
    PLATFORM.clear()

    ## make game FIELD

    for y in range(HIGHT):
        fl = array('b', [POINT * i for i in range(WIDTH)])
        FIELD.append(fl)


    # FIELD = [[POINT * j for j in range(WIDTH)] for i in range(HIGHT)]

    #  верхнюю строчку превращаем в заборчик

    FIELD[0] = [3 for j in range(WIDTH)]

    FIELD[0] = array('b', [6 for i in range(WIDTH)])


    FIELD[0] = array('b', [6 for i in range(WIDTH)])
    print(FIELD)


    #  нижню строчку превращаем в заборчик
    FIELD[HIGHT - 1] = array('b',[6 for j in range(WIDTH)])

    # левую и правые стороны превращаем в столбики
    for y in range(1, HIGHT - 1):
        for x in (0, WIDTH - 1):
            FIELD[y][x] = 4

    # создаём блоки в которые будет бится шар
    for y in range(1, 5):
        for x in range(1, WIDTH - 1):
            FIELD[y][x] = 2

    # make platform
    for x in range(WIDTH // 2 - 6, WIDTH // 2 + 4):
        FIELD[HIGHT - 2][x] = 5
        PLATFORM.append([HIGHT - 2, x])

    # FIELD[START_POS[0]][START_POS[1]] = 1        # первичное размещение точки

def start_game():
    '''
    cоздаём новую игру
    '''

    # начальные координаты точки на 1 стоку выше платформы
    POINT_YX[0], POINT_YX[1] = HIGHT - 4, WIDTH // 2
    # начальный вектор
    ROUT[0], ROUT[1] = -1, 1
    # начальный результат
    SCORE[0] = 0
    # генерируем поле
    make_field()
    # ставим точку на поле
    add_point(POINT_YX)


def clear() -> None:
    '''
    Очистка экрнана
    '''

    system('cls' if name == 'nt' else 'clear')

def end_game():
    stdout.write(f'Игра оконченна\n Ваш результат:{SCORE}\n')
    key: str = input('Хотите сыграть ещё?\n Для начала новой игры нажмите Y \n\
    если хотите выйти то люую клавишу   ')

    if key.upper() == 'Y':
        loop()
    else:
        exit()



def print_FIELD(start_time):
    '''
    Выводит в консоль поле
    Обновляя консоль кажды раз
    '''
    clear()

    y, x = map(int, POINT_YX)
    finish_time = perf_counter()
    FPS = 1 // (finish_time - start_time)


    stdout.write(f'\
        SCORE = {SCORE[0]}  [y = {y}, x = {x}] Vector {ROUT} FPS = {FPS}\n')

    ST = str()

    for line in FIELD:

        # работает через коннотацию строк
        ST += ''.join(PRINT_MAP[e] for e in line) + '\n'


    if name == 'nt':
        ctypes.windll.kernel32.WriteConsoleW(gHandle, c_wchar_p(
            ST), c_ulong(len(ST)), c_void_p(), None) # так экран мерцат меньше
    else:
        stdout.write(ST)                             # так экран мерцат меньше


    stdout.flush()


def rout_v(coord):
    '''
    Отвечает за отскок меняя вектор направления на противоположный
    '''

    if PLATFORM[0][1] <= 1 and coord[1] == -1:
        pass
    elif PLATFORM[-1][1] >= WIDTH - 2 and coord[1] == 1:
        pass
    else:
        for X in range(len(PLATFORM)):
            FIELD[PLATFORM[X][0]][PLATFORM[X][1]] = 0
        for X in range(len(PLATFORM)):
            PLATFORM[X][1] += coord[1]
            FIELD[PLATFORM[X][0]][PLATFORM[X][1]] = 5


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

    start = monotonic()
    while monotonic() - start < timeout:

        echo()

        if kbhit():
            '''
            getch() вызывается дважды не просто так,
            т.к. управление стрелочками а стрелочки при нажатии
            генерируют два кода, и соответственно нужно
            дважды обрабатывать
            '''
            prefix = ord(getch())
            if prefix == 0xe0:
                echo()
                keycode = ord(getch())
                symbol = keys.get(keycode, [0, 0])

                rout_v(symbol)  # отвечает за платформу

            # Отвечает за комбинацию Ctrl + C
            elif prefix == 3:
                echo()
                exit()
            else:
                pass


def move():
    '''
    '''
    Y, X = map(int, POINT_YX)                   # нынешние координаты точки

    # ROUT[0] = Y
    # ROUT[1] = X

    # Проверяю соприкаснётся шар с поверхностью
    # и по какой оси его нужно отразить

    # проверямем, не попал ли мяч в пол
    if Y + ROUT[0] == HIGHT - 1:
        end_game()

    elif FIELD[Y + ROUT[0]][X] in (2, 3, 4, 5,):

        # проверяем где нужно удалить блок
        if FIELD[Y + ROUT[0]][X] == 2:
            FIELD[Y + ROUT[0]][X] = 0
            SCORE[0] += 1

        ROUT[0] = ROUT[0] * -1
        NEW_Y = Y + ROUT[0]

        if FIELD[NEW_Y][X + ROUT[1]] not in (3, 4):
            NEW_X = X + ROUT[1]
        else:
            ROUT[1] = ROUT[1] * -1
            NEW_X = X + ROUT[1]

    elif FIELD[Y][X + ROUT[1]] in (2, 3, 4, 5,):

        # проверяем где нужно удалить блок
        if FIELD[Y][X + ROUT[1]] == 2:
            FIELD[Y][X + ROUT[1]] = 0
            SCORE[0] += 1

        # меняем направление по оси х
        ROUT[1] = ROUT[1] * -1
        # устанавливаем новое положение х
        NEW_X = X + ROUT[1]
        NEW_Y = Y + ROUT[0]                         # новое положение у

    else:
        # если нет припятсвий то летит дальше
        NEW_Y = Y + ROUT[0]
        NEW_X = X + ROUT[1]

    # обнуляем прошлое положение точки
    FIELD[Y][X] = 0
    FIELD[NEW_Y][NEW_X] = 1                      # рисуем точку в новом месте
    POINT_YX[0], POINT_YX[1] = NEW_Y, NEW_X      # обновляем координату точки


def loop():
    '''
    Главный цикл
    '''
    start_game()

    while True:
        start_time = perf_counter()
        print_FIELD(start_time)
        move()
        timed_input()


if __name__ == '__main__':
    loop()
