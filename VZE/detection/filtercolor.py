import cv2
import math
import numpy as np

'''#s5-mini
lower_red = (0, 40, 100)
upper_red = (13, 255, 255)#70, 125)#für bilder s&v auf 255, 255)#
lower_highred=(173, 100, 80)
upper_highred=(180, 175, 160)
lower_yellow = (22, 140, 50)
upper_yellow = (30, 255, 255)
lower_lightblue = (85,50,50)
upper_lightblue = (95,255,255)
lower_blue = (110,50,40)
upper_blue = (130,255,255)
'''

# gopro
lower_red = (0, 120, 84)  # (0, 40, 100) S->auf130??
upper_red = (10, 255, 255)  # 70, 125)#für bilder s&v auf 255, 255)#
lower_highred = (173, 120, 75)  # (173, 100, 80)
upper_highred = (180, 190, 160)  # (180, 175, 160)

lower_yellow = (17, 120, 110)  # (20, 140, 50)
upper_yellow = (30, 255, 255)
# lower_lightblue = (85,50,50)
# upper_lightblue = (95,255,255)
lower_blue = (95, 120, 40)  # (110,50,40)
upper_blue = (130, 255, 255)


def filtercolor(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.medianBlur(hsv, 5)  # reduce noise
    #cv2.imshow("hsv", hsv) #debug
    # cv2.waitKey(0)
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask = cv2.add(mask, cv2.inRange(hsv, lower_highred, upper_highred))
    mask = cv2.add(mask, cv2.inRange(hsv, lower_yellow, upper_yellow))
    # mask = cv2.add(mask,cv2.inRange(hsv, lower_lightblue, upper_lightblue))
    mask = cv2.add(mask, cv2.inRange(hsv, lower_blue, upper_blue))
    #cv2.imshow("0-mask", mask)  # debug
    res = cv2.bitwise_and(frame, frame, mask=mask)
    #cv2.imshow("1-res", res)  # debug
    return (res)#testweiße nur die maske zurückgegeben(pro performance)
