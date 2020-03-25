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

class WorldSelection(QWidget):
    updGUI = pyqtSignal()
    switch_window = pyqtSignal()

    def __init__(self, parent = None):
        super(WorldSelection, self).__init__(parent)
        self.updGUI.connect(self.update_gui)
        self.parent = parent
        self.initUI()
    
    def initUI(self):

        main_layout = QVBoxLayout()
        self.setStyleSheet('background-color: rgb(51,51,51)')
        self.setLayout(main_layout)

        logo = Logo()
        main_layout.addWidget(logo)

        self.world_layout = QHBoxLayout()
        f1_frame = self.create_robot_frame('f1')

        lbl = QLabel('ASDFASDF')

        self.world_layout.addWidget(f1_frame, 0)
        self.world_layout.addWidget(lbl, 1)

        font = QFont('Arial', 30)
        lbl = ClickableLabel(self)
        lbl.setFont(font)
        lbl.setText("Select your world")
        lbl.setFixedHeight(100)
        lbl.setAlignment(Qt.AlignCenter) 
        lbl.setStyleSheet('color: yellow')     

        main_layout.addLayout(self.robot_layout)
        main_layout.addWidget(lbl)

    def create_robot_frame(self, robot_type):

        v3d = View3D(robot_type, self)
        frame = QFrame(v3d)
        r1_layout = QVBoxLayout()        
        r1_layout.addWidget(v3d)
        frame.setLayout(r1_layout)

        return frame

    def update_gui(self):
        # self.update()
        # print('Size {} x {} px'.format(self.width(), self.height()))
        pass
