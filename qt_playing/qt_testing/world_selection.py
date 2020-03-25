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


class QCustomQWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        font = QFont('Arial', 30)
        self.textUpQLabel    = QLabel()
        self.textUpQLabel.setFont(font)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.allQHBoxLayout  = QHBoxLayout()
        self.iconQLabel      = QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(255, 255, 255);
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))

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

        v3d = View3D('f1', self)
        frame = QFrame(self)
        self.r1_layout = QHBoxLayout()
        
        
        myQListWidget = QListWidget()
        myQListWidget.setStyleSheet("border: 0px;")
        myQListWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        myQListWidget.verticalScrollBar().setSingleStep(10)
        myQListWidget.setMaximumWidth(800)
        for index, icon in [
            ('No.1',  'icon.png'),
            ('No.2',  'icon.png'),
            ('No.3',  'icon.png'),
            ('No.2',  'icon.png'),
            ('No.3',  'icon.png'),
            ('No.2',  'icon.png'),
            ('No.3',  'icon.png')]:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setIcon(':/assets/logo_100.svg')
            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(QSize(200, 200))
            # Add QListWidgetItem into QListWidget
            myQListWidget.addItem(myQListWidgetItem)
            myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)     

        self.r1_layout.addWidget(v3d)
        self.r1_layout.addWidget(myQListWidget)
        
        frame.setLayout(self.r1_layout)   

        font = QFont('Arial', 30)
        lbl = ClickableLabel(self)
        lbl.setFont(font)
        lbl.setText("Select your world")
        lbl.setFixedHeight(100)
        lbl.setAlignment(Qt.AlignCenter) 
        lbl.setStyleSheet('color: yellow')     

        main_layout.addWidget(logo)
        main_layout.addWidget(frame)
        main_layout.addWidget(lbl)

    def update_gui(self):
        # self.update()
        # print('Size {} x {} px'.format(self.width(), self.height()))
        pass
