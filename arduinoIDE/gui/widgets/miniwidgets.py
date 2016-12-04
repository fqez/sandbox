from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class BuzzerWidget(QWidget):
	
	
	def __init__(self,winParent):      
		super(BuzzerWidget, self).__init__()
		self.winParent=winParent
		self.setWindowTitle("Buzzer")
		self.initUI()

	def initUI(self):
		self.setMinimumSize(500,300)
		self.setMaximumSize(500,300)

		self.layout=QGridLayout()  
		self.button = QPushButton("Pulsa")
		self.label = QLabel()
		self.label.setText("Buzzeeeeeer")
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.button)
		self.button.clicked.connect(self.on_button_clicked)
		self.setLayout(self.layout)

	def on_button_clicked(self):
		self.label.setText("@@!@#!")
		

