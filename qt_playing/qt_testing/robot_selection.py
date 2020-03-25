from __future__ import division

import sys
import time
import os
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtSvg

from models3d import *
from logo import Logo


from threadGUI import ThreadGUI
import threading

# from contextlib import contextmanager

# @contextmanager
# def suppress_stdout():
#     with open(os.devnull, "w") as devnull:
#         old_stdout = sys.stdout
#         sys.stdout = devnull
#         try:  
#             yield
#         finally:
#             sys.stdout = old_stdout

class ClickableLabel(QLabel):

    clicked = pyqtSignal()

    in_label = False
    SLOW_DURATION = 1500
    FAST_DURATION = 500

    def __init__(self, parent = None):
        QLabel.__init__(self, parent)
        self.start_animation(self.SLOW_DURATION)
        
    def start_animation(self, duration):
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)

        self.animation1 = QPropertyAnimation(self.effect, b"opacity")
        self.animation1.setDuration(duration)
        self.animation1.setStartValue(1)
        self.animation1.setEndValue(0)

        self.animation2 = QPropertyAnimation(self.effect, b"opacity")
        self.animation2.setDuration(duration)
        self.animation2.setStartValue(0)
        self.animation2.setEndValue(1)

        self.ga = QSequentialAnimationGroup()
        self.ga.addAnimation(self.animation1)
        self.ga.addAnimation(self.animation2)
        self.ga.setLoopCount(-1)
        self.ga.start()

    def enterEvent(self, event):
        self.ga.stop()
        self.start_animation(self.FAST_DURATION)
        
    def leaveEvent(self, event):
        self.ga.stop()
        self.start_animation(self.SLOW_DURATION)

    def end_animation(self):
        self.ga.stop()
        self.hide()

class CustomQFrame(QFrame):

    def __init__(self, scene, parent=None, flags=Qt.WindowFlags()):
        super(CustomQFrame, self).__init__(parent=parent, flags=flags)
        self.scene = scene
        self.parent = parent
        
    def enterEvent(self, event):
        self.setStyleSheet('QFrame {background-color: rgba(255,255,255,0.3); border: 2px solid white; }')
        self.scene.view.defaultFrameGraph().setClearColor(QColor(255,255,255))

    def leaveEvent(self, event):
        self.setStyleSheet('QFrame {background-color: rgb(51,51,51); border: 0px solid white; }')
        self.scene.view.defaultFrameGraph().setClearColor(QColor(51,51,51))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('mouse pressed in', self.scene.robot_type)
            self.scene.set_animation_speed(1000)
            self.scene.start_animation_with_duration(2000)
           

class RobotSelection(QWidget):
    updGUI = pyqtSignal()
    switch_window = pyqtSignal()

    def __init__(self, parent = None):
        super(RobotSelection, self).__init__(parent)
        self.updGUI.connect(self.update_gui)
        self.parent = parent
        self.initUI()
    
    def initUI(self):

        main_layout = QVBoxLayout()
        self.setStyleSheet('background-color: rgb(51,51,51)')
        self.setLayout(main_layout)

        logo = Logo()
        main_layout.addWidget(logo)

        self.robot_layout = QGridLayout()
        f1_frame = self.create_robot_frame('f1', 'Formula 1')
        drone_frame = self.create_robot_frame('drone', 'Drone')
        roomba_frame = self.create_robot_frame('roomba', 'Roomba')
        car_frame = self.create_robot_frame('car', 'Car')
        turtle_frame = self.create_robot_frame('turtlebot', 'Turtlebot')
        pepper_frame = self.create_robot_frame('pepper', 'Pepper - Comming soon')

        self.robot_layout.addWidget(f1_frame, 0, 0)
        self.robot_layout.addWidget(drone_frame, 0, 1)
        self.robot_layout.addWidget(roomba_frame, 0, 2)
        self.robot_layout.addWidget(car_frame, 1, 0)
        self.robot_layout.addWidget(turtle_frame, 1, 1)
        self.robot_layout.addWidget(pepper_frame, 1, 2)

        font = QFont('Arial', 30)
        lbl = ClickableLabel(self)
        lbl.setFont(font)
        lbl.setText("Select your robot")
        lbl.setFixedHeight(100)
        lbl.setAlignment(Qt.AlignCenter) 
        lbl.setStyleSheet('color: yellow')     

        main_layout.addLayout(self.robot_layout)
        main_layout.addWidget(lbl)

    def createLabel(self, text, font):
        label = QLabel(self)
        label.setFont(font)
        label.setText(text)
        label.setFixedHeight(40)
        label.setAlignment(Qt.AlignCenter) 
        label.setStyleSheet('background-color: rgba(0,0,0,0);color: white; border: 0px solid black; ')
        return label

    def create_robot_frame(self, robot_type, robot_name):

        v3d = View3D(robot_type, self)
        frame = CustomQFrame(v3d, self)
        r1_layout = QVBoxLayout()        
        font = QFont('Arial', 15)
        lr = self.createLabel(robot_name, font) 

        r1_layout.addWidget(v3d)
        r1_layout.addWidget(lr)
        frame.setLayout(r1_layout)

        return frame

    def emit_and_destroy(self):
        delete_widgets_from(self.robot_layout)
        self.switch_window.emit()


    def update_gui(self):
        # self.update()
        # print('Size {} x {} px'.format(self.width(), self.height()))
        pass

def delete_widgets_from(layout):
    """ memory secure. """
    for i in reversed(range(layout.count())): 
        widgetToRemove = layout.itemAt(i).widget()
        # remove it from the layout list
        layout.removeWidget(widgetToRemove)
        # remove it from the gui
        widgetToRemove.setParent(None)