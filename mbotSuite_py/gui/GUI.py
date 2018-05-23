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


from PyQt5.QtCore import pyqtSignal, QBasicTimer
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QPushButton, QGridLayout
from .ui_gui import Ui_MainWindow
from .teleopWidget import TeleopWidget
from .cameraWidget import CameraWidget
from .communicator import Communicator
from .logoWidget import LogoWidget

from jderobotTypes import CMDVel


class MainWindow(QMainWindow, Ui_MainWindow):

    updGUI = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.teleop = TeleopWidget(self)
        self.mainLayout.addWidget(self.teleop, 0,0,1,4)
        self.teleop.setVisible(True)

        self.updGUI.connect(self.updateGUI)

        self.cameraWidget = CameraWidget(self, 0)
        self.irlWidget = CameraWidget(self, 1)
        self.irrWidget = CameraWidget(self, 2)

        self.cameraCommunicator = Communicator()
        self.trackingCommunicator = Communicator()


    def setCamera(self, camera, irl, irr):
        self.camera = camera
        self.irl = irl
        self.irr = irr
        self.cameraWidget.show()
        self.irlWidget.show()
        self.irrWidget.show()

    def getCamera(self):
        return self.camera

    def getIRL(self):
        return self.irl

    def getIRR(self):
        return self.irr

    def setMotors(self, motors):
        self.motors = motors

    def setSonar(self, sonar):
        self.sonar = sonar

    def getMotors(self):
        return self.motors

    def updateGUI(self):
        self.cameraWidget.imageUpdate.emit()
        self.irlWidget.imageUpdate.emit()
        self.irrWidget.imageUpdate.emit()

        data = self.sonar.getSonarData()
        self.pbar.setValue(data.range*100)
        sonar_range = round(data.range,2)
        self.SonarValue.setText(str(sonar_range)+"m")

    def setXYValues(self, newX, newY):
        self.XValue.setText(str(newX))
        self.YValue.setText(str(newY))
        if (self.motors):
            vel = CMDVel()
            myW=-newX*self.motors.getMaxW()
            myV=-newY*self.motors.getMaxV()
            vel.vx = myV
            vel.az = myW
            self.motors.sendVelocities(vel)

