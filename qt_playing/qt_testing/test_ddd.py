from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import resources

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QLabel.__init__(self)
        self.setAcceptDrops(True)
        self.dragstart = None

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.dragstart = event.pos()
            # self.clicked.emit()

    def mouseReleaseEvent(self, event):
        self.dragstart = None

    def mouseMoveEvent(self, event):
        if (self.dragstart is not None and
            event.buttons() & QtCore.Qt.LeftButton and
            (event.pos() - self.dragstart).manhattanLength() >
             QtWidgets.qApp.startDragDistance()):
            self.dragstart = None
            drag = QtGui.QDrag(self)
            drag.setMimeData(QtCore.QMimeData())
            drag.exec_(QtCore.Qt.LinkAction)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        if event.source() is not self:
            self.clicked.emit()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        central_widget = QtWidgets.QWidget()

        self.setFixedSize(300, 300)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(0)
        hbox.addStretch()

        label01 = ClickableLabel()
        label01.setPixmap(QtGui.QPixmap(':/assets/logo_100.svg'))
        label01.clicked.connect(self.print_something)
        hbox.addWidget(label01)

        label02 = ClickableLabel()
        label02.setPixmap(QtGui.QPixmap(':/assets/logo_100.svg'))
        label02.clicked.connect(self.print_something)
        hbox.addWidget(label02)

        label03 = ClickableLabel()
        label03.setPixmap(QtGui.QPixmap(':/assets/logo_100.svg'))
        label03.clicked.connect(self.print_something)
        hbox.addWidget(label03)

        hbox.addStretch()

        central_widget.setLayout(hbox)

        self.setCentralWidget(central_widget)

    def print_something(self):
        print("Printing something..")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())