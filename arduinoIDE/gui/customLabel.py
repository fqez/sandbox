from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ClickableLabel(QLabel):


	mousePos = pyqtSignal()
	def __init(self, parent, gui):
		QLabel.__init__(self, parent)
		self._x = 0
		self._y = 0
		self.gui = gui

	def mouseMoveEvent(self, ev):

		self._x = ev.x()
		self._y = ev.y()
		self.mousePos.emit()
		print(self._x,",",self._y)
 		
	def getX(self):
		return self._x

	def getY(self):
		return self._y