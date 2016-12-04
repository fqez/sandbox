
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from gui.widgets.miniwidgets import *


from dialogs import Dialog

class WidgetControl(QWidget):

	def __init__(self, parent):
		super(WidgetControl, self).__init__()

		self.parent = parent
		self.initUI()	
		
	def initUI(self):

		'''init mini widgets'''
		self.buzzer = BuzzerWidget(self)
		self.buzzer.setVisible(False)


		'''
		left Up layout 

		LeftUpWidget -> Arduino Robot Control, only digital sensors/actuators and analog embeded ones
		LeftDownWidget -> Arduino Robot Motor, only analog sensors/actuators

		LeftUpWidget sensors/actuators (E = Embeded): LEDs, Light Sensors, Buzzer (E), Potentiometer (E), Keys (E)
		LeftDownWidget sensors/actuators (E = Embeded): Motors (E), IR Sensors (E), Ultrasound, Servo 

		'''
		self.leftLayoutUp = QVBoxLayout(self)
		self.leftLayoutUp.setObjectName("leftLayoutUp")

		self.vSpacer = QSpacerItem(30, 300, QSizePolicy.Ignored, QSizePolicy.Ignored);


		# ----------------------- LEFT WIDGET ARDUINO CONTROL (Up) -------------------------
		'''leds layout (leftUp)'''
		self.ledGroupBox = QGroupBox()
		self.ledGroupBox.setTitle("LEDs")
		self.ledsLayout = QGridLayout()
		self.ledsLayout.setObjectName("ledsLayout")
		self.textbox_leds = QLineEdit()
		self.textbox_leds.setMaximumSize(50,40)
		self.button_leds = QPushButton("Light!")
		self.button_leds.setObjectName("LEDButton")
		self.ledsLayout.addWidget(self.textbox_leds,0,0)
		self.ledsLayout.addWidget(self.button_leds,0,1)
		self.ledGroupBox.setLayout(self.ledsLayout) 

		'''buzzer layout (leftUp)'''
		self.buzzerGroupBox = QGroupBox()
		self.buzzerGroupBox.setTitle("Buzzer")
		self.buzzerLayout = QGridLayout()
		self.buzzerLayout.setObjectName("buzzerLayout")
		self.button_buzzer = QPushButton("Play!")
		self.buzzerLayout.addWidget(self.button_buzzer,0,0)
		self.buzzerGroupBox.setLayout(self.buzzerLayout)

		'''Light sensors (LeftUp)'''
		self.lightSensorGroupBox = QGroupBox()
		self.lightSensorGroupBox.setTitle("Light Sensor")
		self.lightSensorLayout = QGridLayout()
		self.lightSensorLayout.setObjectName("lightSensorLayout")
		self.textbox_lightSensor = QLineEdit()
		self.textbox_lightSensor.setMaximumSize(50,40)
		self.button_lightSensor = QPushButton("Light!")
		self.lightSensorLayout.addWidget(self.textbox_lightSensor,0,0)
		self.lightSensorLayout.addWidget(self.button_lightSensor,0,1)
		self.lightSensorGroupBox.setLayout(self.lightSensorLayout)

		'''Potentiometer layout (leftUp)'''
		self.potentiometerGroupBox = QGroupBox()
		self.potentiometerGroupBox.setTitle("Potentiometer")
		self.potentiometerLayout = QGridLayout()
		self.potentiometerLayout.setObjectName("potentiometerLayout")
		self.button_potentiometer = QPushButton("Play!")
		self.potentiometerLayout.addWidget(self.button_potentiometer,0,0)
		self.potentiometerGroupBox.setLayout(self.potentiometerLayout)

		'''Keys layout (leftUp)'''
		self.keysGroupBox = QGroupBox()
		self.keysGroupBox.setTitle("Keys")
		self.keysLayout = QGridLayout()
		self.keysLayout.setObjectName("keysLayout")
		self.button_keys = QPushButton("Play!")
		self.keysLayout.addWidget(self.button_keys,0,0)
		self.keysGroupBox.setLayout(self.keysLayout)

		self.leftLayoutUp.addWidget(self.ledGroupBox)
		self.leftLayoutUp.addWidget(self.buzzerGroupBox)
		self.leftLayoutUp.addWidget(self.lightSensorGroupBox)
		self.leftLayoutUp.addWidget(self.potentiometerGroupBox)
		self.leftLayoutUp.addWidget(self.keysGroupBox)
		#self.leftLayoutUp.addItem(self.vSpacer)

		# ----------------------- END LEFT WIDGET ARDUINO CONTROL (Up) -------------------------

		self.setLayout(self.leftLayoutUp)

		'''signals'''
		self.button_leds.clicked.connect(self.ledButtonClicked)
		self.button_buzzer.clicked.connect(self.buzzerButtonClicked)
		self.button_lightSensor.clicked.connect(self.lightSensorButtonClicked)
		self.button_potentiometer.clicked.connect(self.potentiometerButtonClicked)
		self.button_keys.clicked.connect(self.keysButtonClicked)

	def ledButtonClicked(self):
		print("Leds click")
		self.checkValue(self.textbox_leds)	

	def buzzerButtonClicked(self):
		print("Buzzer click")
		
		self.buzzer.show()

	def lightSensorButtonClicked(self):
		print("Light sensor click")
		self.checkValue(self.textbox_lightSensor)

	def potentiometerButtonClicked(self):
		print("Potentiometer click")

	def keysButtonClicked(self):
		print("Keys click")


	def checkValue(self, linedit):

		dialog = Dialog()
		try:
			_val = linedit.text()
			if _val != '':
				_val = int(_val)
				if _val < 0 or _val > 7:
					dialog.warningDialog("Buttons out of range!", "This board has only 8 pin (0-7), please enter a valid value")
		
		except ValueError:
			dialog.warningDialog("You entered a non-numeric value", "Please enter a valid number (0-7)")