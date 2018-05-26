import numpy as np
import cv2
from math import sqrt


# ein Objekt zur speicherung der Steigung und der Länge
class vector:
    def __init__(self, corner=0.0, lenght=0.0):
        self.corner = corner
        self.lenght = lenght


# nimmt die Vektoren auf errechnet daraus das Verkehrszeichen
class vectorobjekt:
    def __init__(self):

        self.maxlinks = 10
        self.angledeviation = 0.2

        self.numberoflinks = 0
        self.horizontal = [vector] * 10  # [maxlinks]
        self.count0 = 0
        self.vertical = [vector] * 10  # [maxlinks]
        self.count90 = 0
        self.degree45 = [vector] * 10  # [maxlinks]
        self.count45 = 0
        self.degree60 = [vector] * 10  # [maxlinks]
        self.count60 = 0
        self.other = [vector] * 10  # [maxlinks]
        self.countother = 0

    # funktion zur auswertung hinzufügen

    def reset(self):
        self.numberoflinks = 0
        self.count0 = 0
        self.count90 = 0
        self.count45 = 0
        self.count60 = 0
        self.countother = 0

    def printvo(self):  # aussgabe der werte
        print("\nNL: " + str(self.numberoflinks))
        print("C0: " + str(self.count0))
        print("C90: " + str(self.count90))
        print("C45: " + str(self.count45))
        print("C60: " + str(self.count60))
        print("Cother: " + str(self.countother))

    def processvector(self, vec):
        self.numberoflinks = self.numberoflinks + 1
        if (vec.corner == 0):
            self.horizontal[self.count0] = vec
            self.count0 = self.count0 + 1
        elif (vec.corner == 100):
            self.vertical[self.count90] = vec
            self.count90 = self.count90 + 1
        elif (vec.corner == 1):
            self.degree45[self.count45] = vec
            self.count45 = self.count45 + 1
        elif (vec.corner == 1.732):
            self.degree60[self.count60] = vec
            self.count60 = self.count60 + 1
        else:
            self.other[self.countother] = vec
            self.countother = self.countother + 1

    # berechnet aus den Vektoren das Verkehrszeichen
    def getshape(self):  # zu grob, verbessern

        #dreieck
        if (self.numberoflinks == 3):
            if (self.count60 == 2):
                if (self.count0 == 1):
                    return (3)  # dreieck
                if (((self.degree60[0].lenght * 1.1) > self.degree60[1].lenght) and (
                    (self.degree60[0].lenght * 0.9) < self.degree60[1].lenght)):
                    return (3)  # dreieck
            if (self.count60 == 1 and self.count0 == 1 and self.countother==1): #3 seiten und 2 gleich lang
                if (((self.degree60[0].lenght * 1.1) > self.other[0].lenght) and (
                            (self.degree60[0].lenght * 0.9) < self.other[0].lenght)):
                    return (3)  # dreieck
                if (((self.degree60[0].lenght * 1.1) > self.horizontal[0].lenght) and (
                            (self.degree60[0].lenght * 0.9) < self.horizontal[0].lenght)):
                    return (3)  # dreieck

        if(self.count60>=2 and self.count0 >= 1 and self.count90==0 and self.count45==0 and self.countother==0):
            return(3)
        if (self.count60 == 2 and self.count0 >= 1):
            if (((self.degree60[0].lenght * 1.1) > self.degree60[1].lenght) and (
                        (self.degree60[0].lenght * 0.9) < self.degree60[1].lenght)):
                return (3)  # dreieck

        #viereck
        if (self.numberoflinks == 4):
            if (self.count45 == 4):
                return (4)  # raute
            if (self.count90 == 2 and self.count0 == 2):
                return (4)  # viereck
        if ( self.count60 == 0 and self.count0 == 0 and self.count90 == 0 and self.count45 >= 4 and self.countother == 0):
            return (4)
        if (self.numberoflinks == 8 and self.count45 == 4):
                return (4)  # 4eck

       #achteck
        if (self.numberoflinks == 8):
            if (self.count45 == 4 and self.count0 == 2 and self.count90 == 2):
                return (8)  # 8eck

        return (0)  # nicht gefunden

    # Berechnet aus zwei koordinaten die (positive)steigung sowie die länge des Vektors
    def points2vector(self, p0, p1):
        x = p0[0] - p1[0]
        y = p0[1] - p1[1]
        lenght = sqrt((x) ** 2 + (y) ** 2)

        ###debug###
        # print("VEC: "+str(x)+" "+str(y))
        ###debug###

        if (y == 0):
            corner = 0.0  # vertikal
        elif (x == 0):
            corner = 100.0  # horizontal
        else:
            corner = y / x
        if (corner < 0):
            corner = corner * -1
        if (corner > 100):
            corner = 100
        if (corner < 0.1):  # wert anpassen
            corner = 0
        if ((corner > (1.732 - self.angledeviation)) and (
            corner < (1.732 + self.angledeviation))):  # 60Grad für Vorfahrtachten
            corner = 1.732
        if ((corner > (1 - self.angledeviation)) and (corner < (1 + self.angledeviation))):  # 45Grad
            corner = 1
        vec = vector(corner, lenght)
        self.processvector(vec)
        return ()
