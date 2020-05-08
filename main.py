import subprocess
import platform
import msvcrt
import os
import time
import sys

from field import field

def clear():
    os.system('CLS')


''' Устанавливаем размер игрового поля'''
os.system("mode con cols=50 lines=16")


def loop():
    ''' Рисуем решёлки'''
    fence = '#' * 50

    game = True
    line = 0 # индекс строки
    colum = 0 # индекс столба
    iter = 0 # Считаем циклы

    # Главный циклы
    while game:

        # тут я ввёл ограничители по строкам
        line = 5
        # огранчение по количеству символов
        colum += 1

        # пока что сделал ограничение на количество циклов
        if iter == 50:
            game = False
            print(fence)

            print('Game And')

            print(fence)

            input()

        else:
            # Рисую заборчик
            print(fence)

            # функция рабочего поля
            gameField(line, colum)

            # снова заборчик
            print(fence)

            # счётчи количества итераций
            iter += 1

            # Функция которая ожидает ввода
            timed_input('Для управления введи тречолку вверх или вниз')

            # Для очистки терминала
            clear()
        print(fence)

# Функция отвечающая за отображение игровой зоны
def gameField(l, c):

    hight = 13
    len = 50

    # Ограничение что бы не выйти а предел
    if c <= 49:
        field[l][c] = 0
        field[l][c-1] = ''

    # Построчно рисуем игровое поле
    for lines in range(0, hight):
        temp_line = []

        for i in range(0, len):
            temp_line.append((field[lines][i]))

        print(*temp_line)

# Функция которая ожидает ввод от пользователя определённое время
# если пользователь ничего не ввёл за указанное время
# то ничего не делает
def timed_input(caption, timeout=0.1):
    def echo(c):
        sys.stdout.write(c)
        sys.stdout.flush()

    echo(caption)

    _input = []
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        if msvcrt.kbhit():
            c = msvcrt.getwch()
            if ord(c) == 13:
                echo('\r\n')
                break
            _input.append(c)
            echo(c)

    if _input:
        return ''.join(_input)

if __name__ == '__main__':
    loop()






