import cv2
import math
import numpy as np


def deletedoubles(circlevalue, squarevalue):
    returnlist = []
    # delete squares in circles
    if not circlevalue:
        return (squarevalue)

    if not squarevalue:
        return (circlevalue)

    for circle in circlevalue:  # liegt ein Kreis in keinem Viereck füge in hinzu

        c_radian = circle[2] / 2
        c_0 = circle[0] + c_radian
        c_1 = circle[1] + c_radian
        count = 0
        for square in squarevalue:
            s_0 = square[0] + (square[2] / 2)
            s_1 = square[1] + (square[3] / 2)
            s_radian = (square[2] + square[3]) / 2
            distance = math.sqrt(((c_0 - s_0) ** 2) + ((c_1 - s_1) ** 2))
            if (distance < s_radian and distance !=0):
                count = count + 1
        if (count == 0):
            returnlist.append(circle)

    for square in squarevalue:  # wie oben nur anderst herum
        s_radian = (square[2] + square[3]) / 2
        s_0 = square[0] + (square[2] / 2)
        s_1 = square[1] + (square[3] / 2)

        count = 0
        for circle in returnlist:
            c_0 = circle[0] + c_radian
            c_1 = circle[1] + c_radian
            c_radian = circle[2] / 2
            distance = math.sqrt(((c_0 - s_0) ** 2) + ((c_1 - s_1) ** 2))

            if (distance < c_radian):
                count = count + 1
        if (count == 0):
            returnlist.append(square)
    return (returnlist)
