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

WIDTH = 1750
HEIGHT = 900

# WIDTH = 800
# HEIGHT = 600

from contextlib import contextmanager

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

class VLine(QFrame):
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)

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
        print('ending animation')
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
        self.setStyleSheet('background-color: rgb(51,51,51')
        self.scene.view.defaultFrameGraph().setClearColor(QColor(51,51,51))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('mouse pressed in', self.scene.robot_type)
            self.scene.stop_animation()
            self.scene.set_animation_speed(1000)
            self.scene.start_animation()
            for i in reversed(range(self.parent.robot_layout.count())): 
                widgetToRemove = self.parent.robot_layout.itemAt(i).widget()
                # remove it from the layout list
                self.parent.robot_layout.removeWidget(widgetToRemove)
                # remove it from the gui
                widgetToRemove.setParent(None)
            # for i in reversed(range(self.parent.robot_layout.count()-1)): 
                # self.parent.robot_layout.itemAt(i).widget().setParent(None)

                


class ExampleWindow(QMainWindow):
    updGUI = pyqtSignal()

    def __init__(self):
        super(ExampleWindow, self).__init__()
        self.windowsize = QSize(WIDTH,HEIGHT)
        self.updGUI.connect(self.update_gui)
        self.counter = 0
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(self.windowsize)
        self.init_statusbar()

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setStyleSheet('background-color: rgb(51,51,51)')
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        logo = Logo()
        main_layout.addWidget(logo)

        self.robot_layout = QGridLayout()
        f1_frame = self.create_robot_frame('f1', 'Formula 1')
        drone_frame = self.create_robot_frame('drone', 'Drone')
        roomba_frame = self.create_robot_frame('roomba', 'Roomba')
        car_frame = self.create_robot_frame('car', 'Car')
        turtle_frame = self.create_robot_frame('turtlebot', 'Turtlebot')
        pepper_frame = self.create_robot_frame('pepper', 'Pepper - Comming soon')
        # v3d.show()
        self.robot_layout.addWidget(f1_frame, 0, 0)
        self.robot_layout.addWidget(drone_frame, 0, 1)
        self.robot_layout.addWidget(roomba_frame, 0, 2)
        self.robot_layout.addWidget(car_frame, 1, 0)
        self.robot_layout.addWidget(turtle_frame, 1, 1)
        self.robot_layout.addWidget(pepper_frame, 1, 2)

        

        font = QFont('Arial', 30)
        lbl = QLabel(self)
        lbl.setFont(font)
        lbl.setText("Select your robot")
        lbl.setFixedHeight(100)
        lbl.setAlignment(Qt.AlignCenter) 
        lbl.setStyleSheet('color: white')     

        main_layout.addLayout(self.robot_layout)
        main_layout.addWidget(lbl)

        self.show()

    def createLabel(self, text, font):
        label = QLabel(self)
        label.setFont(font)
        label.setText(text)
        label.setFixedHeight(40)
        label.setAlignment(Qt.AlignCenter) 
        label.setStyleSheet('background-color: rgba(0,0,0,0);color: white; border: 0px solid black; ')
        return label

    def create_robot_frame(self, robot_type, robot_name):

        v3d = View3D(robot_type)
        frame = CustomQFrame(v3d, self)
        r1_layout = QVBoxLayout()        
        font = QFont('Arial', 15)
        lr = self.createLabel(robot_name, font) 

        r1_layout.addWidget(v3d)
        r1_layout.addWidget(lr)
        frame.setLayout(r1_layout)

        return frame



    def init_statusbar(self):
        self.sbar = self.statusBar()
        self.sbar.setStyleSheet('border: 0; background-color: #333333; color: white; QStatusBar::item {border: none;}') 

        # self.sbar.showMessage("bla-bla bla")
        self.lbl1 = QLabel()
        self.lbl1.setStyleSheet('border: 0; color:  white;')
        self.lbl2 = QLabel()
        self.lbl2.setStyleSheet('border: 0; color:  white;')

        self.sbar.addPermanentWidget(VLine())    # <---
        self.sbar.addPermanentWidget(self.lbl1)
        self.sbar.addPermanentWidget(VLine())    # <---
        self.sbar.addPermanentWidget(self.lbl2)
        self.sbar.addPermanentWidget(VLine())    # <---

        self.lbl1.setText("Behavior Suite ")

    def recurring_timer(self):
        hour = datetime.datetime.now()
        dt_string = hour.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl2.setText(dt_string)

    def button_clicked(self):
        self.do_animation()

    def do_animation(self):

        self.anim_above = QPropertyAnimation(self.frame_above, b'pos')
        self.anim_above.setStartValue(self.frame_above.pos())
        self.anim_above.setEndValue(QPoint(0, -1000))
        self.anim_above.setDuration(3000)

        self.anim_below = QPropertyAnimation(self.frame_below, b'pos')
        self.anim_below.setStartValue(self.frame_below.pos())
        self.anim_below.setEndValue(QPoint(self.frame_below.x(), self.frame_below.y() + 1000))
        self.anim_below.setDuration(3000)

        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim_above)
        self.anim_group.addAnimation(self.anim_below)

        self.anim_group.start()
        
    
    def update_gui(self):
        # self.update()
        # print('Size {} x {} px'.format(self.width(), self.height()))
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleWindow()

    th = ThreadGUI(ex)
    th.daemon = True
    th.start()

    sys.exit(app.exec_())