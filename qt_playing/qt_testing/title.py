from __future__ import division

import sys
import time
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtSvg

WIDTH = 1750
HEIGHT = 900

# WIDTH = 800
# HEIGHT = 600

class AnimatedLabel(QLabel):

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

    def mousePressEvent(self, event):
        self.clicked.emit()
        self.end_animation()

    def enterEvent(self, event):
        self.ga.stop()
        self.start_animation(self.FAST_DURATION)
        
    def leaveEvent(self, event):
        self.ga.stop()
        self.start_animation(self.SLOW_DURATION)

    def end_animation(self):
        self.ga.stop()
        self.hide()

class TitleWindow(QWidget):
    updGUI = pyqtSignal()
    switch_window = pyqtSignal()

    def __init__(self, parent = None):
        super(QWidget, self).__init__(parent)
        self.updGUI.connect(self.update_gui)
        self.parent = parent
        self.initUI()
    
    def initUI(self):

        main_layout = QVBoxLayout()
        self.setStyleSheet('background-color: rgb(51,51,51)')
        self.setLayout(main_layout)

        mid = self.height() // 2
        third = self.height() // 3
        
        img = QImage('/home/fran/github/BehaviorSuite/ggui/assets/logo.svg')
        pmap = QPixmap.fromImage(img)
        self.frame_above = QLabel(self)
        self.frame_above.setGeometry(0, 0, self.width(), self.height())
        self.frame_above.setPixmap(pmap)
        self.frame_above.setAlignment(Qt.AlignCenter)

        font = QFont('Arial', 20)
        self.clk_label = AnimatedLabel(self)    # no se si este mejor o el label normal
        self.clk_label.setFont(font)
        self.clk_label.setText("Click to start")
        self.clk_label.setAlignment(Qt.AlignCenter)
        self.clk_label.clicked.connect(self.do_animation)   
        self.clk_label.setStyleSheet('color: yellow')     
   
        font = QFont('Techno Capture', 58)
        self.frame_below = QLabel(self)
        self.frame_below.setGeometry(0, mid, self.width(), self.height())
        self.frame_below.setFont(font)
        self.frame_below.setText("Welcome to Behavior Suite")
        self.frame_below.setAlignment(Qt.AlignCenter)
        self.frame_below.setStyleSheet('color: white')

        main_layout.addWidget(self.frame_above) 
        main_layout.addWidget(self.frame_below)
        main_layout.addWidget(self.clk_label)
                
        self.show()

    def do_animation(self):

        self.anim_above = QPropertyAnimation(self.frame_above, b'pos')
        self.anim_above.setStartValue(self.frame_above.pos())
        self.anim_above.setEndValue(QPoint(0, -600))
        self.anim_above.setDuration(2000)

        self.anim_below = QPropertyAnimation(self.frame_below, b'pos')
        self.anim_below.setStartValue(self.frame_below.pos())
        self.anim_below.setEndValue(QPoint(self.frame_below.x(), self.frame_below.y() + 600))
        self.anim_below.setDuration(2000)

        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim_above)
        self.anim_group.addAnimation(self.anim_below)

        self.anim_group.start()
        self.anim_group.finished.connect(self.animation_finished)

    def animation_finished(self):
        self.switch_window.emit()
        
    
    def update_gui(self):
        # self.update()
        # print('Size {} x {} px'.format(self.width(), self.height()))
        pass
