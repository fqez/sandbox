import numpy as np
import threading
import time
from datetime import datetime
from random import randint

time_cycle = 80
THOLD = 2

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
     

        if self.machine.isStateActive(0):
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
        if self.machine.isStateActive(0):
            self.motors.setV(2)
            if self.obstacle():
                self.machine.setTransitionActive(0,True)
                self.motors.setV(0)
                time.sleep(1)
                self.machine.setStateActive(1, True)
        elif self.machine.isStateActive(1):
            while self.obstacle():
                self.motors.setV(-2)
            self.machine.setTransitionActive(1,True)
            time.sleep(1)
            self.machine.setStateActive(2, True)
        elif self.machine.isStateActive(2):
            angle = randint(-180,180)
            while (math.abs(self.pose3d.getYaw()) < math.abs(angle)):
                self.motors.setW(angle/10)
            self.machine.setTransitionActive(2,True)
            time.sleep(1)
            self.machine.setStateActive(0, True)
        '''
    
    def obstacle(self):
        data = self.laser.getLaserData()
        for i in data:
            if i < THOLD:
                return True
        return False

        

    

        #EXAMPLE OF HOW TO SEND INFORMATION TO THE ROBOT ACTUATORS
        #self.motors.setV(10)
        #self.motors.setW(5)
        #self.motors.sendVelocities()


        #SHOW THE FILTERED IMAGE ON THE GUI
        #self.setRightImageFiltered(imageRight)
        #self.setLeftImageFiltered(imageLeft)

