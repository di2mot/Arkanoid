# -*- coding: utf-8 -*-
'''
Arkanoid version 1.6
by Di2mot
'''
VERSION = 1.6

from time import perf_counter, monotonic, strftime
from os import system, name
from sys import stdout
from array import array
from getpass import getuser

if name == 'nt':

    from msvcrt import getch, kbhit
    import ctypes
    from ctypes import c_long, c_wchar_p, c_ulong, c_void_p

    gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))
else:
    # for UNIX systems
    import curses
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)
    curses.echo()
    stdscr.nodelay(True)

import argparse

# Size of the game FIELD
# Размер игрового поля
WIDTH = 100
HIGHT = 20

# coefficient for the number of blocks
# коэфициент отвечающий за количество блоков
AMOUNT = 5

# parsing startup parameters from the command line
# парсинг параметров запуска из командной строки
argpars_text = '''
Arkanoid by Di2mot

A small simple game in Python, without external modules. 
To set the parameters of the playing field, call the script with these parameters:
python Arkanoid.py --h=20 --w=100 --a=4
Where:
 --h - height in lines
 --w - width in columns
 --a - number of lines in blocks
'''

parser = argparse.ArgumentParser(description=argpars_text)
parser.add_argument(
    '--h',
    type=int,
    default=HIGHT,
    help='height in lines'
)
parser.add_argument(
    '--w',
    type=int,
    default=WIDTH,
    help='width in columns'
)
parser.add_argument(
    '--a',
    type=int,
    default=AMOUNT,
    help='block rows'
)
my_namespace = parser.parse_args()

HIGHT, WIDTH, AMOUNT = my_namespace.h, my_namespace.w, my_namespace.a


'''
 what the playing field is made up
 only numbers, strings are not!
 из чего состоит игровое поле
 только цифры, строки конноктирует!
'''
POINT = 0

# start point coordinates
# начальные координаты точки
POINT_YX = array('b', [0, 0])

# platform blank
# заготовка для платформы
PLATFORM = [0]

# Keymap of control
# коды клавиш
keys = {
    0x4b: (0, -1),
    0x4d: (0, 1),
    'KEY_LEFT': (0, -1),
    'KEY_RIGHT': (0, 1),  }
'''
0x48: 'Up' = -1,        0x48: (-1, 0)
0x50: 'Down' = 1, 0     0x50: (1, 0)
0x4b: 'Left' = 0, -1    0x4b: (0, -1)
0x4d: 'Right' = 0, 1    0x4d: (0, 1),
'''
# score
# счёт
SCORE = array('b', [0])

'''
Map converting numbers into textures
Карта преобразования цифр в текстуры
'''
PRINT_MAP = {
    0: '░',
    1: '▢',
    2: '■',
    3: '-',
    4: '|',
    5: '█',
    6: '=',
}

# direction of travel
# направление движения
ROUT = [-1, 1]

# make game FIELD
# создаём игровое поле
FIELD = [0]

# game status
# статус игры
GAME_STATUS = [0]



def add_point(POINT_YX):
    '''
    initial placement of the point
    первичное размещение точки
    '''
    y, x = map(int, POINT_YX)
    FIELD[y][x] = 1


def make_field():
    '''
    This creates a playing field
    Здесь создаётся игровое поле о всеми вытекающими
    '''
    FIELD.clear()
    PLATFORM.clear()

    # make game FIELD

    for y in range(HIGHT):
        fl = array('b', [POINT * i for i in range(WIDTH)])
        FIELD.append(fl)

    # top line turn into a fence
    #  верхнюю строчку превращаем в заборчик
    FIELD[0] = array('b', [3 for i in range(WIDTH)])

    # the bottom line turn into lava!
    #  ижняя строчку превращаем в лаву!
    FIELD[HIGHT - 1] = array('b', [6 for j in range(WIDTH)])

    # left and right sides turn into columns
    # левую и правые стороны превращаем в столбики
    for y in range(1, HIGHT - 1):
        for x in (0, WIDTH - 1):
            FIELD[y][x] = 4

    # create the blocks into which the ball will hit
    # создаём блоки в которые будет бится шар
    for y in range(1, AMOUNT):
        for x in range(1, WIDTH - 1):
            FIELD[y][x] = 2

    # make platform
    # генерируем платформу
    for x in range(WIDTH // 2 - 6, WIDTH // 2 + 4):
        FIELD[HIGHT - 2][x] = 5
        PLATFORM.append([HIGHT - 2, x])

    # FIELD[START_POS[0]][START_POS[1]] = 1        # первичное размещение точки


def write_records(SCORE, name=getuser(), file_name='arkanoid_score.txt'):
    '''
    write the result in the file
    записываем результат в файлик
    '''
    with open(file_name, 'a') as record:
        date = ''.join([strftime('%H:%M %d.%m.%Y'), '\n'])
        line = '='.join([name, str(SCORE[0]), date])
        record.write(line)


def read_records(file_name='arkanoid_score.txt'):
    '''
    get the best result
    получаем лучший результат
    '''
    max = 0
    with open(file_name, 'r') as record:
        for line in record:
            if int(line.split('=')[1]) > max:
                max = int(line.split('=')[1])
        return max

def exit_game():
    '''
    for exit from the game
    '''
    if name == 'nt':
        move_cursor(HIGHT + 1, 0)
        exit()
    else:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        exit()

def start_game():
    '''
    Creating a new game
    Создаём новую игру
    '''

    # initial coordinates of the point 1 stack above the platform
    # начальные координаты точки на 1 стоку выше платформы
    POINT_YX[0], POINT_YX[1] = HIGHT - 4, WIDTH // 2

    # initial motion vector
    # начальный вектор
    ROUT[0], ROUT[1] = -1, 1

    # reset the result to zero
    # обнуляем результат
    SCORE[0] = 0

    # generate the field
    # генерируем поле
    make_field()

    # put a dot in the field
    # ставим точку на поле
    add_point(POINT_YX)

    if GAME_STATUS[0] == 0:
        print_FIELD()
        game_name = f'Arkanoid v.{VERSION}'
        start_game_text = 'To start the game, press: Y'
        exit_game_text = 'To exit, press any key '

        # to shorten the record
        # для сокращения записи
        H = HIGHT // 2
        W = WIDTH // 2

        '''
        Для вывода на экран текст, переводим курсор в нужное положение
        To display the text on the screen, move the cursor to the desired position
        '''
        move_cursor(H, W - len(game_name) // 2)
        print_func(game_name)

        move_cursor(H + 2, W - len(start_game_text) // 2)
        print_func(start_game_text)

        move_cursor(H + 3, W - len(exit_game_text) // 2)
        print_func(exit_game_text)

        if name == 'nt':
            key: str = input('  ')

            '''
            переводим курсор ниже поля, для того, что если откажется играть, 
            текст выводилс ниже экрана
            move the cursor below the field, so that if he refuses to play, 
            the text will be displayed below the screen
            '''
            move_cursor(HIGHT + 1, 0)

        else:
            stdscr.nodelay(False)
            key = stdscr.getkey()
            stdscr.nodelay(True)

        if key.upper() != 'Y':
            exit_game()
    GAME_STATUS[0] = 1


def end_game():
    '''
    Responsible for quitting the game
    Отвечает за выход из игры
    '''
    game_over = 'Game over!'
    end_game_text = f'Your score: {SCORE[0]}'

    for_new_game = 'Would you like to play again? Y/N   '

    move_cursor(HIGHT // 2, WIDTH // 2 - len(game_over) // 2)
    print_func(game_over)

    move_cursor((HIGHT // 2) + 2, WIDTH // 2 - len(end_game_text) // 2)
    print_func(end_game_text)

    move_cursor((HIGHT // 2) + 4, WIDTH // 2 - len(for_new_game) // 2)
    print_func(for_new_game)

    if name == 'nt':
        key: str = input()

    else:
        # for UNIX
        stdscr.nodelay(False)
        key = stdscr.getkey()
        stdscr.nodelay(True)

    if key.upper() == 'Y':
        loop()
    else:
        exit_game()


def win():
    '''
    In the case of victory
    В случае победы
    '''

    win_text = 'You win!'
    win_q = 'Would you like to play again? Y/N'

    H = HIGHT // 2
    W = WIDTH // 2 - len(win_q) // 2

    move_cursor(H, W - len(win_text) // 2)
    print_func(win_text)


    move_cursor(H + 2, W - len(win_q) // 2)
    print_func(win_q)

    if name == 'nt':
        key: str = input()


    else:
        stdscr.nodelay(False)
        key = stdscr.getkey()
        stdscr.nodelay(True)


    if key.upper() == 'Y':
        loop()
    else:
        exit_game()


def clear() -> None:
    '''
    Screen Cleaning
    Очистка экрана
    '''

    system('cls')


def move_cursor(y, x):
    '''
    Переместить курсор в позицию, обозначенную x и y.
    Windows only. Move cursor to position indicated by x and y.
    Thanks to stackoverflow
    '''
    if name == 'nt':
        value = x + (y << 16)
        ctypes.windll.kernel32.SetConsoleCursorPosition(gHandle, c_ulong(value))
    else:
        stdscr.move(y, x)

def print_func(text: str):
    '''
    displays the text in the console.
    It uses different methods for different operating systems
    выводит в консоль текст.
    Для разных ОС исользует разные способы
    '''
    if name == 'nt':
        stdout.write(text)
        stdout.flush()
    else:
        try:
            stdscr.addstr(text)
        except curses.error:
            pass


def print_FIELD():
    '''
    Outputs the playing field to the console, overwriting it from top to bottom
    Go through the array and line by line preconvert into str() lines
    After the playing field is formed, display

    Выводит в консоль игровое поле перезаписывая его сверху в низ
    Проходим по массиву и построчно предобразуем в строки str()
    После того как сформировали игровое поле, выодим на экран
    '''

    move_cursor(0, 0)

    print_func(f'SCORE = {SCORE[0]}\n')

    # blank string in which the field will be added
    # заготовка строки в которую будет добавляться поле
    ST = str()

    for line in FIELD:
        # works through string connotation
        # работает через коннотацию строк
        ST += ''.join(PRINT_MAP[e] for e in line) + '\n'

    # works through string connotation
    # так экран мерцат меньше
    if name == 'nt':
        ctypes.windll.kernel32.WriteConsoleW(gHandle, c_wchar_p(
            ST), c_ulong(len(ST)), c_void_p(), None)
        stdout.flush()
    else:
        print_func(ST)




def move_platform(coord):
    '''
    Responsible for controlling the movement of the platform
    Отвечает за управление движением платформы
    '''
    # checks if the platform is at the edge of the field
    # проверяет не находится ли платформа у края поля
    if PLATFORM[0][1] <= 1 and coord[1] == -1:
        pass
    elif PLATFORM[-1][1] >= WIDTH - 2 and coord[1] == 1:
        pass
    else:
        '''
        very suboptimal, in several passes overwrites the 
        position of the platform

        очень не оптимально, в нескалько подходов 
        перезаписывает положение платформы
        '''
        for X in range(len(PLATFORM)):
            FIELD[PLATFORM[X][0]][PLATFORM[X][1]] = 0

        for X in range(len(PLATFORM)):
            PLATFORM[X][1] += coord[1]
            FIELD[PLATFORM[X][0]][PLATFORM[X][1]] = 5


def timed_input(timeout=0.1):
    '''
    function responsible for handling keystrokes
    timeout: is responsible for the time the script waits
    before it continues to run, the smaller the value is,
    the more often the screen will be refreshed

    функция отвечающая за обработку нажатия клвиш
    timeout: отвечает за время которое скрипт ждёт
    прежде чем продолжить выполнение чем меньше значение,
    тем чаще будет обновляться экран
    '''

    start = monotonic()

    while monotonic() - start < timeout:

        if name == 'nt':

            stdout.flush()

            if kbhit():
                '''
                getch() is called twice for a reason,
                because the arrow control and the arrows, when pressed
                generate two codes and, consequently, we have to
                handle

                getch() вызывается дважды не просто так,
                т.к. управление стрелочками а стрелочки при нажатии
                генерируют два кода, и соответственно нужно
                дважды обрабатывать
                '''
                prefix = ord(getch())
                if prefix == 0xe0:
                    stdout.flush()
                    keycode = ord(getch())
                    symbol = keys.get(keycode, [0, 0])
                    move_platform(symbol)

                # Responsible for the Ctrl + C combination
                # Отвечает за комбинацию Ctrl + C
                elif prefix == 3:
                    stdout.flush()
                    exit()
                else:
                    pass
        else:
            key=""
            try:
                keycode = stdscr.getkey()
                symbol = keys.get(keycode, (0, 0))
                move_platform(symbol)
            except curses.error:
                pass


def move():
    '''
    Responsible for moving the point across the screen
    Отвечает за перемещение точки по экрану
    '''

    # current point coordinates
    # нынешние координаты точки
    Y, X = map(int, POINT_YX)

    # ROUT[0] = Y
    # ROUT[1] = X

    '''
    check if the ball is in contact with the surface
    and along which axis it should be reflected

    Проверяю соприкаснётся шар с поверхностью
    и по какой оси его нужно отразить
    '''

    # check to see if the ball hit the floor
    # проверямем, не попал ли мяч в пол
    if Y + ROUT[0] == HIGHT - 1:
        end_game()

    # check to see if the ball has hit the platform
    # проверямем, не попал ли мяч в платформу
    elif [Y + ROUT[0], X + ROUT[1]] in PLATFORM:

        # get the index of the occurrence [Y, X] in the PLATFORM array
        # получаем индекс вхождения [Y, X] в массиве PLATFORM
        PL_index = PLATFORM.index([Y + ROUT[0], X + ROUT[1]])

        # kicking the ball to the side
        # отбиваем шар в сторону

        # if it hits the right side of the platform
        # если попало в правую часть платформы
        if PL_index > len(PLATFORM) // 2:
            ROUT[1] = 1
        
        # if hit on the left side of the platform       
        # если попало в левую часть платформы
        else:
            ROUT[1] = -1
        ROUT[0] = -1
        NEW_Y = Y + ROUT[0]
        NEW_X = X + ROUT[1]

    # if the ball hit the sides, the top, and the blocks
    # если шар попал в боковые поверхности, верх, и блоки

    # check the Y-axis
    # проверям по оси Y
    elif FIELD[Y + ROUT[0]][X] in (2, 3, 4,):

        # check where to delete the block
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

    # check along the X-axis
    # проверяем по оси X
    elif FIELD[Y][X + ROUT[1]] in (2, 3, 4,):

        # check where to delete the block
        # проверяем где нужно удалить блок
        if FIELD[Y][X + ROUT[1]] == 2:
            FIELD[Y][X + ROUT[1]] = 0
            SCORE[0] += 1

        # change the direction of the x-axis
        # меняем направление по оси х
        ROUT[1] = ROUT[1] * -1

        # set the new position x and y
        # устанавливаем новое положение х и у
        NEW_X = X + ROUT[1]
        NEW_Y = Y + ROUT[0]

    else:
        # if there are no obstacles, it flies on
        # если нет припятсвий то летит дальше
        NEW_Y = Y + ROUT[0]
        NEW_X = X + ROUT[1]

    # reset the past position of the point, draw the point at the new location
    # update the point coordinate

    # обнуляем прошлое положение точки, рисуем точку в новом месте
    # обновляем координату точки
    FIELD[Y][X] = 0
    FIELD[NEW_Y][NEW_X] = 1
    POINT_YX[0], POINT_YX[1] = NEW_Y, NEW_X


def loop():
    '''
    Main cycle
    Главный цикл
    '''
    clear()

    start_game()

    while True:

        print_FIELD()
        move()
        timed_input()

        if SCORE[0] >= AMOUNT * (WIDTH - 2):
            win()


if __name__ == '__main__':
    loop()
