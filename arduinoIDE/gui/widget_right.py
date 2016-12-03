
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gui.customLabel import ClickableLabel
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

		#self.buttonAux = QPushButton("Switch")
		#self.buttonAux.clicked.connect(lambda:self.switchWidget())
		#self.rightLayout.addWidget(self.buttonAux)

		self.imageLabel = ClickableLabel(self)
		self.imageLabel.setObjectName("ClickableLabel")
		self.imageLabel.setPixmap(QPixmap("gui/images/Disabled.png").scaled(800,600,Qt.KeepAspectRatio))
		self.imageLabel.setScaledContents(True)
		self.imageLabel.setMouseTracking(True)
		self.imageLabel.setGeometry(QRect(0, 0, 800, 600))
		self.imageLabel.mousePos.connect(self.mousePose)
		self.imageLabel.mouseClick.connect(self.mouseClicked)

		self.rightLayout.addWidget(self.imageLabel)


		# ---------------------------------- END RIGHT WIDGET  --------------------------------------

		self.setLayout(self.rightLayout)


	def mousePose(self):
		_x = self.imageLabel.getX()
		_y = self.imageLabel.getY()

		if (_y < self.imageLabel.height()/4 * 3):
			print("top")
		else:
			print("bottom")

		rgb = self.imageLabel.pixmap().toImage().pixel(_x,_y)
		rgb = QColor(rgb)
		print(_x,",",_y,":",rgb.red(),rgb.blue(),rgb.green())

		if rgb.red() == 22 and rgb.blue() == 71 and rgb.green() == 69:
			self.selectedBoard = 0
			self.imageLabel.setPixmap(QPixmap("gui/images/TopBoard.png"))
		elif rgb.red() == 0 and rgb.blue() == 0 and rgb.green() == 0:
			self.selectedBoard = -1
			self.imageLabel.setPixmap(QPixmap("gui/images/Disabled.png"))
		else:
			self.selectedBoard = -1
			self.imageLabel.setPixmap(QPixmap("gui/images/BottomBoard.png"))

	def mouseClicked(self):
		if self.selectedBoard == 0:
			print("Arduino Control Selected")
		elif self.selectedBoard == 1:
			print("Arduino Motor Selected")
		else:
			print("No board selected")