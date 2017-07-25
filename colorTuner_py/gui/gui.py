#
#  Copyright (C) 1997-2016 JDE Developers Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#  Authors :
#       Alberto Martin Florido <almartinflorido@gmail.com>
#       Aitor Martinez Fernandez <aitor.martinez.fernandez@gmail.com>
#


from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QGroupBox, QLabel, QToolTip, QAction, QDialog
from myLabel import MyLabel
from controlWidget import  ControlWidget
from logoWidget import  LogoWidget
import resources_rc
import sys

class MainWindow(QMainWindow):


    # aspect ratio 16:9
    IMAGE_COLS_MAX=640
    IMAGE_ROWS_MAX=320

    # zoom level for pixel selection
    ZOOM_X = 2

    '''def aboutWindow(self):
        about = QDialog(self)
        about.MinimumSize=(500,400)
        logoLayout = QGridLayout()
        logo = LogoWidget(about)
        text = QLabel("Jderobot 5.5.2")
        logoLayout.addWidget(logo,0,0)
        logoLayout.addWidget(text, 2, 0, Qt.AlignCenter)
        about.setLayout(logoLayout)
        about.exec_()'''

    def aboutWindow(self):
        about = QDialog(self)
        about.setFixedSize(550,350)
        about.setWindowTitle("About JdeRobot")
        logoLayout = QHBoxLayout()
        logo = LogoWidget(about)
        text = QLabel(about)
        str = "<span style='font-size:15pt; font-weight:600;'>Jderobot 5.5.2</span> <br><br>Software suite for robotics and computer vision. <br><br>You can find more info <a href='http://jderobot.org'>here</a><br><br>Github <a href='https://github.com/jderobot/jderobot.git'>repository</a>"
        text.setFixedSize(200, 350)
        text.setWordWrap(True);
        text.setTextFormat(Qt.RichText)
        text.setOpenExternalLinks(True)
        text.setText(str)
        logoLayout.addWidget(logo,1)
        logoLayout.addWidget(text, 0, Qt.AlignTop)
        about.setLayout(logoLayout)
        about.exec_()

    def closeApp(self):
        sys.exit()


    updGUI=pyqtSignal()
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        aboutAction = QAction("&About", self)
        aboutAction.setStatusTip('About JdeRobot')
        aboutAction.triggered.connect(self.aboutWindow)

        closeAction = QAction("&Quit", self)
        closeAction.setShortcut("Ctrl+Q")
        closeAction.setStatusTip('Leave The App')
        closeAction.triggered.connect(self.closeApp)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(aboutAction)
        fileMenu.addAction(closeAction)

        

        #self.setMaximumSize(800,600)

        centralWidget = QWidget(self)
        mainLayout = QGridLayout()
        centralWidget.setLayout(mainLayout)

        imagesLayout = QVBoxLayout(self)
        controlLayout = QVBoxLayout(self)

        sliders = QGridLayout(self)

        self.image = QImage(":/images/image.png").scaled(self.IMAGE_COLS_MAX, self.IMAGE_ROWS_MAX, Qt.KeepAspectRatio)
        self.sourceImg = MyLabel(self)
        self.sourceImg.setScaledContents(True)
        self.sourceImg.setPixmap(QPixmap.fromImage(self.image))

        sourceGroupBox = QGroupBox("Source image")
        grid1 = QGridLayout()
        grid1.addWidget(self.sourceImg)
        sourceGroupBox.setLayout(grid1)
        self.sourceImg.setFixedSize(self.IMAGE_COLS_MAX, self.IMAGE_ROWS_MAX)


        self.imageF = QImage(":/images/image.png").scaled(self.IMAGE_COLS_MAX, self.IMAGE_ROWS_MAX)
        self.filterImg = QLabel(self)
        self.filterImg.setScaledContents(True)
        self.filterImg.setPixmap(QPixmap.fromImage(self.imageF))

        filterGroupBox = QGroupBox("Filtered image")
        grid2 = QGridLayout()
        grid2.addWidget(self.filterImg)
        filterGroupBox.setLayout(grid2)
        self.filterImg.setFixedSize(self.IMAGE_COLS_MAX, self.IMAGE_ROWS_MAX)


        print "size1 ", self.sourceImg.size()
        print "size2 ", self.filterImg.size()


        zoompixGroupBox = QGroupBox("Zoom x" + str(self.ZOOM_X))
        grid3 = QGridLayout()
        self.crop = MyLabel(self, True)
        self.crop.setFixedSize(200,200)

        self.tootippixel = QLabel(self)
        self.pixel = QLabel(self)
        self.pixel.setFixedSize(75,75)  
        self.rgbVal = QLabel("RGB")

        grid3.addWidget(self.crop,0,0)
        grid3.addWidget(self.rgbVal,1,0)
        grid3.addWidget(self.pixel,1,0, Qt.AlignRight)
        zoompixGroupBox.setLayout(grid3)

        slidersGroupBox = QGroupBox("Filter setup")
        controlWidget = ControlWidget(self)
        grid4 = QGridLayout()
        grid4.addWidget(controlWidget)
        slidersGroupBox.setLayout(grid4)

        imagesLayout.addWidget(sourceGroupBox,0)
        imagesLayout.addWidget(filterGroupBox,1)
        controlLayout.addWidget(zoompixGroupBox,0)
        controlLayout.addStretch(10)
        controlLayout.addWidget(slidersGroupBox,0)
        mainLayout.addLayout(imagesLayout,0,0)
        mainLayout.addLayout(controlLayout,0,1)

        '''
        mainLayout.addWidget(self.crop,0,1)
        mainLayout.addWidget(self.pixel,1,1)
        mainLayout.addWidget(self.rgbVal,1,0,1,1)'''

        self.setCentralWidget(centralWidget)

        self.updGUI.connect(self.updateGUI)

    def updateGUI(self):

        img = self.camera.getOrigImage()
        if img is not None:
            self.image = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * img.shape[2], QImage.Format_RGB888).scaled(self.IMAGE_COLS_MAX, self.IMAGE_ROWS_MAX)
            self.sourceImg.setPixmap(QPixmap.fromImage(self.image))

        filt = self.getFilterName()
        img = self.camera.getFilteredImage(filt)
        if img is not None:
            self.imageF = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * img.shape[2], QImage.Format_RGB888).scaled(self.IMAGE_COLS_MAX, self.IMAGE_ROWS_MAX)
            self.filterImg.setPixmap(QPixmap.fromImage(self.imageF))

        #print "update"
        pos = self.sourceImg.getMousePos()
        if pos != None:
            #print pos
            x_ini = (self.sourceImg.width()*self.ZOOM_X*pos.x())/self.sourceImg.width()
            y_ini = (self.sourceImg.height()*self.ZOOM_X*pos.y())/self.sourceImg.height()
            rect = QRect(x_ini-100,y_ini-100,200,200)

            #print 'orig', pos.x(), ",", pos.y(), ",", self.sourceImg.size()
            #print 'scale', x_ini, ",", y_ini

            #self.crop.setPixmap(QPixmap.fromImage(self.image.copy(rect).scaled(1000,1000)))

            #print self.sourceImg.pixmap().size()
            im2 = self.image.copy().scaled(self.sourceImg.width()*self.ZOOM_X,self.sourceImg.height()*self.ZOOM_X)
            self.crop.setPixmap(QPixmap.fromImage(im2.copy(rect)))
            #print self.crop.pixmap().size()
            
            pos = self.sourceImg.getMousePos()
            #print pos
            rgb = QColor(self.image.pixel(pos))
            self.tootippixel.setStyleSheet("background: rgb(" + str(rgb.red()) + "," + str(rgb.green()) + "," + str(rgb.blue()) + "); border: 1px solid;")
            self.tootippixel.setGeometry(pos.x(), pos.y()+52, 20,20)
            self.pixel.setStyleSheet("background: rgb(" + str(rgb.red()) + "," + str(rgb.green()) + "," + str(rgb.blue()) + ");border: 1px solid;")
            text = "XY ["+str(pos.x())+","+str(pos.y())+"]\nrgb(" + str(rgb.red()) + "," + str(rgb.green()) + "," + str(rgb.blue()) + ")"
            self.rgbVal.setText(text)

    def getCamera(self):
        return self.camera

    def setCamera(self,camera):
        print camera
        self.camera = camera

    def getFilterName(self):
        return self.filt

    def setFilterName(self,filt):
        self.filt = filt

    def closeEvent(self, event):
        self.camera.stop()
        event.accept()
            

        



