

def move(field, status):

    y = 0
    x = 0

    for string in field:

        for colum in string:


            if colum == 1:
                if colum == 1 and x != 0:
                    field[y][x - 1] = 1
                    field[y][x] = 0

                elif colum == 1 and x == 0:
                    field[y][x] = 0



            elif colum == 2:
                if status == "run":
                    pass

                elif status == "up":
                    if colum == 1 and y != 0:
                        field[y + 1][x] = 1
                        field[y][x] = 0

                    elif colum == 1 and y == 0:
                        field[y][x] = 0


                x += 1
            y += 1
