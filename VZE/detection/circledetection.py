import cv2
import math
import numpy as np
from detection import filtercolor
from detection import helpers



class circle:
    def __init__(self):
        self.returnlist =[]

    def getcirclelist(self):
        return(self.returnlist)

    def circledetection(self,frame):

        frame = filtercolor.filtercolor(frame)
        # cv2.imshow("test", framefiltert)
        # cv2.waitKey(0)


        mask = cv2.Canny(frame, 150, 300)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        circles = cv2.HoughCircles(mask,  # input
                                   cv2.HOUGH_GRADIENT,  # methode
                                   1,  # The inverse ratio of resolution(1=original größe, 2=halbierte größe
                                   40,  # min.distanz zwischen den kreismittelpunkten
                                   param1=200,  # obere Schwelle des Kantenalgo.
                                   param2=60,  # Schwellwert zur mittelpunkt detection #vlt auf 60 erhöhen
                                   minRadius=10,  # min radius(0=default)
                                   maxRadius=100)  # max radius(0=default)

        oldx = 0.0
        oldy = 0.0
        oldradius = 0.0
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])  # center des kreises y/x
                radius = i[2]
                # reg=Bildauschnitt des erkannten schilds(radius+10% toleranz)
                distance = math.sqrt((((oldx - (int)(i[0]))) ** 2) + (((oldy - (int)(i[1]))) ** 2))
                if (oldradius < distance):
                    oldx = i[0]
                    oldy = i[1]
                    oldradius = radius
                    x1 = i[0] - (int)(radius * 1.3)
                    if (x1 < 0):
                        x1 = 0
                    x2 = i[0] + (int)(radius * 1.3)
                    if (x2 > frame.shape[1]):
                        x2 = frame.shape[1] - 1
                    y1 = i[1] - (int)(radius * 1.3)
                    if (y1 < 0):
                        y1 = 0
                    y2 = i[1] + (int)(radius * 1.3)
                    if (y2 > frame.shape[0]):
                        y2 = frame.shape[0] - 1

                    reg = frame[y1:y2, x1:x2]
                    # beugt error mit leeren Bildern vor
                    if (reg.shape[0] > 0 and reg.shape[1] > 0):
                        #cv2.imshow("bild", reg)
                        #cv2.waitKey(0)
                        self.returnlist.append([x1, y1, x2 - x1, y2 - y1, 0])

        self.returnlist = helpers.deletedoubles(self.returnlist, self.returnlist)  # filtert manche Bäume


