import msvcrt
import os
import time
import sys


def clear():
    os.system('CLS')


hight = 20  # количество строк
width = 100 # шарина, т.е. сколько символов в строке

''' Устанавливаем размер игрового поля'''
os.system(f"mode con cols={width} lines={hight+1}")




# Цикл
def loop(hight, width):

    hight_f = 30
    width_f = 17

    # Поле
    field = [[ 0 * j for j in range(width)] for i in range(hight)]


    field[hight - 1][width - 2] = 1     # устанавливаем врага
    field[hight - 1][width - 1] = 1  # устанавливаем врага
    field[hight - 2][width - 1] = 1  # устанавливаем врага
    field[hight - 2][width - 2] = 1  # устанавливаем врага
    field[hight - 3][width - 1] = 1  # устанавливаем врага
    field[hight - 3][width - 2] = 1  # устанавливаем врага



    ''' Рисуем решёлки'''
    fence = '#' * width

    line = 0 # индекс строки
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


            move(field, 19, 49)

            # снова заборчик
            print(fence)

            # счётчи количества итераций
            iter += 1

            # Функция которая ожидает ввода
            text = 'Для управления введи тречолку вверх или вниз'
            if timed_input(text) == 'up':
                # print('Eeeeeeee')
                time.sleep(5)

            # Для очистки терминала
            clear()
            print(fence)



# Функция которая ожидает ввод от пользователя определённое время
# если пользователь ничего не ввёл за указанное время
# то ничего не делает
def timed_input(caption, timeout=0.5):
    def echo(c):

        sys.stdout.flush()

    start = time.monotonic()
    while time.monotonic() - start < timeout:
        if msvcrt.kbhit():
            c = msvcrt.getwch()
            if ord(c) == 32:
                echo(c)
                return 'up'



def move(field, pos_x, pos_y):

    border_x = 0  # ограничение по х
    border_y = 4  # ограничение по у


    for y in range(0, len(field)):
        tmp = []

        for x in range(0, len(field[y])):
            if field[y][x] == 0:
                tmp.append('')


            elif field[y][x] == 1:
                tmp.append('█')
                field[y][x] = 0
                field[y][x-1] = 1

        print(*tmp)





def gameEnd(fence, width):

    for i in range(6): print('')

    print('Game and'.center(width))

    for i in range(6): print('')
    print(fence)

    input('Нажми Enter для выхода')
    sys.exit()


if __name__ == '__main__':
    loop(hight, width)






