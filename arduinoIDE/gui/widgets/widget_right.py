
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
		self.imageLabel.mouseClickL.connect(self.iMouseClicked)

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
		self.setContextMenuPolicy(Qt.CustomContextMenu);
		self.customContextMenuRequested[QPoint].connect(self.contextMenuRequested)
	
		
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
		self.topLabel.mouseClickL.connect(self.tMouseClickedL)
		self.topLabel.mouseClickR.connect(self.tMouseClickedR)

		self.backLabel = ClickableLabel(self)
		self.backLabel.setObjectName("BackLabel")
		self.backLabel.setText("Back")
		self.backLabel.setGeometry(QRect(0, 0, 50, 10))
		self.backLabel.mouseClickL.connect(self.backMouseClicked)


		self.rightLayoutUp.addWidget(self.backLabel)
		self.rightLayoutUp.addWidget(self.topLabel)

		# ---------------------------------- END RIGHT WIDGET  --------------------------------------

		self.setLayout(self.rightLayoutUp)


	def tMouseClickedL(self):
		None

	def tMouseClickedR(self):
		None

	def tMousePose(self):
		_x = self.topLabel.getX()
		_y = self.topLabel.getY()

		print(_x,",",_y, self.topLabel.size())

		# if the region in circular. To make it easy it will be rectangular for now.
		# Hardcoded coordinates from the image in the GUI: Buzzer_center(422,238), radius 40
		# to check if the mouse is inside the buzzer we apply the following ecuation
		# (x - center_x)^2 + (y - center_y)^2 < radius^2
		#buz = (_x - 422)**2 + (_y - 238)**2 < 40**2

		# normalized mouse position between 0% and 100%. This way we can reescale the image, and get the same regions
		# Te reference image size was (600x600 px). Normalized(x,y) = (x,y) * 100 / 600
		#
		#	LCD -> normalized area between (39%,34.5%) and (60.6%,65.6%)
		#	Buzzer-> normalized area between (62.8%,32.6%) and (77.3%,46%)
		#	Keys -> normalized area between (63%,47.5%) and (85%,71.6%)
		#	Potentiometer -> normalized area between (15.8%,63%) and (20.8%,69.5%)
		#	TK0 -> normalized area between (90.8%,47.7%) and (95.0%,53.0%)
		#	TK1 -> normalized area between (77.2%,17.5%) and (83.3%,22.5%)
		#	TK2 -> normalized area between (47.2%,5.8%) and (53.0%,9.5%)
		#	TK3 -> normalized area between (15.5%,17.8%) and (22.8%,22.3%)
		#	TK4 -> normalized area between (4.7%,47.3%) and (9.3%,53.0%)
		#	TK5 -> normalized area between (17.2%,78.0%) and (22.3%,82.7%)
		#	TK6 -> normalized area between (47.3%,91.5%) and (53.0%,95.0%)
		#	TK7 -> normalized area between (77.0%,78.0%) and (82.7%,82.2%)
		#
		x_p = _x * 100 / self.topLabel.size().width()
		y_p = _y * 100 / self.topLabel.size().height()

		# TODO: Make this more clean, create a class for this kind of mapping
		if x_p > 39 and y_p > 34.5 and x_p < 60.6 and y_p < 65.6:
			self.topLabel.setPixmap(QPixmap("gui/images/LCD.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 62.8 and y_p > 32.6 and x_p < 77.3 and y_p < 46:
			self.topLabel.setPixmap(QPixmap("gui/images/Buzzer.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 63 and y_p > 47.5 and x_p < 85 and y_p < 71.6:
			self.topLabel.setPixmap(QPixmap("gui/images/Keys.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 15.8 and y_p > 63 and x_p < 20.8 and y_p < 69.5:
			self.topLabel.setPixmap(QPixmap("gui/images/Potentiometer.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 90.8 and y_p > 47.7 and x_p < 95.0 and y_p < 53.0 :
			self.topLabel.setPixmap(QPixmap("gui/images/TK0.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 77.2 and y_p > 17.5 and x_p < 83.3 and y_p < 22.5 :
			self.topLabel.setPixmap(QPixmap("gui/images/TK1.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 47.2 and y_p > 5.8 and x_p < 53.0 and y_p < 9.5 :
			self.topLabel.setPixmap(QPixmap("gui/images/TK2.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 15.5 and y_p > 17.8 and x_p < 22.8 and y_p < 22.3 :
			self.topLabel.setPixmap(QPixmap("gui/images/TK3.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 4.7 and y_p > 47.3 and x_p < 9.3 and y_p < 53.0 :
			self.topLabel.setPixmap(QPixmap("gui/images/TK4.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 17.2 and y_p > 78.0 and x_p < 22.3 and y_p < 82.7 :
			self.topLabel.setPixmap(QPixmap("gui/images/TK5.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 47.3 and y_p > 91.5 and x_p < 53.0 and y_p < 95.0 :
			self.topLabel.setPixmap(QPixmap("gui/images/TK6.png").scaled(800,600,Qt.KeepAspectRatio))
		elif x_p > 77.0 and y_p > 78.0 and x_p < 82.7 and y_p < 82.2 :
			self.topLabel.setPixmap(QPixmap("gui/images/TK7.png").scaled(800,600,Qt.KeepAspectRatio))
		else:
			self.topLabel.setPixmap(QPixmap("gui/images/DisabledTopBoard.png").scaled(800,600,Qt.KeepAspectRatio))

	def backMouseClicked(self):
		self.parent.changeWidget.emit(-1)

	def contextMenuRequested(self,point):
    
		menu = QMenu()
		    
		action1 = menu.addAction("Set Size 100x100")
		action2 = menu.addAction("Set Size 500x500") 

		action2.triggered.connect(self.slotShow500x500)
		action1.triggered.connect(self.slotShow100x100)
		menu.exec_(self.mapToGlobal(point))
		
	def slotShow500x500(self):
		self.setFixedSize(500,500)   
		self.show()

	def slotShow100x100(self):
		self.setFixedSize(100,100)   
		self.show()


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
		self.bottomLabel.mouseClickL.connect(self.bMouseClickedL)
		self.bottomLabel.mouseClickR.connect(self.bMouseClickedR)

		self.backLabel = ClickableLabel(self)
		self.backLabel.setObjectName("BackLabel")
		self.backLabel.setText("Back")
		self.backLabel.setGeometry(QRect(0, 0, 50, 10))
		self.backLabel.mouseClickL.connect(self.backMouseClicked)


		self.rightLayoutDown.addWidget(self.backLabel)
		self.rightLayoutDown.addWidget(self.bottomLabel)

		# ---------------------------------- END RIGHT WIDGET  --------------------------------------

		self.setLayout(self.rightLayoutDown)


	def bMousePose(self):
		None
	
	def bMouseClickedL(self):
		None

	def bMouseClickedR(self):
		None

	def backMouseClicked(self):
		
		self.parent.changeWidget.emit(-1)




		






		






		





