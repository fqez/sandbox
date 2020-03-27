from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import resources
from collections import defaultdict


current_selection_id = 0

class ClickableQFrame(QFrame):

    def __init__(self, parent, row, col):
        QFrame.__init__(self)
        self.parent = parent
        self.is_selected = False
        self.group_id = -1
        self.row = row
        self.col = col

        lay = QVBoxLayout()
        t = str(self.row) + ',' + str(self.col)
        labelpos = QLabel(t)
        global current_selection_id
        self.labelgr = QLabel(str(self.group_id))
        labelpos.setStyleSheet('QLabel{ font-size: 30px; color: white}')
        self.labelgr.setStyleSheet('QLabel{ font-size: 30px; color: white}')
        labelpos.setText(t)
        lay.addWidget(labelpos)
        lay.addWidget(self.labelgr)
        self.setLayout(lay)
        self.setStyleSheet("""QFrame{
            border: 3px solid white;
            border-radius: 20px
        }""")

    def enterEvent(self, event):
        # print('over frame {}, with geom: {}'.format(self.get_position(), self.geometry()))
        self.setStyleSheet("""
            border: 3px solid yellow;
            border-radius: 20px
        """)
        self.parent.over_frame.emit(self)
    
    def leaveEvent(self, event):
        if not self.is_selected:
            self.setStyleSheet("""
                border: 3px solid white;
                border-radius: 20px
            """)
        else:
            self.parent.leave_frame.emit(self)
        
    def mousePressEvent(self, event):
        global current_selection_id
        if event.buttons() & Qt.LeftButton:
            if not self.is_selected:
                modifiers = QApplication.keyboardModifiers()
                if not modifiers == Qt.ControlModifier:
                    current_selection_id += 1
                self.is_selected = True
                self.group_id = current_selection_id
            else:
                self.is_selected = False
                self.group_id = -1
        self.labelgr.setText(str(self.group_id))

    def get_position(self):
        return (self.row, self.col)

    # def __str__(self):
    #     return "Frame:\n\tposition [{}, {}]\n\tselected: {}\n\tgroup_id: {}".format(self.row, self.col, self.is_selected, self.selection_grop)

class LayoutSel(QWidget):

    over_frame = pyqtSignal(ClickableQFrame)
    leave_frame = pyqtSignal(ClickableQFrame)

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.dragstart = None
        # self.over_frame.connect(self.add_to_group)
        self.main_layout = QGridLayout()

        # add left side toolbar
        self.tools = Toolbar()
        # self.main_layout.addWidget(self.tools, 0, 0, 3, 1)

        # add matrix frame
        self.frames = []
        for row in range (4):
            for col in range(1, 4):
                frame = ClickableQFrame(self, row, col)
                frame.setMouseTracking(True)
                self.frames.append(frame)
                self.main_layout.addWidget(frame, row, col)
        self.setLayout(self.main_layout)

    def collect_groups(self):
        """ retrieve info of the final layout"""
        groups = defaultdict(list)
        for frame in self.frames:
            # id = groups.get(frame.group_id)
            groups[frame.group_id].append(frame)
        return groups
            

        # for frame in self.frames:
        #     print('frame: {}'.format(frame.get_position())) 

    # def mousePressEvent(self, event):
    #     if event.buttons() & Qt.LeftButton:
    #         self.dragstart = event.pos()
    #         # self.clicked.emit()

    # def mouseReleaseEvent(self, event):
    #     start = self.dragstart
    #     end = event.pos()
    #     # print('started at {}, ended at {}'.format(start, end))
    #     # self.check_selected_frames(start, end)
    #     self.dragstart = None
    
    # @pyqtSlot(ClickableQFrame)
    # def add_to_group(self, frame):
    #     print('trying to add: ', self.dragstart)
    #     if self.dragstart:
    #         print('add', frame)

    # @pyqtSlot(ClickableQFrame)
    # def remove_from_group(self, frame):
    #     if self.dragstart:
    #         print('remove', frame)


        

    # def mouseMoveEvent(self, event):
    #     if (self.dragstart is not None and
    #         event.buttons() & Qt.LeftButton and
    #         (event.pos() - self.dragstart).manhattanLength() >
    #          qApp.startDragDistance()):
    #         self.dragstart = None
    #         drag = QDrag(self)
    #         drag.setMimeData(QMimeData())
    #         drag.exec_(Qt.LinkAction)

    # def dragEnterEvent(self, event):
    #     event.acceptProposedAction()
    #     if event.source() is not self:
    #         self.clicked.emit()
    #         print('dragevent')   

    # def mousePressEvent(self, evt):
    #     """Select the toolbar."""
    #     self.oldPos = evt.globalPos()
    #     print('-----')

    # def mouseMoveEvent(self, evt):
    #     """Move the toolbar with mouse iteration."""
    #     delta = QPoint(evt.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     print('old pos', self.oldPos)
    #     self.oldPos = evt.globalPos()

class Toolbar(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setStyleSheet('background-color: green')
        self.setMaximumWidth(500)
        self.initUI()

        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid gray;
                border-color: #FF17365D;
                margin-top: 27px;
                font-size: 14px;
                border-radius: 15px;
            }
            QGroupBox::title {
                border-top-left-radius: 9px;
                border-top-right-radius: 9px;
                padding: 2px 82px;
                background-color: #FF17365D;
                color: rgb(255, 255, 255);
            }""")

    def initUI(self):
        self.main_layout = QVBoxLayout()
        b1 = QGroupBox()
        b1_layout = QGridLayout()
        b1.setTitle('Box1')



        self.main_layout.addWidget(b1)

        self.setLayout(self.main_layout)

class LayoutBase(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.main_layout = QGridLayout()

        self.tools = Toolbar()
        self.main_layout.addWidget(self.tools, 0, 0, 3, 1)
        camera = CameraWidget()
        self.main_layout.addWidget(camera ,0,1,1,1)
        camera2 = CameraWidget()
        self.main_layout.addWidget(camera2 ,1,1,2,2)

        self.setLayout(self.main_layout)

    def mousePressEvent(self, evt):
        """Select the toolbar."""
        self.oldPos = evt.globalPos()
        print('-----')

    def mouseMoveEvent(self, evt):
        """Move the toolbar with mouse iteration."""
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        print('old pos', self.oldPos)
        self.oldPos = evt.globalPos()

class CameraWidget(QWidget):

    signal_update = pyqtSignal()

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.signal_update.connect(self.update)
        self.associated_topic = None
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setMouseTracking(True)
        self.setMouseTracking(True)

        self.image_label.setPixmap(QPixmap(':/assets/logo_200.svg'))
        self.image_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.image_label)
        self.setLayout(self.main_layout)

    def enterEvent(self, event):
        print("enter in widget")
        self.setStyleSheet('background-color: yellow')

    def leaveEvent(self, event):
        print('leave widget')
        self.setStyleSheet('background-color: rgba(0,0,0,0)')

    def update(self):
        # get image from topic? pass image?
        pass

class MainWindow(QMainWindow):
    updGUI = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setFixedSize(1750,900)
        self.setStyleSheet('background-color: rgb(51,51,51)')
        central_w = QWidget()
        self.layout = QVBoxLayout()
        self.base = LayoutSel()
        self.layout.addWidget(self.base, 0)

        confirm = QPushButton("Confirm", self)
        confirm.setFixedSize(100,50)
        confirm.clicked.connect(self.get_config)
        self.layout.addWidget(confirm)

        central_w.setLayout(self.layout)
        self.setCentralWidget(central_w)

        self.show()

    def get_config(self):
        groups = self.base.collect_groups()
        self.gs = []
        for id in groups:
            if id == -1:
                continue
            frames = groups[id]
            min_row = min(frame.row for frame in frames)
            min_col = min(frame.col for frame in frames)
            max_row = max(frame.row for frame in frames)
            max_col = max(frame.col for frame in frames)
            print('(widget, {}, {}, {}, {})'.format(min_row, min_col, (max_row - min_row)+1, (max_col - min_col)+1))
            self.gs.append( (min_row, min_col, (max_row - min_row)+1, (max_col - min_col)+1))
        self.paint_new(self.gs)

    def paint_new(self, config):
        greedy = QGridLayout()
        self.layout.addLayout(greedy)
        positions = config
        for c in positions:
            lbl = QLabel()
            lbl.setStyleSheet('border: 2px solid white')
            lbl.setPixmap(QPixmap(':/assets/logo_100.svg'))
            lbl.setAlignment(Qt.AlignCenter)
            greedy.addWidget(lbl, c[0], c[1], c[2], c[3])

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    coolWidget = MainWindow()
    coolWidget.show()
    sys.exit(app.exec_())