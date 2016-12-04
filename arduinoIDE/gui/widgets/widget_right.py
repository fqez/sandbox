
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gui.customLabel import ClickableLabel
from gui.fade import *
from PyQt5.QtGui import QPixmap, QColor

class RightWidget(QWidget):

	def __init__(self, parent):
		super(RightWidget, self).__init__()

		self.parent = parent
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

		self.rightLayout.addWidget(self.imageLabel)

		# ---------------------------------- END RIGHT WIDGET  --------------------------------------

		self.setLayout(self.rightLayout)


	def iMousePose(self):

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

		if self.selectedBoard == 0:
			print("Arduino Control Selected")
			self.parent.changeWidget.emit(0)
			self.parent.changeWidget.emit(2)

		elif self.selectedBoard == 1:
			print("Arduino Motor Selected")
			self.parent.changeWidget.emit(1)
			self.parent.changeWidget.emit(3)

		else:
			print("No board selected")
			self.parent.changeWidget.emit(-1)


class RightWidgetUp(QWidget):

	def __init__(self, parent):
		super(RightWidgetUp, self).__init__()

		self.parent = parent
		self.initUI()	
		
	def initUI(self):

		self.rightLayoutUp = QVBoxLayout(self)
		self.rightLayoutUp.setObjectName("rightLayoutUp")
		

		# ---------------------------------- RIGHT WIDGET Up  --------------------------------------

		self.topLabel = ClickableLabel(self)
		self.topLabel.setObjectName("TopLabel")
		self.topLabel.setPixmap(QPixmap("gui/images/DisabledTopBoard.png").scaled(800,600,Qt.KeepAspectRatio))
		self.topLabel.setScaledContents(True)
		self.topLabel.setMouseTracking(True)
		self.topLabel.setGeometry(QRect(0, 0, 800, 600))
		self.topLabel.mousePos.connect(self.tMousePose)
		self.topLabel.mouseClick.connect(self.tMouseClicked)
		

		self.backLabel = ClickableLabel(self)
		self.backLabel.setObjectName("BackLabel")
		self.backLabel.setText("Back")
		self.backLabel.setGeometry(QRect(0, 0, 50, 10))
		self.backLabel.mouseClick.connect(self.backMouseClicked)


		self.rightLayoutUp.addWidget(self.backLabel)
		self.rightLayoutUp.addWidget(self.topLabel)

		# ---------------------------------- END RIGHT WIDGET  --------------------------------------

		self.setLayout(self.rightLayoutUp)


	def tMouseClicked(self):
		None

	def tMousePose(self):
		_x = self.topLabel.getX()
		_y = self.topLabel.getY()

		print(_x,",",_y)

		if _x > 234 and _y > 207 and _x < 364 and _y < 394:
			self.topLabel.setPixmap(QPixmap("gui/images/lcd.png").scaled(800,600,Qt.KeepAspectRatio))

	def backMouseClicked(self):
		
		self.parent.changeWidget.emit(-1)


class RightWidgetDown(QWidget):

	def __init__(self, parent):
		super(RightWidgetDown, self).__init__()

		self.parent = parent
		self.initUI()	
		
	def initUI(self):

		self.rightLayoutDown = QVBoxLayout(self)
		self.rightLayoutDown.setObjectName("rightLayoutDown")
		

		# ---------------------------------- RIGHT WIDGET  --------------------------------------

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
		self.backLabel.mouseClick.connect(self.backMouseClicked)


		self.rightLayoutDown.addWidget(self.backLabel)
		self.rightLayoutDown.addWidget(self.bottomLabel)

		# ---------------------------------- END RIGHT WIDGET  --------------------------------------

		self.setLayout(self.rightLayoutDown)


	def bMousePose(self):
		None
	
	def bMouseClicked(self):
		None

	def backMouseClicked(self):
		
		self.parent.changeWidget.emit(-1)




		






		






		





