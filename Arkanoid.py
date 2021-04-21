# -*- coding: utf-8 -*-
'''
Arkanoid version 1.2.1
by Di2mot
'''

from time import perf_counter, monotonic
from msvcrt import getch, kbhit
from os import system, name
from sys import stdout
from array import array
from getpass import getuser

if name == 'nt':
    import ctypes
    from ctypes import c_long, c_wchar_p, c_ulong, c_void_p
    gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))

# Size of the game FIELD
WIDTH = 100
HIGHT = 20

# Game point
POINT = 0  # только цифры, строки конноктирует!

# начальные координаты точки
POINT_YX = array('b', [0, 0])

# заготовка для платформы
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

# направление движения
ROUT = [-1, 1]

# make game FIELD
FIELD = [0]

# статус игры
GAME_STATUS = [0]

# коэфициент отвечающий за количество блоков
AMOUNT = 5


def add_point(POINT_YX):
    '''
    первичное размещение точки
    '''
    y, x = map(int, POINT_YX)
    FIELD[y][x] = 1


def make_field():
    '''
    Здесь создаётся игровое поле о всеми вытекающими
    '''
    FIELD.clear()
    PLATFORM.clear()

    # make game FIELD

    for y in range(HIGHT):
        fl = array('b', [POINT * i for i in range(WIDTH)])
        FIELD.append(fl)

    #  верхнюю строчку превращаем в заборчик
    FIELD[0] = array('b', [3 for i in range(WIDTH)])

    #  ижняя строчку превращаем в лаву!
    FIELD[HIGHT - 1] = array('b', [6 for j in range(WIDTH)])

    # левую и правые стороны превращаем в столбики
    for y in range(1, HIGHT - 1):
        for x in (0, WIDTH - 1):
            FIELD[y][x] = 4

    # создаём блоки в которые будет бится шар
    for y in range(1, AMOUNT):
        for x in range(1, WIDTH - 1):
            FIELD[y][x] = 2

    # make platform
    for x in range(WIDTH // 2 - 6, WIDTH // 2 + 4):
        FIELD[HIGHT - 2][x] = 5
        PLATFORM.append([HIGHT - 2, x])

    # FIELD[START_POS[0]][START_POS[1]] = 1        # первичное размещение точки


def write_records(SCORE, name=getuser(), file_name='arkanoid_score.txt'):

    with open(file_name, 'a') as record:
        record.write('='.join(name, str(SCORE[0])))

def read_records(file_name='arkanoid_score.txt'):
    max = 0
    with open(file_name, 'r') as record:
        for line in record:
            if int(line.split('=')[1]) > max:
                max = int(line.split('=')[1])
        return max

def start_game():
    '''
    Создаём новую игру
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

    if GAME_STATUS[0] == 0:
        print_FIELD()
        game_name = 'Arkanoid v.1.2'
        start_game_text = 'Для начала игры нажмите: Y'
        exit_game_text = 'Для выхода нажмите любую клавишу '

        # для сокращения записи
        H = HIGHT // 2

        if name == 'nt':
            move_cursor(H, WIDTH // 2 - len(game_name) // 2)
            stdout.write(game_name)
            stdout.flush()

            move_cursor(H + 2, WIDTH // 2 - len(start_game_text) // 2)
            stdout.write(start_game_text)
            stdout.flush()

            move_cursor(H + 3, WIDTH // 2 - len(exit_game_text) // 2)
            stdout.write(exit_game_text)
            stdout.flush()
            key: str = input('  ')
            move_cursor(HIGHT + 1, 0)  # переводим курсор ниже поля

        else:
            # '\033[8;1H' перевод курсора на 8 строку, 1 столбец в Linux

            W = WIDTH // 2 - len(game_name) // 2

            stdout.write(
                f'\033[{H};{W}H' + game_name)
            stdout.flush()

            stdout.write(
                f'\033[{H + 2};{W}H' + game_name)
            stdout.flush()

            stdout.write(
                f'\033[{H + 3};{W}H' + game_name)
            stdout.flush()
            key: str = input('  ')

        if key.upper() != 'Y':
            exit()
    GAME_STATUS[0] = 1


def end_game():
    '''
    Отвечает за выход из игры
    '''
    game_over = 'Game over!'
    end_game_text = f'Ваш результат: {SCORE[0]}'
    end_game_q = 'Хотите сыграть ещё?'
    for_new_game = 'Для начала новой игры нажмите Y'
    for_exit_game = 'Eсли хотите выйти то любую клавишу   '

    # '\033[8;1H'  f'\033[{8};{1}H'
    if name == 'nt':
        move_cursor(HIGHT // 2, WIDTH // 2 - len(game_over) // 2)
        stdout.write(game_over)
        stdout.flush()

        move_cursor((HIGHT // 2) + 2, WIDTH // 2 - len(end_game_text) // 2)
        stdout.write(end_game_text)
        stdout.flush()

        move_cursor((HIGHT // 2) + 3, WIDTH // 2 - len(end_game_q) // 2)
        stdout.write(end_game_q)
        stdout.flush()

        move_cursor((HIGHT // 2) + 4, WIDTH // 2 - len(for_new_game) // 2)

    else:
        H = HIGHT // 2
        W = WIDTH // 2 - len(game_over) // 2

        stdout.write(f'\033[{H};{W}H' + game_over)
        stdout.flush()

        stdout.write(f'\033[{H + 2};{W}H' + end_game_text)
        stdout.flush()

        stdout.write(f'\033[{H + 3};{W}H' + end_game_q)
        stdout.flush()

        stdout.write(f'\033[{H + 4};{W}H')
        stdout.flush()

    key: str = input('Хотите сыграть ещё раз? Y/N   ')
    stdout.flush()
    if key.upper() == 'Y':
        loop()
    else:
        move_cursor(HIGHT + 1, 0)  # перводим курсор ниже поля
        exit()


def win():
    win_text = 'You win!'
    win_q = 'Хотите сыграть ещё раз? Y/N'

    H = HIGHT // 2
    W = WIDTH // 2 - len(win_q) // 2

    if name == 'nt':
        move_cursor(H, WIDTH // 2 - len(win_text) // 2)
        stdout.write(win_text)
        stdout.flush()

        move_cursor(H + 2, WIDTH // 2 - len(win_q) // 2)
        stdout.write(win_q)
        stdout.flush()
    else:
        stdout.write(f'\033[{H};{W}H' + win_text)
        stdout.flush()

        stdout.write(f'\033[{H + 2};{W}H' + win_q)
        stdout.flush()

    key: str = input('Введите ответ   ')
    stdout.flush()
    if key.upper() == 'Y':
        loop()
    else:
        move_cursor(HIGHT + 1, 0)  # перводим курсор ниже поля
        exit()


def clear() -> None:
    '''
    Очистка экрнана
    '''

    system('cls' if name == 'nt' else 'clear')


def move_cursor(y, x):
    """Move cursor to position indicated by x and y."""
    value = x + (y << 16)
    ctypes.windll.kernel32.SetConsoleCursorPosition(gHandle, c_ulong(value))


def print_FIELD(start_time=0):
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

    # так экран мерцат меньше
    if name == 'nt':
        ctypes.windll.kernel32.WriteConsoleW(gHandle, c_wchar_p(
            ST), c_ulong(len(ST)), c_void_p(), None)
    else:
        stdout.write(ST)

    stdout.flush()


def rout_v(coord):
    '''
    Отвечает за управление движением платформы
    '''

    # проверяет не находится ли платформа у края поля
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

    # проверямем, не попал ли мяч в платформу
    elif [Y + ROUT[0], X + ROUT[1]] in PLATFORM:

        # получаем индекс вхождения [Y, X] в массиве PLATFORM
        PL_index = PLATFORM.index([Y + ROUT[0], X + ROUT[1]])

        # отбиваем шар в сторону
        # если попало в правую часть платформы
        if PL_index > len(PLATFORM) // 2:
            ROUT[1] = 1
        # если попало в левую часть платформы
        else:
            ROUT[1] = -1
        ROUT[0] = -1
        NEW_Y = Y + ROUT[0]
        NEW_X = X + ROUT[1]

    # если шар попал в боковые поверхности, верх, и блоки
    # проверям по оси Y
    elif FIELD[Y + ROUT[0]][X] in (2, 3, 4,):

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

    # проверяем по оси X
    elif FIELD[Y][X + ROUT[1]] in (2, 3, 4,):

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

        if SCORE[0] >= AMOUNT * (WIDTH - 2):
            win()


if __name__ == '__main__':
    loop()
