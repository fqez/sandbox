from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap


class ImageWindow(QtWidgets.QWidget):

    imageUpdate = QtCore.pyqtSignal()

    def __init__(self, winParent):
        super(ImageWindow, self).__init__()
        self.winParent = winParent
        self.initUI()

    def initUI(self):

        self.setWindowTitle("image")
        self.imgLabel = QtWidgets.QLabel(self)

    def setImage(self, path):
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(800, 600, QtCore.Qt.KeepAspectRatio)
        self.imgLabel.setPixmap(pixmap)
        self.setMinimumSize(pixmap.width(), pixmap.height())