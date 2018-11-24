from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,QLineEdit, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QRect, pyqtSlot
import numpy as np

import sys
import cv2

import lpf
from sobel import filterSobelOrig, filterSobelFft

time_cycle = 50

class MainWindow(QMainWindow):

    updGUI = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.sourceImage = 'lena.jpg'

        self.setupUI()

    def setupUI(self):
        self.setFixedSize(950,550)

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 30, 900, 500))
        self.hLayout = QHBoxLayout(self.verticalLayoutWidget)
        self.leftLayout = QVBoxLayout()
        self.toolsLayout = QVBoxLayout()
        self.paramsLayout = QVBoxLayout()
        self.imageLayout = QGridLayout()
        self.toolBox = QGroupBox("Filters and tools")
        self.paramBox = QGroupBox("Parametets")
        self.leftLayout.addWidget(self.toolBox)
        self.leftLayout.addWidget(self.paramBox)
        self.hLayout.addLayout(self.leftLayout)
        self.hLayout.addLayout(self.imageLayout)

        self.btnLabel = QtWidgets.QLabel(self)
        self.btnLabel.setText("Image:")
        self.imgButton = QPushButton(self)
        self.imgButton.setText("Browse...")
        self.imgButton.move(20, 20)
        self.imgButton.resize(20, 40)
        self.hbtn = QHBoxLayout()
        self.hbtn.addWidget(self.btnLabel)
        self.hbtn.addWidget(self.imgButton)
        self.leftLayout.addLayout(self.hbtn)


        # ---------------- RADIO BUTTONS ------------------------
        self.low_pass_radio_button = QtWidgets.QRadioButton(self)
        self.low_pass_radio_button.setText("Butterworth LPF")
        self.high_pass_radio_button = QtWidgets.QRadioButton(self)
        self.high_pass_radio_button.setText("Butterworth HPF")
        self.sobel_radio_button = QtWidgets.QRadioButton(self)
        self.sobel_radio_button.setText("Sobel Filter")
        self.dct_radio_button = QtWidgets.QRadioButton(self)
        self.dct_radio_button.setText("DCT compression")

        #self.low_pass_radio_button.setChecked(True)

        # ---------------- PARAMETERS ------------------------
        self.frecLabel = QtWidgets.QLabel(self)
        self.frecLabel.setText("Frec.")
        self.cutFrec = QLineEdit(self)
        self.cutFrec.setText("20")
        self.cutFrec.move(20, 20)
        self.cutFrec.resize(20, 40)
        self.hFrec = QHBoxLayout()
        self.hFrec.addWidget(self.frecLabel)
        self.hFrec.addWidget(self.cutFrec)

        self.orderLabel = QtWidgets.QLabel(self)
        self.orderLabel.setText("Order (n)")
        self.order = QLineEdit(self)
        self.order.setText("1")
        self.order.move(20, 20)
        self.order.resize(20, 40)
        self.horder = QHBoxLayout()
        self.horder.addWidget(self.orderLabel)
        self.horder.addWidget(self.order)

        self.blockLabel = QtWidgets.QLabel(self)
        self.blockLabel.setText("Block size")
        self.block = QLineEdit(self)
        self.block.move(20, 20)
        self.block.resize(20, 40)
        self.hblock = QHBoxLayout()
        self.hblock.addWidget(self.blockLabel)
        self.hblock.addWidget(self.block)



        # ---------------- IMAGES ------------------------
        self.imgLabel = QtWidgets.QLabel(self)
        self.imgText = QtWidgets.QLabel(self)
        self.imgText.setText("source")
        self.vsource = QVBoxLayout()
        self.vsource.addWidget(self.imgText)
        self.vsource.addWidget(self.imgLabel)

        self.imgLabel2 = QtWidgets.QLabel(self)
        self.imgText2 = QtWidgets.QLabel(self)
        self.imgText2.setText("Title1")
        self.vsource2 = QVBoxLayout()
        self.vsource2.addWidget(self.imgText2)
        self.vsource2.addWidget(self.imgLabel2)

        self.imgLabel3 = QtWidgets.QLabel(self)
        self.imgText3 = QtWidgets.QLabel(self)
        self.imgText3.setText("Title2")
        self.vsource3 = QVBoxLayout()
        self.vsource3.addWidget(self.imgText3)
        self.vsource3.addWidget(self.imgLabel3)

        self.imgLabel4 = QtWidgets.QLabel(self)
        self.imgText4 = QtWidgets.QLabel(self)
        self.imgText4.setText("Title3")
        self.vsource4 = QVBoxLayout()
        self.vsource4.addWidget(self.imgText4)
        self.vsource4.addWidget(self.imgLabel4)

        self.imgLabel5 = QtWidgets.QLabel(self)
        self.imgText5 = QtWidgets.QLabel(self)
        self.imgText5.setText("Title4")
        self.vsource5 = QVBoxLayout()
        self.vsource5.addWidget(self.imgText5)
        self.vsource5.addWidget(self.imgLabel5)

        pixmap = QPixmap('../images/lena.jpg')
        pixmap = pixmap.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
        self.imgLabel.setPixmap(pixmap)
        self.imgLabel2.setPixmap(pixmap)
        self.imgLabel3.setPixmap(pixmap)
        self.imgLabel4.setPixmap(pixmap)
        self.imgLabel5.setPixmap(pixmap)

        #-------------------- LAYOUTS --------------------------
        self.toolsLayout.addWidget(self.low_pass_radio_button)
        self.toolsLayout.addWidget(self.high_pass_radio_button)
        self.toolsLayout.addWidget(self.sobel_radio_button)
        self.toolsLayout.addWidget(self.dct_radio_button)
        self.paramsLayout.addLayout(self.hFrec)
        self.paramsLayout.addLayout(self.horder)
        self.paramsLayout.addLayout(self.hblock)
        self.toolBox.setLayout(self.toolsLayout)
        self.paramBox.setLayout(self.paramsLayout)
        self.imageLayout.addLayout(self.vsource,0,0)
        self.imageLayout.addLayout(self.vsource2,0,1)
        self.imageLayout.addLayout(self.vsource3,0,2)
        self.imageLayout.addLayout(self.vsource4,1,1)
        self.imageLayout.addLayout(self.vsource5,1,2)


        #------------------- CONNECTIONS ------------------
        self.cutFrec.textChanged.connect(self.on_change_cf)
        self.order.textChanged.connect(self.on_change_cf)
        self.imgButton.clicked.connect(self.on_click)
        self.low_pass_radio_button.clicked.connect(self.on_click_lpf)
        self.high_pass_radio_button.clicked.connect(self.on_click_hpf)
        self.sobel_radio_button.clicked.connect(self.on_click_sobel)
        self.dct_radio_button.clicked.connect(self.on_click_dct)

    def checkText(self):
        img = cv2.imread(self.sourceImage)
        print(self.sourceImage,img)
        frec = self.cutFrec.text()
        n = self.order.text()
        if frec == "" or n == "":
            None
        else:
            n = int(n)
            frec = int(frec)
            img_org = None
            if self.low_pass_radio_button.isChecked():
                img_org, a = lpf.filter(img, frec, n, 'low')
                self.imgText2.setText("Low Pass Filter")
            else:
                img_org, a = lpf.filter(img, frec, n)
                self.imgText2.setText("High Pass Filter")
            cv2.imwrite("lpf.jpg", img_org.real)
            cv2.imwrite("a.jpg", a.real)

            pixmap = QPixmap('lpf.jpg')
            pixmap2 = QPixmap('a.jpg')
            pixmap = pixmap.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
            pixmap2 = pixmap2.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
            self.imgLabel2.setPixmap(pixmap)

            self.imgLabel3.setPixmap(pixmap2)
            self.imgText3.setText("Center FFT")

    @pyqtSlot()
    def on_change_cf(self):
        #self.checkText()
        print(self.sourceImage)


    @pyqtSlot()
    def on_click(self):
        self.openFileNameDialog()

    @pyqtSlot()
    def on_click_lpf(self):
        self.order.setEnabled(True)
        self.cutFrec.setEnabled(True)
        self.block.setEnabled(False)
        self.checkText()

    @pyqtSlot()
    def on_click_hpf(self):
        self.order.setEnabled(True)
        self.cutFrec.setEnabled(True)
        self.block.setEnabled(False)
        self.checkText()

    @pyqtSlot()
    def on_click_sobel(self):
        self.order.setEnabled(False)
        self.cutFrec.setEnabled(False)
        self.block.setEnabled(False)
        img = cv2.imread(self.sourceImage)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        SobelH = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        SobelV = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        print(SobelV)
        BH1,BV1 = filterSobelOrig(img, SobelH, SobelV)
        img_fft = np.fft.fft2(img)
        BH2,BV2 = filterSobelFft(img_fft, SobelH, SobelV)

        cv2.imwrite("bh1.jpg", BH1)
        cv2.imwrite("bv1.jpg", BV1)
        cv2.imwrite("bh2.jpg", BH2)
        cv2.imwrite("bv2.jpg", BV2)

        pixmap = QPixmap('bh1.jpg')
        pixmap2 = QPixmap('bv1.jpg')
        pixmap3 = QPixmap('bh2.jpg')
        pixmap4 = QPixmap('bv2.jpg')
        pixmap = pixmap.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
        pixmap2 = pixmap2.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
        pixmap3 = pixmap3.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
        pixmap4 = pixmap4.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
        self.imgLabel2.setPixmap(pixmap)
        self.imgText2.setText("Horizontal borders image domain")
        self.imgLabel3.setPixmap(pixmap2)
        self.imgText3.setText("Vertical borders image domain")
        self.imgLabel4.setPixmap(pixmap3)
        self.imgText4.setText("Horizontal borders FFT domain")
        self.imgLabel5.setPixmap(pixmap4)
        self.imgText5.setText("Vertical borders FFT domain")



    @pyqtSlot()
    def on_click_dct(self):
        self.order.setEnabled(False)
        self.cutFrec.setEnabled(False)
        self.block.setEnabled(True)
        print("dct")

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;JPEG (*.jpg);;PNG (*.png)", options=options)
        if fileName:
            print(fileName)
            self.sourceImage = fileName
            pixmap = QPixmap(fileName)
            pixmap = pixmap.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(pixmap)
            self.imgLabel2.setPixmap(pixmap)
            self.imgLabel3.setPixmap(pixmap)
            self.imgLabel4.setPixmap(pixmap)
            self.imgLabel5.setPixmap(pixmap)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()

    sys.exit(app.exec_())