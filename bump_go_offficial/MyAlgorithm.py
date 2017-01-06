import numpy as np
import math
import threading
import time
from datetime import datetime
from random import randint

time_cycle = 80
THOLD = 1000

class MyAlgorithm(threading.Thread):

    def __init__(self, laser, motors, pose3d, machine):
        self.laser = laser
        self.motors = motors
        self.pose3d = pose3d
        self.machine = machine
        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)

    def run (self):

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
        self.machine.deactivateAll()
        self.motors.setV(0)
        self.motors.sendVelocities()
        self.stop_event.set()

    def play (self):
        if self.is_alive():
            self.stop_event.clear()
            self.machine.setStateActive(0, True)

        else:
            self.machine.setStateActive(0, True)
            self.start()

    def kill (self):
        self.kill_event.set()

    def execute(self):
        #GETTING THE IMAGES
        #imageLeft = self.cameraL.getImage()
        #imageRight = self.cameraR.getImage()


        # Add your code here
        #print ("Running")
     

        '''if self.machine.isStateActive(0):
            print('Forward')
            time.sleep(2)
            self.machine.setTransitionActive(0,True)
            time.sleep(2)
            self.machine.setStateActive(1, True)
        elif self.machine.isStateActive(1):
            print('Backward')
            time.sleep(1)
            self.machine.setTransitionActive(1,True)
            time.sleep(1)
            self.machine.setStateActive(2, True)
        elif self.machine.isStateActive(2):
            print('Turn')
            time.sleep(2)
            self.machine.setTransitionActive(2,True)
            time.sleep(1)
            self.machine.setStateActive(0, True)
        '''

        #'''
        if self.machine.isStateActive(0):
            self.setV(0.1)
            if self.obstacle():
                self.machine.setTransitionActive(0,True)
                self.setV(0)
                time.sleep(2)
                self.machine.setStateActive(1, True)

        elif self.machine.isStateActive(1):
            while self.obstacle(500):
                self.setV(-0.1)
            self.machine.setTransitionActive(1,True)
            self.setV(0)
            time.sleep(2)
            self.machine.setStateActive(2, True)

        elif self.machine.isStateActive(2):
            angle = randint(-180,180)
            angle *= math.pi/180
            print(angle)
            while (abs(self.pose3d.getYaw()) < abs(angle)):
                self.setW(angle*0.1)
            self.machine.setTransitionActive(2,True)
            self.setW(0)
            time.sleep(1)
            self.machine.setStateActive(0, True)
        #'''
    
    def obstacle(self, margin=0):
        data = self.laser.getLaserData()
        for i in range(80,100):
            #if i >80 and i < 100:
                #print(data.distanceData[i])
            if data.distanceData[i] < THOLD+margin:
                return True
        return False

    def setV(self, v):
        self.motors.setV(v)
        self.motors.sendVelocities()
    
    def setW(self, w):
        self.motors.setW(w)
        self.motors.sendVelocities()

    

        #EXAMPLE OF HOW TO SEND INFORMATION TO THE ROBOT ACTUATORS
        #self.motors.setV(10)
        #self.motors.setW(5)
        #self.motors.sendVelocities()


        #SHOW THE FILTERED IMAGE ON THE GUI
        #self.setRightImageFiltered(imageRight)
        #self.setLeftImageFiltered(imageLeft)

