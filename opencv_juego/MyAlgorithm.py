import threading
import time
from datetime import datetime
import signal
import sys
import cv2 as cv2
import numpy as np
import imutils


from parallelIce.cameraClient import CameraClient
from parallelIce.navDataClient import NavDataClient
from parallelIce.cmdvel import CMDVel
from parallelIce.extra import Extra
from parallelIce.pose3dClient import Pose3DClient

time_cycle = 80

def nothing(x):
	pass

class MyAlgorithm(threading.Thread):

    def __init__(self, camera, navdata, pose, cmdvel, extra):
        self.camera = camera
        self.navdata = navdata
        self.pose = pose
        self.cmdvel = cmdvel
        self.extra = extra

        self.image = None
        self.first = True 

        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)

    def setImageFiltered(self, image):
        self.lock.acquire()
        self.image=image
        self.lock.release()

    def getImageFiltered(self):
        self.lock.acquire()
        tempImage=self.image
        self.lock.release()
        return tempImage

    def run (self):

        self.stop_event.clear()

        while (not self.kill_event.is_set()):

            start_time = datetime.now()

            if not self.stop_event.is_set():
                self.execute()

            finish_Time = datetime.now()

            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.stop_event.set()

    def play (self):
        if self.is_alive():
            self.stop_event.clear()
        else:
            self.start()

    def kill (self):
        self.kill_event.set()

    def execute(self):
        if (self.first):
            self.cmdvel.sendCMDVel(0, 0, 0, 0, 0, 0)
            self.extra.takeoff()
            self.cmdvel.sendCMDVel(0.2, 2, 0, 0, 0, 0)
            time.sleep(2)
            self.first = not self.first

    	droneImage = self.camera.getImage().data
	
        hsv = cv2.cvtColor(droneImage, cv2.COLOR_RGB2HSV)
        lower_blue = np.array([104,200,0])
        upper_blue = np.array([129,235,255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        res = cv2.bitwise_and(droneImage,droneImage, mask= mask)
        self.setImageFiltered(res)

        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(droneImage, contours, -1, (0,255,0), 1)

        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        x,y,w,h = cv2.boundingRect(biggest_contour)
        cv2.rectangle(droneImage,(x,y),(x+w,y+h),(0,255,0),2)
        crop_img = droneImage[y:y+h, x:x+w]
        #cv2.circle(droneImage, (w/2,h/2), 10, (255,0,0), thickness=3, lineType=8, shift=0)

        c = contours[0]
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        #cv2.circle(droneImage, (cX, cY), 2, (255, 255, 255), -1)

        area = cv2.contourArea(c)
        
        #s = "area"+str(c)
        #cv2.putText(droneImage, s,  (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        

        height, width, channels = droneImage.shape
        #cv2.line(droneImage, (x,0), (x, height), (255,255,255))
        #cv2.line(droneImage, (width/2,0), (width/2, height), (255,255,255))
        #cv2.line(droneImage, (x+w,0), (x+w, height), (255,255,255))
        #cv2.putText(droneImage, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if cX == 0:
            self.cmdvel.sendCMDVel(0, 0, 0, 0, 0, 0)
        elif cX > width/2:
            self.cmdvel.sendCMDVel(0, 0, 0, 0, 0, -0.3)
        elif cX < width/2:
            self.cmdvel.sendCMDVel(0, 0, 0, 0, 0, 0.3)
        
        








        cv2.imshow('frame',droneImage)
        cv2.imshow("cropped", crop_img)
        # cv2.imshow('mask',mask)
        # cv2.imshow('res',res)
        # cv2.imshow('contour',im2)
    
        k = cv2.waitKey(5) & 0xFF
            







