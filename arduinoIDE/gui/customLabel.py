from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ClickableLabel(QLabel):


	mousePos = pyqtSignal()
	mouseClick = pyqtSignal()
	def __init(self, parent):
		QLabel.__init__(self, parent)
		self._x = 0
		self._y = 0

	def mouseMoveEvent(self, ev):

		self._x = ev.x()
		self._y = ev.y()
		self.mousePos.emit()

	def mousePressEvent(self,ev):

		self.mouseClick.emit()
		
	def getX(self):
		return self._x

	def getY(self):
		return self._y