from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ClickableLabel(QLabel):


	mousePos = pyqtSignal()
	mouseClickL = pyqtSignal()
	mouseClickR = pyqtSignal()
	def __init(self, parent):
		QLabel.__init__(self, parent)
		self._x = 0
		self._y = 0

	def mouseMoveEvent(self, ev):

		self._x = ev.x()
		self._y = ev.y()
		self.mousePos.emit()

	def mousePressEvent(self,ev):

		if ev.button() == Qt.LeftButton:
			self.mouseClickL.emit()
		elif ev.button() == Qt.RightButton:	
			self.mouseClickR.emit()
					
	def getX(self):
		return self._x

	def getY(self):
		return self._y