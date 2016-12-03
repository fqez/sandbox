
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class WidgetMotor(QWidget):

	def __init__(self, parent):
		super(WidgetMotor, self).__init__()

		self.parent = parent
		self.initUI()	
		
	def initUI(self):

		'''
		right and left layouts main window

		LeftUpWidget -> Arduino Robot Control, only digital sensors/actuators and analog embeded ones
		LeftDownWidget -> Arduino Robot Motor, only analog sensors/actuators

		LeftUpWidget sensors/actuators (E = Embeded): LEDs, Light Sensors, Buzzer (E), Potentiometer (E), Keys (E)
		LeftDownWidget sensors/actuators (E = Embeded): Motors (E), IR Sensors (E), Ultrasound, Servo 

		'''
		self.leftLayoutDown = QVBoxLayout(self)
		self.leftLayoutDown.setObjectName("leftLayoutDown")


		# ----------------------- LEFT WIDGET ARDUINO MOTOR (Down) -------------------------

		'''motors layout (leftDown)'''
		self.motorsGroupBox = QGroupBox()
		self.motorsGroupBox.setTitle("Motors")
		self.motorsLayout = QGridLayout()
		self.motorsLayout.setObjectName("motorsLayout")
		self.button_motors = QPushButton("Play!")
		self.motorsLayout.addWidget(self.button_motors,0,0)
		self.motorsGroupBox.setLayout(self.motorsLayout)

		'''IR Sensors layout (leftDown)'''
		self.irSensorsGroupBox = QGroupBox()
		self.irSensorsGroupBox.setTitle("IR Sensors")
		self.irSensorsLayout = QGridLayout()
		self.irSensorsLayout.setObjectName("irSensorsLayout")
		self.button_irSensors = QPushButton("Play!")
		self.irSensorsLayout.addWidget(self.button_irSensors,0,0)
		self.irSensorsGroupBox.setLayout(self.irSensorsLayout)

		'''ultrasound sensors (LeftDown)'''
		self.ultrasoundGroupBox = QGroupBox()
		self.ultrasoundGroupBox.setTitle("ultrasound")
		self.ultrasoundLayout = QGridLayout()
		self.ultrasoundLayout.setObjectName("ultrasoundLayout")
		self.textbox_ultrasound = QLineEdit()
		self.textbox_ultrasound.setMaximumSize(50,40)
		self.button_ultrasound = QPushButton("Light!")
		self.ultrasoundLayout.addWidget(self.textbox_ultrasound,0,0)
		self.ultrasoundLayout.addWidget(self.button_ultrasound,0,1)
		self.ultrasoundGroupBox.setLayout(self.ultrasoundLayout)

		self.leftLayoutDown.addWidget(self.motorsGroupBox)
		self.leftLayoutDown.addWidget(self.irSensorsGroupBox)
		self.leftLayoutDown.addWidget(self.ultrasoundGroupBox)

		# ----------------------- END LEFT WIDGET ARDUINO MOTOR (Down) -------------------------

		self.setLayout(self.leftLayoutDown)

		'''signals'''
		self.button_motors.clicked.connect(lambda:self.motorsButtonClicked())
		self.button_irSensors.clicked.connect(lambda:self.irSensorsButtonClicked())
		self.button_ultrasound.clicked.connect(lambda:self.ultrasoundButtonClicked())


	def motorsButtonClicked(self):
		print("Motors click")

	def irSensorsButtonClicked(self):
		print("IR sensors click")

	def ultrasoundButtonClicked(self):
		print("ultrasound click")
		self.checkValue(self.textbox_ultrasound)

	def checkValue(self, linedit):
		try:
			_val = linedit.text()
			if _val != '':
				_val = int(_val)
				if _val < 0 or _val > 7:
					self.warningDialog("Buttons out of range!", "This board has only 8 pin (0-7), please enter a valid value")
		
		except ValueError:
			self.warningDialog("You entered a non-numeric value", "Please enter a valid number (0-7)")