from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,QLineEdit, QFileDialog, QCheckBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QRect, pyqtSlot
import numpy as np
from imageWindow import ImageWindow

import sys
import cv2

from lpf import filter
from sobel import sobel, sobelfft
from dct import dct_main

time_cycle = 50

class MainWindow(QMainWindow):

    updGUI = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.sourceImage = 'lena.jpg'
        self.imgW = ImageWindow(self)
        self.imgW2 = ImageWindow(self)
        self.imgW3 = ImageWindow(self)
        self.imgW4 = ImageWindow(self)
        self.imgW5 = ImageWindow(self)

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

        self.toolBox = QGroupBox("Filters and tools")
        self.paramBox = QGroupBox("Parametets")
        self.leftLayout.addWidget(self.toolBox)
        self.leftLayout.addWidget(self.paramBox)
        self.hLayout.addLayout(self.leftLayout)
        self.hLayout.addLayout(self.imageLayout)




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

        self.dctBox = QGroupBox("DCT")
        layout = QVBoxLayout()

        self.b1 = QCheckBox("Compression 1/64")
        self.b1.setChecked(True)
        self.b1.stateChanged.connect(lambda: self.btnstate(self.b1))
        self.b2 = QCheckBox("Compression 3/64")
        self.b2.toggled.connect(lambda: self.btnstate(self.b2))
        self.b3 = QCheckBox("Compression 3/64")
        self.b3.toggled.connect(lambda: self.btnstate(self.b3))
        self.b4 = QCheckBox("Compression 6/64")
        self.b4.toggled.connect(lambda: self.btnstate(self.b4))
        self.b5 = QCheckBox("Compression 10/64")
        self.b5.toggled.connect(lambda: self.btnstate(self.b5))
        self.b6 = QCheckBox("Compression 15/64")
        self.b6.toggled.connect(lambda: self.btnstate(self.b6))
        self.b7 = QCheckBox("Compression 21/64")
        self.b7.toggled.connect(lambda: self.btnstate(self.b7))
        self.b8 = QCheckBox("Compression 28/64")
        self.b8.toggled.connect(lambda: self.btnstate(self.b8))
        self.b9 = QCheckBox("Compression 36/64")
        self.b9.toggled.connect(lambda: self.btnstate(self.b9))

        layout.addWidget(self.b1)
        layout.addWidget(self.b2)
        layout.addWidget(self.b3)
        layout.addWidget(self.b4)
        layout.addWidget(self.b5)
        layout.addWidget(self.b6)
        layout.addWidget(self.b7)
        layout.addWidget(self.b8)
        layout.addWidget(self.b9)

        self.dctBox.setLayout(layout)




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
        self.imgLabel.fileName = 'lena.jpg'
        self.imgLabel.mousePressEvent = self.clicked1
        self.imgText = QtWidgets.QLabel(self)
        self.imgText.setText("source")
        self.vsource = QVBoxLayout()
        self.vsource.addWidget(self.imgText)
        self.vsource.addWidget(self.imgLabel)

        self.imgLabel2 = QtWidgets.QLabel(self)
        self.imgLabel2.fileName = 'lena.jpg'
        self.imgLabel2.mousePressEvent = self.clicked2
        self.imgText2 = QtWidgets.QLabel(self)
        self.imgText2.setText("Title1")
        self.vsource2 = QVBoxLayout()
        self.vsource2.addWidget(self.imgText2)
        self.vsource2.addWidget(self.imgLabel2)

        self.imgLabel3 = QtWidgets.QLabel(self)
        self.imgLabel3.fileName = 'lena.jpg'
        self.imgLabel3.mousePressEvent = self.clicked3
        self.imgText3 = QtWidgets.QLabel(self)
        self.imgText3.setText("Title2")
        self.vsource3 = QVBoxLayout()
        self.vsource3.addWidget(self.imgText3)
        self.vsource3.addWidget(self.imgLabel3)

        self.imgLabel4 = QtWidgets.QLabel(self)
        self.imgLabel4.fileName = 'lena.jpg'
        self.imgLabel4.mousePressEvent = self.clicked4
        self.imgText4 = QtWidgets.QLabel(self)
        self.imgText4.setText("Title3")
        self.vsource4 = QVBoxLayout()
        self.vsource4.addWidget(self.imgText4)
        self.vsource4.addWidget(self.imgLabel4)

        self.imgLabel5 = QtWidgets.QLabel(self)
        self.imgLabel5.fileName = 'lena.jpg'
        self.imgLabel5.mousePressEvent = self.clicked5
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
        self.paramsLayout.addWidget(self.dctBox)
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


    def clicked1(self, event):
        print("labelClicked")
        self.imgW.setImage(self.imgLabel.fileName)
        self.imgW.show()

    def clicked2(self, event):
        print("labelClicked")
        self.imgW2.setImage(self.imgLabel2.fileName)
        self.imgW2.show()

    def clicked3(self, event):
        print("labelClicked")
        self.imgW3.setImage(self.imgLabel3.fileName)
        self.imgW3.show()

    def clicked4(self, event):
        print("labelClicked")
        self.imgW4.setImage(self.imgLabel4.fileName)
        self.imgW4.show()

    def clicked5(self, event):
        print("labelClicked")
        self.imgW5.setImage(self.imgLabel5.fileName)
        self.imgW5.show()

    def checkText(self):
        img = cv2.imread(self.sourceImage)
        frec = self.cutFrec.text()
        n = self.order.text()
        if frec == "" or n == "":
            None
        else:
            n = int(n)
            frec = int(frec)
            if self.low_pass_radio_button.isChecked():
                result, fft = filter(img, frec, n, 'low')
                self.imgText2.setText("Low Pass Filter")
            else:
                result, fft = filter(img, frec, n)
                self.imgText2.setText("High Pass Filter")
            cv2.imwrite("results/filter.jpg", result.real)
            cv2.imwrite("results/fourier.jpg", fft.real)

            pixmap = QPixmap('results/filter.jpg')
            pixmap2 = QPixmap('results/fourier.jpg')
            pixmap = pixmap.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
            pixmap2 = pixmap2.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
            self.imgLabel2.fileName ='results/filter.jpg'
            self.imgLabel3.fileName = 'results/fourier.jpg'
            self.imgLabel2.setPixmap(pixmap)
            self.imgLabel3.setPixmap(pixmap2)
            self.imgText3.setText("Center FFT")

    @pyqtSlot()
    def on_change_cf(self):
        self.checkText()

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

        Vkernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        Hkernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        v, h = sobel(img, Vkernel, Hkernel)

        img_fft = np.fft.fft2(img)
        vfft, hfft = sobelfft(img_fft, Vkernel, Hkernel)

        cv2.imwrite("results/sobelV.jpg", v)
        cv2.imwrite("results/sobelH.jpg", h)
        cv2.imwrite("results/sobelVFFT.jpg", vfft)
        cv2.imwrite("results/sobelHFFT.jpg", hfft)

        pixmap = QPixmap('results/sobelV.jpg')
        pixmap2 = QPixmap('results/sobelH.jpg')
        pixmap3 = QPixmap('results/sobelVFFT.jpg')
        pixmap4 = QPixmap('results/sobelHFFT.jpg')
        pixmap = pixmap.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
        pixmap2 = pixmap2.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
        pixmap3 = pixmap3.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
        pixmap4 = pixmap4.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
        self.imgLabel2.setPixmap(pixmap)
        self.imgText2.setText("Vertical borders image domain")
        self.imgLabel3.setPixmap(pixmap2)
        self.imgText3.setText("Horizontal borders image domain")
        self.imgLabel4.setPixmap(pixmap3)
        self.imgText4.setText("Vertical borders FFT domain")
        self.imgLabel5.setPixmap(pixmap4)
        self.imgText5.setText("Horizontal borders FFT domain")

    @pyqtSlot()
    def on_click_dct(self):
        self.order.setEnabled(False)
        self.cutFrec.setEnabled(False)
        self.block.setEnabled(True)
        img = cv2.imread(self.sourceImage)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dct_main(img)

    def btnstate(self, b):
        if b.isChecked():
            pixmap = QPixmap('results/comp_1_dct.jpg')
            pixmap2 = QPixmap('results/comp_1_idct.jpg')
            pixmap3 = QPixmap('results/comp_3_dct.jpg')
            pixmap4 = QPixmap('results/comp_3_idct.jpg')
            pixmap = pixmap.scaled(self.imgLabel.width(), self.imgLabel.height(), QtCore.Qt.KeepAspectRatio)
            pixmap2 = pixmap2.scaled(self.imgLabel2.width(), self.imgLabel2.height(), QtCore.Qt.KeepAspectRatio)
            pixmap3 = pixmap3.scaled(self.imgLabel3.width(), self.imgLabel3.height(), QtCore.Qt.KeepAspectRatio)
            pixmap4 = pixmap4.scaled(self.imgLabel4.width(), self.imgLabel4.height(), QtCore.Qt.KeepAspectRatio)
            self.imgLabel2.fileName = 'results/comp_1_dct'
            self.imgLabel3.fileName = 'results/comp_1_idct.jpg'
            self.imgLabel2.setPixmap(pixmap)
            self.imgText2.setText(b.text() + " DCT")
            self.imgLabel3.setPixmap(pixmap2)
            self.imgText3.setText(b.text() + " IDCT")
            self.imgLabel4.setPixmap(pixmap3)
            self.imgText2.setText(b.text() + " DCT")
            self.imgLabel5.setPixmap(pixmap4)
            self.imgText2.setText(b.text() + " DCT")
            print(b.text())


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fn, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;JPEG (*.jpg);;PNG (*.png)", options=options)
        if fn:
            print(fn)
            self.sourceImage = fn
            pixmap = QPixmap(fn)
            pixmap = pixmap.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
            self.imgLabel.setPixmap(pixmap)
            self.imgLabel.fileName = fn
            self.imgLabel2.setPixmap(pixmap)
            self.imgLabel2.fileName = fn
            self.imgLabel3.setPixmap(pixmap)
            self.imgLabel3.fileName = fn
            self.imgLabel4.setPixmap(pixmap)
            self.imgLabel4.fileName = fn
            self.imgLabel5.setPixmap(pixmap)
            self.imgLabel5.fileName = fn
            self.low_pass_radio_button.setChecked(False)
            self.high_pass_radio_button.setChecked(False)
            self.sobel_radio_button.setChecked(False)
            self.dct_radio_button.setChecked(False)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()

    sys.exit(app.exec_())