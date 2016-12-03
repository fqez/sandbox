
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gui.customLabel import ClickableLabel
from gui.fade import *
from PyQt5.QtGui import QPixmap, QColor

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

		self.topLabel = ClickableLabel(self)
		self.topLabel.setObjectName("TopLabel")
		self.topLabel.setPixmap(QPixmap("gui/images/DisabledTopBoard.png").scaled(800,600,Qt.KeepAspectRatio))
		self.topLabel.setScaledContents(True)
		self.topLabel.setMouseTracking(True)
		self.topLabel.setGeometry(QRect(0, 0, 800, 600))
		self.topLabel.mousePos.connect(self.tMousePose)
		self.topLabel.mouseClick.connect(self.tMouseClicked)

		self.bottomLabel = ClickableLabel(self)
		self.bottomLabel.setObjectName("BottomLabel")
		self.bottomLabel.setPixmap(QPixmap("gui/images/DisabledBottomBoard.png").scaled(800,600,Qt.KeepAspectRatio))
		self.bottomLabel.setScaledContents(True)
		self.bottomLabel.setMouseTracking(True)
		self.bottomLabel.setGeometry(QRect(0, 0, 800, 600))
		self.bottomLabel.mousePos.connect(self.bMousePose)
		self.bottomLabel.mouseClick.connect(self.bMouseClicked)

		self.backLabel = ClickableLabel(self)
		self.backLabel.setObjectName("BackLabel")
		self.backLabel.setText("Back")
		self.backLabel.setGeometry(QRect(0, 0, 50, 10))
		self.backLabel.setVisible(False)
		self.backLabel.mouseClick.connect(self.backMouseClicked)


		self.rightLayout.addWidget(self.backLabel)
		self.rightLayout.addWidget(self.imageLabel)
		self.rightLayout.addWidget(self.topLabel)
		self.rightLayout.addWidget(self.bottomLabel)

		self.imageLabel.setVisible(True)
		self.topLabel.setVisible(False)
		self.bottomLabel.setVisible(False)

		# ---------------------------------- END RIGHT WIDGET  --------------------------------------

		self.setLayout(self.rightLayout)


	def iMousePose(self):

		if self.flag == 0:
			_x = self.imageLabel.getX()
			_y = self.imageLabel.getY()

			# calculate the y coord corresponding to 2/3 of the image (more or less where the board image changes)
			# TODO
			# 	calculate the ellipse area of each board
			pos = (self.imageLabel.height()/3) * 2
			
			rgb = QColor(self.imageLabel.pixmap().toImage().pixel(_x,_y))
			print(_x,",",_y,":",rgb.red(),rgb.blue(),rgb.green())

			if  _y < pos:
				self.selectedBoard = 0
				self.imageLabel.setPixmap(QPixmap("gui/images/TopBoard.png"))
			elif _y > pos:
				self.selectedBoard = 1
				self.imageLabel.setPixmap(QPixmap("gui/images/BottomBoard.png"))
			elif rgb.red() == 0  and rgb.green() == 0 and rgb.blue() == 0:
				self.selectedBoard = -1
				self.imageLabel.setPixmap(QPixmap("gui/images/Disabled.png"))

	def iMouseClicked(self):

		fadei = FadeIn(self.topLabel, 1, 0, 500)

		if self.selectedBoard == 0:
			print("Arduino Control Selected")
			self.backLabel.setVisible(True)
			self.imageLabel.setVisible(False)
			self.topLabel.setVisible(True)
			fadei.fade()
			self.parent.changeWidget.emit(0)

		elif self.selectedBoard == 1:
			print("Arduino Motor Selected")
			self.backLabel.setVisible(True)
			self.imageLabel.setVisible(False)
			self.bottomLabel.setVisible(True)
			fadei.fade()
			self.parent.changeWidget.emit(1)

		else:
			print("No board selected")
			self.parent.changeWidget.emit(-1)


		self.flag= 1

	def tMousePose(self):
		None
	
	def tMouseClicked(self):
		None

	def bMousePose(self):
		None
	
	def bMouseClicked(self):
		None

	def backMouseClicked(self):
		
		fadei = FadeIn(self.imageLabel, 1, 0, 500)

		self.flag = 0
		self.imageLabel.setVisible(True)
		self.backLabel.setVisible(False)
		self.topLabel.setVisible(False)
		self.bottomLabel.setVisible(False)
		fadei.fade()
		self.parent.changeWidget.emit(-1)




		





