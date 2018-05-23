# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_gui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(430, 400)
        MainWindow.setMinimumSize(QtCore.QSize(430, 400))
        MainWindow.setMaximumSize(QtCore.QSize(800, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        #self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 361, 301))     
        #self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.mainLayout = QtWidgets.QGridLayout(self.centralwidget)
        #self.tlLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        #self.tlLayout.setObjectName("tlLayout")
        self.XLabel = QtWidgets.QLabel()
        self.XLabel.setGeometry(QtCore.QRect(20, 340, 21, 21))
        self.XLabel.setObjectName("XLabel")
        self.YLabel = QtWidgets.QLabel()
        self.YLabel.setGeometry(QtCore.QRect(130, 340, 21, 21))
        self.YLabel.setObjectName("YLabel")
        self.XValue = QtWidgets.QLabel()
        self.XValue.setGeometry(QtCore.QRect(40, 340, 41, 21))
        self.XValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.XValue.setObjectName("XValue")
        self.YValue = QtWidgets.QLabel()
        self.YValue.setGeometry(QtCore.QRect(150, 340, 41, 21))
        self.YValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.YValue.setObjectName("YValue")
        self.SonarLabel = QtWidgets.QLabel()
        self.SonarLabel.setGeometry(QtCore.QRect(130, 340, 21, 21))
        self.SonarLabel.setObjectName("SonarLabel")
        self.SonarValue = QtWidgets.QLabel()
        self.SonarValue.setGeometry(QtCore.QRect(40, 340, 41, 21))
        self.SonarValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.SonarValue.setObjectName("SonarValue")
        self.mainLayout.addWidget(self.XLabel,1,0)
        self.mainLayout.addWidget(self.XValue,1,1)
        self.mainLayout.addWidget(self.YLabel,2,0)
        self.mainLayout.addWidget(self.YValue,2,1)
        self.mainLayout.addWidget(self.SonarLabel,1,3)
        self.mainLayout.addWidget(self.SonarValue,1,5)

        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setOrientation(QtCore.Qt.Vertical)
        self.pbar.setGeometry(200, 25, 30, 40)
        self.pbar.setTextVisible(False)
        self.pbar.setRange(30, 400)
        self.mainLayout.addWidget(self.pbar,0,5)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)   
        
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Basic Component py"))
        self.XLabel.setText(_translate("MainWindow", "X:"))
        self.YLabel.setText(_translate("MainWindow", "Y:"))
        self.XValue.setText(_translate("MainWindow", "0"))
        self.YValue.setText(_translate("MainWindow", "0"))
        self.SonarLabel.setText(_translate("MainWindow", "Range:"))
        self.SonarValue.setText(_translate("MainWindow", "0"))


import resources_rc
