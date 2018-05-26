import numpy as np
import cv2
from math import sqrt
from detection import contourclasses


# Errechnet die Eckigen schilder
class squaresigns:
    def __init__(self):

        self.divider = 1  # verkleinerungsfaktor

    def compute(self,frame):
        self.returnlist = []

        #self.resizedframe = cv2.resize(frame, (0, 0), fx=(1 / self.divider), fy=(1 / self.divider))  # verkleinern des Bildes

        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #cv2.imshow("1-gray", imgray)#debug

        #ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
        thresh = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 5)
        #cv2.imshow("2-treshold", thresh)#debug

        im2, self.contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.hierarchy = 0
        if hierarchy is not None:
            if len(hierarchy) > 0:
                self.hierarchy = hierarchy[0]

        ###debug###q
        #self.img = self.resizedframe.copy()
        ###debug###
        ###debug
        #cv2.drawContours(self.img, self.contours, -1, (0, 255, 0), 3)
        #cv2.imshow("3-countours", self.img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        self.process()

    def getlist(self):
        return self.returnlist


    def process(self):
        if len(self.contours) > 0:
            #debug
            #print(len(self.contours))
            self.processtree(0, 0)


    def processtree(self, nodeindexnumber, depth):
        # durchläuft effizient den Konturen Baum
        if depth < 5 and self.hierarchy is not None:  # sollte zu tief itteriert werden wird es abgebrochen
            while (nodeindexnumber != (-1)):  # weitere Konturen sind auf der selben ebene Vorhanden
                cnt = self.contours[nodeindexnumber]
                nodemetadata = self.hierarchy[nodeindexnumber]
                signvalue = self.procescontour(cnt)
                if signvalue == 0:  # keine Kontur wurde erkannt
                    if (nodemetadata[2] != (-1)):  # Es gibt eine Kind Kontur
                        self.processtree(nodemetadata[2], depth)
                nodeindexnumber = nodemetadata[0]


    def procescontour(self, cnt):
        vObjekt = contourclasses.vectorobjekt()
        counter = 0
        retvalue = 0

        cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        numberofedges = len(cnt)

        x, y, w, h = cv2.boundingRect(cnt)  # gibt die Koordinaten des Verkehszeichens
        sizeofcontour = w * h
        if ((sizeofcontour > 400) and ((w / h) < 1.3) and (
            (h / w) < 1.3) and (w<(1280/2)) and (h<(720/2))):  # kleine/unfoermige Konturen werden ignoriert(ggf anpassen)KOnturen welche das BIld umschließen auch

            if ((numberofedges < (vObjekt.maxlinks + 1)) and (
                numberofedges > 2)):  # Konturen welche zu viele/wenig ecken besitzen werden ignoriert
                vObjekt.reset()
                while (counter < (numberofedges - 1)):  # liest die Einzelnen Konturen in die Vektoren ein
                    cord0 = cnt[counter]
                    cord1 = cnt[counter + 1]
                    point0 = (cord0[0][0], cord0[0][1])
                    point1 = (cord1[0][0], cord1[0][1])
                    vObjekt.points2vector(point0, point1)
                    counter = counter + 1
                # contour zwischen punkt max und 0 berechnen
                cord0 = cnt[numberofedges - 1]
                cord1 = cnt[0]
                point0 = (cord0[0][0], cord0[0][1])
                point1 = (cord1[0][0], cord1[0][1])
                vObjekt.points2vector(point0, point1)

                retvalue = vObjekt.getshape()  # berechnet die Form der Kontur

                ###debug####
                # print(cnt)
                # print("retvalue")
                # print(retvalue)
                #img = self.img.copy()
                #cv2.drawContours(img, (cnt * 2), -1, (0, 255, 0), 3)
                #cv2.imshow("img", img)
                #cv2.waitKey(0)
                ####debug###

                if (retvalue > 0):
                    self.returnlist.append(
                        [(x * self.divider), (y * self.divider), (w * self.divider), (h * self.divider),
                         retvalue])  # koordinaten auf orginalgröße rechnen

        return (retvalue)

