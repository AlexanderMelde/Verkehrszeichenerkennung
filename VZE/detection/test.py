from time import *

class mtime:
    def __init__(self,name):
        self.totaltime=0
        self.count=0
        self.name=name
        self.time=0
    def pstats(self):
        print(self.name,": ",(self.totaltime/self.count))

    def ptime(self):
        print(self.name," ",self.count,": ",self.time)

    def start(self):
        self.time=clock()

    def end(self):
        self.time=(clock())-self.time
        self.count=self.count+1
        self.totaltime=self.totaltime+self.time



