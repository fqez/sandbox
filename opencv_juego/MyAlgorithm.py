import threading
import time
from datetime import datetime
import signal
import sys
import cv2 as cv2
import numpy as np
import imutils
from pid import PID
import math


from parallelIce.cameraClient import CameraClient
from parallelIce.navDataClient import NavDataClient
from parallelIce.cmdvel import CMDVel
from parallelIce.extra import Extra
from parallelIce.pose3dClient import Pose3DClient

time_cycle = 80

ideal_height_wall_1 = 200
ideal_height_wall_3_4 = 200



filters = {"BLUE_HSV": [[104,200,0],[129,235,255]] , 
            "RED_HSV": [[171,214,0],[179,255,255]],
            "YELLOW_HSV": [[30,190,0],[30,205,135]] }

strats = ("STRAT_WALL_1", "STRAT_WALL_2","STRAT_WALL_3_4")
'''
    Strategies for avoiding walls according to the movement of each one, corresponding to:
        STRAT_WALL_1: Strategy to avoid the first wall (the blue one)
        STRAT_WALL_2: Strategy to avoid the second wall (the red one)
        STRAT_WALL_3: Strategy to avoid the third and fourth wall (the yellow ones)

    STRAT_WALL_1: Consist on the drone going to the left corner of the hangar, to be as far as possible of
                    the wall. Then, avoid the wall from there

                    TOP VIEW:

                            |                 |
                            |   #### <-wall   |
                            |                 |
                            | *  <-drone      |     
                            |_________________|
    
    STRAT_WALL_2: Consist no the drone to go almost to ground level, and avoid the wall when it's going up.

                    FRONT VIEW:

                            |  ##############################  
                            |  ##############################    <- wall
                            |  ##############################
                            |                                  
                            |              * <-drone          
                            |__________________________________  <- ground

    STRAT_WALL_3: Position the drone right on the middle of both wall centers, Then, when the distance between those
                    centers is maximum, move the drone forward.

                    FRONT VIEW:


                                ###########           ###########  
                      wall ->   #### @ ####           #### @ ####   <- wall
                                ###########           ###########  
                            |                                  
                            |                   * <-drone          
                            |__________________________________  <- ground



'''

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
        self.prev_area=0
        self.centers = []
        self.current_strat = strats[0]
        self.strat_complete = False

        self.pidX = PID(0, 1.75, 0.90, 0.1, 6)
        self.pidY = PID(0, 1.75, 0.90, 0.1, 6)
        self.pidZ = PID(0, 2.00, 1.00, 0.5, 6)
        self.pidRot = PID(0, 1.00, 0.75, 0.15, 12)    # (0, 1.75, 0.75, 0.15, 6)    # OK     

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

    def getImageFilteredC(self, image, filter):

        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        lower = np.array(filters[filter][0])
        upper = np.array(filters[filter][1])
        
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(image,image, mask= mask)

        return mask, res

    def stage_done (self, image, filter, size):

        mask1, res1 = self.getImageFilteredC(image, filter)
        _, contours1, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours1]

        if len(contours1) > 0:
            biggest_contours1 = sorted(contours1, key=cv2.contourArea)
            for c in biggest_contours1:
                xr,yr,wr,hr = cv2.boundingRect(c)
                cv2.rectangle(image,(xr,yr),(xr+wr,yr+hr),(0,255,0),2)
            #cv2.imshow("ALGO", image)
            print "--- " ,hr
            if hr >= size:
                return True
            else:
                return False

        
    def execute(self):

        if (self.first):
            print ("Z: ", self.pose.getPose3d().z)
            if self.pose.getPose3d().z < 2:
                self.extra.takeoff()
                self.cmdvel.sendCMDVel(0, 0, 0, 0, 0, 0)
            self.extra.toggleCam()
            self.first = not self.first
        
    	droneImage = self.camera.getImage().data
        self.centers = []
        
        if self.current_strat == strats[0]:
            cfilter = "BLUE_HSV"
        elif self.current_strat == strats[1]:
            cfilter = "RED_HSV"
        elif self.current_strat == strats[2]:
            cfilter = "YELLOW_HSV"
        mask, res = self.getImageFilteredC(droneImage, cfilter)
        kernel = np.ones((5,5), np.uint8)


        img_dilation = cv2.dilate(mask, kernel, iterations=1)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]

        #print len(contours)
        #print "-------------------------------"

        if len(contours) > 0:
            # Obtain the max area contour
            biggest_contours = sorted(contours, key=cv2.contourArea)[-2:]
            # get bounding box
            for cont in biggest_contours:
                x,y,w,h = cv2.boundingRect(cont)
            
                # draw bonding box
                cv2.rectangle(droneImage,(x,y),(x+w,y+h),(0,255,0),2)
                # get only bounding box image
                crop_img = droneImage[y:y+h, x:x+w]

            # Get center of mass to obtain the center of the object (wall)
            for c in contours:
            #c = contours[0]
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                else:
                    cX, cY = 0, 0
                #draw the center of mass
                cv2.circle(droneImage, (cX, cY), 2, (255, 255, 255), -1)
                cv2.putText(droneImage, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                self.centers.append(cX)

            # draw the image center line
            height, width, channels = droneImage.shape
            # cv2.line(droneImage, (x,0), (x, height), (255,255,255))
            cv2.line(droneImage, (width/2,0), (width/2, height), (255,255,255))
            # cv2.line(droneImage, (x+w,0), (x+w, height), (255,255,255))

            # cv2.imshow('Contour',droneImage)
            # cv2.imshow("Isolated wall", crop_img)
            # cv2.imshow('Mask',mask)       
            k = cv2.waitKey(5) & 0xFF


        if self.current_strat == "STRAT_WALL_1":

            if not self.strat_complete:
                # Apply the strat to the movement. In this case STRAT_WALL_1
                self.cmdvel.sendCMDVel(0.1,2,0,0,0,0)
                time.sleep(2)
                self.strat_complete = True
                print "STRAT_COMPLETE"

            if len(contours) < 1:
                # Wall not found, search it
                self.cmdvel.sendCMDVel(0,0,0,0,0,-0.2)
                None
            else:

                # if area < 5000:
                #     print "EVITO!!"
                #     self.cmdvel.sendCMDVel(0,3,0,0,0,0)
                #     time.sleep(2)                
                #s = "area"+str(c)
                #cv2.putText(droneImage, s,  (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                                
                # calculate the error for STRAT_WALL_1
                centerx = width/2.0
                # We want to look at the wall during the movement
                dist = -((cX-centerx)/centerx)
                # We have to maintain a security distance with the wall to avoid collision.
                depth = -((h-ideal_height_wall_1))

                # print dist
                #print h

                # calculate the speeds through PIDs
                velX = self.pidX.feedback(depth)
                velY = self.pidY.feedback(depth)
                velRot= self.pidRot.feedback(dist)
                #print velX, velY, velRot

                area = cv2.contourArea(c)
                # print area

                # if the wall is too close, we wait till it gets further away
                if area > self.prev_area:
                    # print (area/1000, ">", self.prev_area/1000, "   ACERCANDOSE")
                    self.cmdvel.sendCMDVel(0,0,0,0,0,velRot)
                    None
                else:
                    # print (area/1000, "<", self.prev_area/1000, "   ALEJANDOSE")
                    self.cmdvel.sendCMDVel(velX, velY ,0,0,0,velRot)
                    None
                #print "-------------------------------------"
                self.prev_area = area

                #print ("@@@@@@@@@@@@@@@@@@@@@@@@@@", self.pose.getPose3d().yaw)

                if self.stage_done(droneImage, "RED_HSV", 105):
                        self.current_strat = strats[1]
                        self.strat_complete = False

        
        elif self.current_strat == "STRAT_WALL_2":

            if not self.strat_complete:
                print "On second strat!"
                
                # Position the drone looking at front
                current_yaw = self.pose.getPose3d().yaw
                if not (current_yaw < 0.1 and current_yaw > -0.1):
                    print "turning..."
                    ideal_yaw = 0
                    error = -(current_yaw-ideal_yaw)
                    velRot = self.pidRot.feedback(error)
                    self.cmdvel.sendCMDVel(0,0,0,0,0,velRot)
                else:
                    # Apply the strat to the movement. In this case STRAT_WALL_2
                    ideal_alt = 0.7
                    current_alt =self.pose.getPose3d().z
                    error = -(current_alt - ideal_alt)
                    velZ = self.pidZ.feedback(error)
                    self.cmdvel.sendCMDVel(0,0,velZ,0,0,0)
                    if current_alt <= ideal_alt:
                        self.strat_complete = True
                        self.cmdvel.sendCMDVel(0,0,0,0,0,0)
                        print "STRAT_COMPLETE"
            else:
                if len(contours)<1:
                    self.cmdvel.sendCMDVel(0,0,0,0,0,0)     
                elif h < 100:
                    self.cmdvel.sendCMDVel(4,0,0,0,0,0)     
                    
                
                if self.stage_done(droneImage, "YELLOW_HSV", 140):
                        self.current_strat = strats[2]
                        self.strat_complete = False
        
        elif self.current_strat == "STRAT_WALL_3_4":

            ideal_alt = 2
            current_alt =self.pose.getPose3d().z
            error = -(current_alt - ideal_alt)
            velZ = self.pidZ.feedback(error)
            self.cmdvel.sendCMDVel(0,0,velZ,0,0,0)
            if current_alt >= 1.8 and current_alt <= 2.2:

                if len(self.centers) > 1:
                    c = self.centers[-2:]
                    #print c[0], c[1]

                    # calculate the error for STRAT_WALL_1
                    centerx = width/2.0
                    # # We want to look at the wall during the movement
                    cc = (c[0]+c[1])/2
                    cv2.line(droneImage, (cc,0), (cc, height), (0,0,255))
                    dist = -((cc-centerx)/centerx)
                    # # We have to maintain a security distance with the wall to avoid collision.
                    depth = -((h-ideal_height_wall_3_4))

                    # print dist
                    # print h

                    if h < ideal_height_wall_3_4 and h > 120:
                        velX = self.pidX.feedback(depth)
                        self.cmdvel.sendCMDVel(velX,0,0,0,0,0)
                    else:
                        if c[0] != 0 and c[1] != 0:
                            # calculate the speeds through PIDs
                            velY = self.pidY.feedback(dist)
                            velRot = self.pidRot.feedback(dist)
                            self.cmdvel.sendCMDVel(0,velY,0,0,0,velRot)
                            if abs(c[0]-c[1]) > 200:              
                                self.cmdvel.sendCMDVel(2,0,0,0,0,0)
                        elif c[0] == 0 or c[1] == 0:
                            # Too close?
                            self.cmdvel.sendCMDVel(-1,0,0,0,0,0)
                            None 
                        if h < 20:
                            self.cmdvel.sendCMDVel(2,0,0,0,0,0)


        # cv2.imshow('frame',droneImage)
        # cv2.imshow("cropped", crop_img)
        cv2.imshow('mask',mask)
        # cv2.imshow('res',res)
        #cv2.imshow('contour',im2)
    
        k = cv2.waitKey(5) & 0xFF
            







