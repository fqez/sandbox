import sys
import time
import datetime


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from title import TitleWindow
from robot_selection import RobotSelection
from world_selection import WorldSelection
from threadGUI import ThreadGUI

WIDTH = 1750    #800
HEIGHT = 900    #600

class VLine(QFrame):
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)

class ParentWindow(QMainWindow):
    updGUI = pyqtSignal()

    def __init__(self):
        super(ParentWindow, self).__init__()
        self.windowsize = QSize(WIDTH,HEIGHT)
        self.updGUI.connect(self.update_gui)
        self.initUI()

        self.robot_selection = None
        self.world_selection = None

    def initUI(self):
        self.setFixedSize(self.windowsize)
        self.init_statusbar()

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        self.main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setStyleSheet('background-color: rgb(51,51,51)')
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def init_statusbar(self):
        self.sbar = self.statusBar()
        self.sbar.setStyleSheet('border: 0; background-color: #333333; color: white; QStatusBar::item {border: none;}') 

        # self.sbar.showMessage("bla-bla bla")
        self.lbl1 = QLabel()
        self.lbl1.setStyleSheet('border: 0; color:  white;')
        self.lbl2 = QLabel()
        self.lbl2.setStyleSheet('border: 0; color:  white;')

        self.sbar.addPermanentWidget(VLine())
        self.sbar.addPermanentWidget(self.lbl1)
        self.sbar.addPermanentWidget(VLine())
        self.sbar.addPermanentWidget(self.lbl2)
        self.sbar.addPermanentWidget(VLine())

        self.lbl1.setText("Behavior Suite ")

    def recurring_timer(self):
        hour = datetime.datetime.now()
        dt_string = hour.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl2.setText(dt_string)
        
    def update_gui(self):
        # self.update()
        # print('Size {} x {} px'.format(self.width(), self.height()))
        pass

class Controller:

    home_singal = pyqtSignal()
    robot_select_signal = pyqtSignal()
    
    def __init__(self, parent):
        self.parent = parent
        # self.home_singal.connect(self.show_title)
        # self.robot_select_signal.connect(self.show_robot_selection)

    def show_title(self):
        self.title = TitleWindow(self.parent)
        self.parent.main_layout.addWidget(self.title)
        self.title.switch_window.connect(self.show_robot_selection)
        self.title.show()
    
    def show_robot_selection(self):
        delete_widgets_from(self.parent.main_layout)
        self.title.close()
        del self.title
        self.robot_selector = RobotSelection(self.parent)
        self.parent.main_layout.addWidget(self.robot_selector)
        self.robot_selector.switch_window.connect(self.show_world_selection)
        self.robot_selector.show()

    def show_world_selection(self):
        delete_widgets_from(self.parent.main_layout)
        self.robot_selector.close()
        del self.robot_selector
        self.world_selector = WorldSelection(self.parent.robot_selection, self.parent)
        self.parent.main_layout.addWidget(self.world_selector)
        self.world_selector.switch_window.connect(self.show_layout_selection)
        self.world_selector.show()

    def show_layout_selection(self):
        print('A layouts')
        delete_widgets_from(self.parent.main_layout)
        self.world_selector.close()
        del self.world_selector
        self.layout_selector = LayoutSelector(self.parent)
        self.parent.main_layout.addWidget(self.layout_selector)
        self.layout_selector.switch_window.connect(self.show_main_view)
        self.layout_selector.show()

def delete_widgets_from(layout):
    """ memory secure. """
    for i in reversed(range(layout.count())): 
        widgetToRemove = layout.itemAt(i).widget()
        # remove it from the layout list
        layout.removeWidget(widgetToRemove)
        # remove it from the gui
        widgetToRemove.setParent(None)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = ParentWindow()
    main_window.show()

    controller = Controller(main_window)
    controller.show_title()

    th = ThreadGUI(main_window)
    th.daemon = True
    th.start()

    sys.exit(app.exec_())