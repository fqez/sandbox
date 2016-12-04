from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class BuzzerWidget(QWidget):
	
	
	def __init__(self,winParent):      
		super(ControlWidget, self).__init__()
		self.winParent=winParent

		self.initUI()

	def initUI(self):
		None