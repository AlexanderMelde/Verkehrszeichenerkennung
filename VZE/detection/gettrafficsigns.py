import numpy as np
import cv2
import threading
#from threading import Thread
from detection import squaresigns
from detection import circledetection
from detection import helpers
from detection import test


circle = test.mtime("circle")
square = test.mtime("square")
complete =test.mtime("complete")

# returns coordinates of detected signs
# def returncoordinatesofsign(frame):
def gettrafficsigns(frame):

    #complete.start()
    #circle.start()
    #square.start()

    ciobjekt=circledetection.circle()
    tci=threading.Thread(target = ciobjekt.circledetection,args = (frame, ))
    tci.start()

    sqobjekt=squaresigns.squaresigns()
    tsq=threading.Thread(target = sqobjekt.compute,args = (frame, ))
    tsq.start()

    tci.join()
    #tsq.join()

    circlevalue = ciobjekt.getcirclelist()
    squarevalue =sqobjekt.getlist()

    #circle.end()
    #square.end()

    returnlist = helpers.deletedoubles(circlevalue, squarevalue)

    #complete.end()

    #complete.ptime()
    #circle.ptime()
    #square.ptime()
    #complete.pstats()
    #circle.pstats()
    #square.pstats()


    return returnlist


'''
cnt=0   
while cnt<8:
	#test mit einzelnen bildern
	string1="schilder/vkz"+str(cnt)+".png"
	img = cv2.imread(string1)
	gettrafficsigns(img)
	#cv2.waitKey(0)
	cnt=cnt+1

string1="C:\\Users\Administrator\\Documents\\semester5\\Studienarbeit\\OneDrive\\Shared\\testvideos\\aaa1"
img = cv2.imread(string1)
gettrafficsigns(img)
'''