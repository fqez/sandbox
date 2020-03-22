from __future__ import division

import sys
import time
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtSvg


from threadGUI import ThreadGUI
import threading

WIDTH = 1750
HEIGHT = 900

# WIDTH = 800
# HEIGHT = 600

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

        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setStyleSheet('background-color: rgb(51,51,51)')
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        

        from models3d import *

        v3d = View3D('car')
        v3d2 = View3D('drone')
        v3d3 = View3D('car')
        # v3d.show()
        main_layout.addWidget(v3d)
        main_layout.addWidget(v3d2)
        main_layout.addWidget(v3d3)

        self.show()

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