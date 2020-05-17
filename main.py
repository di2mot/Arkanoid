import msvcrt
import os
import time
import sys


hight = 15       # количество строк
width = 30      # шарина, т.е. сколько символов в строке

''' Устанавливаем размер игрового поля'''

os.system(f"mode con cols={width} lines={hight+1}")

def clear():
    os.system('CLS')

# Цикл
def loop(hight, width):

    '''

    :param hight:  - высота игрового полоя в символах
    :param width:  - ширина игрового поля в символах
    :return: ничего, просто выводит на экран
    '''

    '''
     status = ['run', 1] # хранит данные о игровых событиях:
     'run' / 'up' - бежит или прыгает
     0 - состояние прыжка, бывает 1, 2, 3, по сути прыжок, запис, опутсился
    '''
    status = ['run', 0] # хранит данные о игровых событиях

    # Поле
    field = [[ 0 * j for j in range(width)] for i in range(hight)]

    add_let(field)      # содаём препятсвие
    add_Dino(field)     # рисум Динозёбра


    ''' Рисуем решёлки'''
    fence = '#' * width


    colum = 0 # индекс столба
    iter = 0 # Считаем циклы

    # Главный циклы
    while True:

        # тут я ввёл ограничители по строкам
        line = 5
        # огранчение по количеству символов
        colum += 1

        

        # пока что сделал ограничение на количество циклов
        if iter == 50:
            gameEnd(fence, width)

        else:
            move(field, status)

            # снова заборчик
            print(fence)

            # счётчи количества итераций
            iter += 1

            # Функция которая ожидает ввода
            text = 'Для управления введи тречолку вверх или вниз'
            timed_input(status)


            # Для очистки терминала
            clear()
            print(fence)



# Функция которая ожидает ввод от пользователя определённое время
# если пользователь ничего не ввёл за указанное время
# то ничего не делает
def timed_input(status, timeout=0.5):
    def echo():
        sys.stdout.flush()

    start = time.monotonic()
    while time.monotonic() - start < timeout:
        if msvcrt.kbhit():
            c = msvcrt.getwch()
            if ord(c) == 32:
                echo()
                status[0] = 'up'
            if ord(c) == 80:
                echo()
                status[0] = 'print'




def move(field, status):

    '''
    :param field: - параметры игрового поля
    :param status: - сообщает о небходимом действии: 'u'p и 'run'
    :return:
    '''

    border_x = 0  # ограничение по х
    border_y = 4  # ограничение по у

    dino = {10: '/', 11: '#', 12: '@', 13: '\\', 14: '-', 15: '=', 16: '|'}

    for y in range(0, len(field)):
        tmp = []
        string = ''


        for x in range(0, len(field[y])):

            # if field[y][x] >= 10: # проверяем на условие проигрыша
            #     gameEnd('#'*50, 50)

            if status[0] == 'run':
                if field[y][x] in dino:
                    string += dino[field[y][x]]

            elif status[0] == 'up':
                if y + 1 <= len(field)-1:
                    # print(y+1, len(field))

                    if field[y + 1][x] in dino:
                        string += dino[field[y + 1][x]]
                        field[y][x] = 1
                        field[y + 1][x] = 0

            # debag tool - press 'P' - 'Shift + p'
            elif status[0] == 'print':
                os.system("mode con cols=300 lines=100")
                for x in field:
                    print(x)
                time.sleep(15)




            if field[y][x] == 0:
                tmp.append('.')
                string += '.'

            elif field[y][x] == 1:
                tmp.append('█')
                string += '█'
                field[y][x] = 0
                field[y][x-1] = 1

        # status[0] = 'run'
        # print(*tmp)

        print(string)

    if status[1] != 1:
        status[1] = status[1] - 1

    if status[1] == 0:
        status[0] = 'run'

def render(field, type, let, status):

    if type == 'DINO':

        if status[0] == 'run':
            pass

        elif status[0] == 'up':

            if DINO[len(DINO)-1][0] == len(field)-1:
                pass


            # перерисовываем в field место где раньше был динозёбр на 0
            for line in DINO:
                line[0] = line[0] - 1
                field[DINO[0][0]][DINO[0][1]]

            # а тут перепиывам уже с дино на филд
            for line in DINO:
                line[0] = line[0] - 1
                field[DINO[0][0]][DINO[0][1]]

        elif status[0] == 'down':

            if DINO[0][0] == len(field) - 1:
                status[0] = 'run'
            else:
                # перерисовываем в field место где раньше был динозёбр на 0
                for line in DINO:
                    line[0] = line[0] + 1
                    field[DINO[0][0]][DINO[0][1]]

                # а тут перепиывам уже с дино на филд
                for line in DINO:
                    line[0] = line[0] + 1
                    field[DINO[0][0]][DINO[0][1]]


    elif type == 'LET':
        pass


def add_let(field):
    ''' Препятсвия'''
    field[hight - 1][width - 2] = 1  # устанавливаем врага
    field[hight - 1][width - 1] = 1  # устанавливаем врага
    field[hight - 2][width - 1] = 1  # устанавливаем врага
    field[hight - 2][width - 2] = 1  # устанавливаем врага
    field[hight - 3][width - 1] = 1  # устанавливаем врага
    field[hight - 3][width - 2] = 1  # устанавливаем врага

def add_Dino(field):

    '''
...2345
-5 /#@\
-4 /#-/
-3 /#==
-2 /|\\
-1 /|\\

10: '/', 11: '#',  12: '@', 13: '\\', 14: '-', 15: '=', 16: '||'

Что нужно сделать:
 - автогенерацию динозёбра
 - автоматически создавать список с координатами каждой точки


    '''

    field[hight - 1][2] = 10  # устанавливаем Dino
    field[hight - 1][3] = 10
    field[hight - 1][4] = 16  # устанавливаем Dino
    field[hight - 1][5] = 16  # устанавливаем Dino

    # field[hight - 2][2] = 10  # устанавливаем Dino
    # field[hight - 2][3] = 10  # устанавливаем Dino
    # field[hight - 2][4] = 13  # устанавливаем Dino
    # field[hight - 2][5] = 13  # устанавливаем Dino
    #
    # field[hight - 3][2] = 10  # устанавливаем Dino
    # field[hight - 3][3] = 11  # устанавливаем Dino
    # field[hight - 3][4] = 15  # устанавливаем Dino
    # field[hight - 3][5] = 15  # устанавливаем Dino
    #
    # field[hight - 4][2] = 10  # устанавливаем Dino
    # field[hight - 4][3] = 11  # устанавливаем Dino
    # field[hight - 4][4] = 14  # устанавливаем Dino
    # field[hight - 4][5] = 10  # устанавливаем Dino
    #
    # field[hight - 5][2] = 10  # устанавливаем Dino
    # field[hight - 5][3] = 11  # устанавливаем Dino
    # field[hight - 5][4] = 12  # устанавливаем Dino
    # field[hight - 5][5] = 13  # устанавливаем Dino

    DIN0 = [
        [hight - 1, 2],
        [hight - 1, 3],
        [hight - 2, 2],
        [hight - 2, 3],

    ]

    return DINO


def gameEnd(fence, width):

    for i in range(6): print('')

    print('Game and'.center(width))

    for i in range(6): print('')
    print(fence)

    input('Нажми Enter для выхода')
    sys.exit()

DINO = add_Dino()

LET = add_let()

if __name__ == '__main__':
    loop(hight, width)






