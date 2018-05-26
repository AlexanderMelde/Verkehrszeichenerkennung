from classes.Pos import Pos
import cv2

class Sign:
    pos = None  # dictionary of form framenr:(x,y,w,h)

    edgecount = None
    rotation = None
    color = None

    labels = None # dictionary of form framenr:("id",prob)

    tracker = None

    def __init__(self, framenr, x, y, w, h, edgecount=None, rotation=None):
        self.pos = {framenr: Pos(x, y, w, h)}
        self.edgecount = edgecount
        self.rotation = rotation
        self.labels = {}

    def getLabel(self):  # returns the most recent label
        if len(self.labels) == 0:
            return None
        return[self.labels[max(self.labels.keys())]][0]

    def addLabel(self, framenr, label):
        self.labels[framenr] = label
        return label

    def addPos(self, framenr, x, y, w, h):
        self.pos[framenr] = Pos(x, y, w, h)

    def sameSignPosition(self, x, y, w, h, edgecount=None):
        #checks if the parameter x,y,w,h are very close (10%) to the signs last position
        lastPos = self.pos[max(self.pos.keys())]
        # check if inside +100% box
        scale = 1
        bigPos = Pos(int(lastPos.x - lastPos.w * scale),
                     int(lastPos.y - lastPos.h * scale),
                     int(lastPos.w * (1 + 2 * scale)),
                     int(lastPos.h * (1 + 2 * scale)))

        # return false if outside bigPos box
        if x < bigPos.x or y < bigPos.y or x+w > bigPos.x+bigPos.w or y+h > bigPos.y+bigPos.h:
            return False

        # check if approximately same size (if difference in area is max. 100% of the old size)
        if abs(w*h - lastPos.w * lastPos.h) > lastPos.w * lastPos.h / scale*100:
            return False

        # check if number of edges matches
        if edgecount is not (None or self.edgecount):
            return False

        return True

    def addTracker(self):
        print(cv2.__version__)
        self.tracker = cv2.TrackerKCF_create()
        return self.tracker

    def __str__(self):
        # defines the string representation of this Sign
        lastPos = self.pos[max(self.pos.keys())]
        allPos = ""
        for framenr, pos in self.pos.items():
            allPos += str(framenr)+":"+str(pos)+","
        return "Sign(pos{"+allPos+"}edges"+str(self.edgecount)+"rot"+str(self.rotation)+")"
