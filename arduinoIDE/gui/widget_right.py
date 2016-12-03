
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gui.customLabel import ClickableLabel
from gui.fade import Fader
from PyQt5.QtGui import QPixmap, QColor


import time

class RightWidget(QWidget):

	def __init__(self, parent):
		super(RightWidget, self).__init__()

		self.parent = parent
		self.flag = 0
		self.initUI()	
		
	def initUI(self):

		self.rightLayout = QVBoxLayout(self)
		self.rightLayout.setObjectName("rightLayout")
		

		# ---------------------------------- RIGHT WIDGET  --------------------------------------

		self.imageLabel = ClickableLabel(self)
		self.imageLabel.setObjectName("ClickableLabel")
		self.imageLabel.setPixmap(QPixmap("gui/images/Disabled.png").scaled(800,600,Qt.KeepAspectRatio))
		self.imageLabel.setScaledContents(True)
		self.imageLabel.setMouseTracking(True)
		self.imageLabel.setGeometry(QRect(0, 0, 800, 600))
		self.imageLabel.mousePos.connect(self.iMousePose)
		self.imageLabel.mouseClick.connect(self.iMouseClicked)

		self.backLabel = ClickableLabel(self)
		self.backLabel.setObjectName("BackLabel")
		self.backLabel.setText("Back")
		self.imageLabel.setGeometry(QRect(0, 0, 50, 10))
		self.backLabel.setVisible(False)
		self.backLabel.mouseClick.connect(self.bMouseClicked)


		self.rightLayout.addWidget(self.imageLabel)


		# ---------------------------------- END RIGHT WIDGET  --------------------------------------

		self.setLayout(self.rightLayout)


	def iMousePose(self):

		if self.flag == 0:
			_x = self.imageLabel.getX()
			_y = self.imageLabel.getY()

			pos = self.imageLabel.height()/3 * 2
			if (_y < self.imageLabel.height()/3 * 2):
				print("top")
			else:
				print("bottom")

			rgb = self.imageLabel.pixmap().toImage().pixel(_x,_y)
			rgb = QColor(rgb)
			print(_x,",",_y,":",rgb.red(),rgb.blue(),rgb.green())

			if  _y < pos:
				self.selectedBoard = 0
				self.imageLabel.setPixmap(QPixmap("gui/images/TopBoard.png"))
			elif _y > pos:
				self.selectedBoard = 1
				self.imageLabel.setPixmap(QPixmap("gui/images/BottomBoard.png"))
			elif rgb.red() == 0 and rgb.blue() == 0 and rgb.green() == 0:
				self.selectedBoard = -1
				self.imageLabel.setPixmap(QPixmap("gui/images/Disabled.png"))

	

	def iMouseClicked(self):

		fade = Fader()
		fade.configFade(self.imageLabel, 1, 0, 500)

		if self.selectedBoard == 0:
			print("Arduino Control Selected")
			self.backLabel.setVisible(True)
			self.imageLabel.setPixmap(QPixmap("gui/images/TopBoardCloseup.png"))
			fade.fadeIn()
			self.parent.changeWidget.emit(0)
		elif self.selectedBoard == 1:
			print("Arduino Motor Selected")
			self.backLabel.setVisible(True)
			self.imageLabel.setPixmap(QPixmap("gui/images/BottomBoardCloseup.png"))
			fade.fadeIn()
			self.parent.changeWidget.emit(1)
		else:
			print("No board selected")


		self.flag= 1


	def bMouseClicked(self):
		
		self.flag = 0
		self.imageLabel.setPixmap(QPixmap("gui/images/Disabled.png"))
		self.backLabel.setVisible(False)
		self.parent.changeWidget.emit(-1)




		





