from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import resources

class MyMovableWidget(QWidget):
    """WToolBar is a personalized toolbar."""

    homeAction = None

    oldPos = QPoint()

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setStyleSheet('background-color: blue')
        b = QLabel(self)
        b.setPixmap(QPixmap(':/assets/logo_200.svg'))

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

class MainWindow(QMainWindow):
    updGUI = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()

        ww = MyMovableWidget(self)
        gr = QSizeGrip(ww)

        self.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    coolWidget = MainWindow()
    coolWidget.show()
    sys.exit(app.exec_())