class Pos:
    x = None
    y = None
    w = None
    h = None

    def __init__(self, x, y, w, h):
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

    def __str__(self):
        # defines the string representation of this Pos
        return "x"+str(self.x)+"y"+str(self.y)+"h"+str(self.h)+"w"+str(self.w)
