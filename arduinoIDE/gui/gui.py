
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QColor

from gui.customLabel import ClickableLabel

class MainWindow(QMainWindow):

	updateGUI=pyqtSignal()
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.setWindowTitle("Arduino Robot")
		self.setMinimumSize(1000,700)
		self.setMaximumSize(1000,700)
		self.selectedBoard = -1	#-1:no selection; 0: top; 1: bottom
		self.initUI()


	def initUI(self):  

		self.setStyleSheet(self.readStyleSheet("style.stylesheet"))
		self.initMenuBar()

		self.hSpacer = QSpacerItem(30, 30, QSizePolicy.Ignored, QSizePolicy.Ignored);

		'''main layout'''
		self.horizontalLayoutWidget = QWidget(self)
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.mainLayout = QHBoxLayout(self.horizontalLayoutWidget)
		self.mainLayout.setObjectName("mainLayout")


		'''
		right and left layouts main window

		LeftUpWidget -> Arduino Robot Control, only digital sensors/actuators and analog embeded ones
		LeftDownWidget -> Arduino Robot Motor, only analog sensors/actuators

		LeftUpWidget sensors/actuators (E = Embeded): LEDs, Light Sensors, Buzzer (E), Potentiometer (E), Keys (E)
		LeftDownWidget sensors/actuators (E = Embeded): Motors (E), IR Sensors (E), Ultrasound, Servo 

		'''
		self.leftWidgetUp = QWidget()
		self.leftWidgetDown = QWidget()
		self.rightWidget = QWidget()

		self.rightLayout = QVBoxLayout()
		self.rightLayout.setObjectName("rightLayout")
		self.leftLayoutUp = QVBoxLayout()
		self.leftLayoutUp.setObjectName("leftLayoutUp")
		self.leftLayoutDown = QVBoxLayout()
		self.leftLayoutDown.setObjectName("leftLayoutDown")

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

		# ----------------------- END LEFT WIDGET ARDUINO CONTROL (Up) -------------------------

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

		self.leftWidgetUp.setLayout(self.leftLayoutUp)
		self.leftWidgetDown.setLayout(self.leftLayoutDown)
		self.rightWidget.setLayout(self.rightLayout)
		self.mainLayout.addWidget(self.leftWidgetUp, 0)
		self.mainLayout.addWidget(self.leftWidgetDown, 0)
		self.mainLayout.addWidget(self.rightWidget,1)

		self.leftWidgetUp.setVisible(True)
		self.leftWidgetDown.setVisible(False)

		'''signals'''
		self.button_leds.clicked.connect(lambda:self.ledButtonClicked())
		self.button_buzzer.clicked.connect(lambda:self.buzzerButtonClicked())
		self.button_lightSensor.clicked.connect(lambda:self.lightSensorButtonClicked())
		self.button_potentiometer.clicked.connect(lambda:self.potentiometerButtonClicked())
		self.button_keys.clicked.connect(lambda:self.keysButtonClicked())

		self.button_motors.clicked.connect(lambda:self.motorsButtonClicked())
		self.button_irSensors.clicked.connect(lambda:self.irSensorsButtonClicked())
		self.button_ultrasound.clicked.connect(lambda:self.ultrasoundButtonClicked())

		self.setCentralWidget(self.horizontalLayoutWidget)
		self.show()


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

	def readStyleSheet(self, filename):
		'''load custom stylesheet from file'''
		sshFile="gui/"+filename
		sytle = ''
		with open(sshFile,"r") as fh:
			style = fh.read()

		return style

	def initMenuBar(self):
		
		menubar = self.menuBar()
		menubar.setNativeMenuBar(False)       

		'''File Menu'''
		openAction = QAction('Open', self)
		openAction.setShortcut('Ctrl+O')
		openAction.setStatusTip('Open a file')
		openAction.triggered.connect(self.openFile)
 
		closeAction = QAction('Close', self)
		closeAction.setShortcut('Ctrl+Q')
		closeAction.setStatusTip('Close Notepad')
		closeAction.triggered.connect(self.close)

		newAction = QAction('New...', self)
		newAction.setShortcut('Ctrl+N')
		newAction.setStatusTip('New file')
		newAction.triggered.connect(self.newFile)

		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(openAction)        
		fileMenu.addAction(newAction)
		fileMenu.addAction(closeAction)

		'''Examples menus and submenus'''
		sub_control = QMenu('Arduino Control',self)
		sub_motor = QMenu('Arduino Motor',self)
		sub_behaviour = QMenu('Behaviours', self)	# comportamientos: sigue linea, sigue luz...

		sub_sub_leds = QMenu('LEDs', self)
		sub_sub_buzzer = QMenu('Buzzer', self)
		sub_sub_light = QMenu('Light sensors', self)
		sub_sub_potentiometer = QMenu('Potentiometer', self)
		sub_sub_lcd = QMenu('LCD', self)
		sub_sub_keys = QMenu('Keys', self)

		sub_sub_ultrasound = QMenu('Ultrasound', self)
		sub_sub_ir = QMenu('IR sensors', self)
		sub_sub_motors = QMenu('Motors', self)


		# Examples Actions (code)
		turn_on_led = QAction('Key Leds', self)
		turn_on_led.setStatusTip('Turn on a specific LED pushing a key')
		turn_on_led.triggered.connect(lambda:self.loadExample("keys_led"))
		buzz_song = QAction('Play a Song', self)
		buzz_song.setStatusTip('Play a song using the buzzer')
		buzz_song.triggered.connect(lambda:self.loadExample("song_buzzer"))


		ultra_distance = QAction('Read ultrasound', self)
		ultra_distance.setStatusTip('Read values from ultrasonic sensor')
		ultra_distance.triggered.connect(lambda:self.loadExample("ultra_distance"))

		follow_line = QAction('Follow Line', self)
		follow_line.setStatusTip('Follow a black line using IR sensors')
		follow_line.triggered.connect(lambda:self.loadExample("follow_line"))

		#
		# Adding actions to submenus
		#

		# Arduino Control
		sub_sub_leds.addAction(turn_on_led)
		sub_sub_buzzer.addAction(buzz_song)

		# Arduino Motor
		sub_sub_ultrasound.addAction(ultra_distance)

		# Behaviours
		sub_behaviour.addAction(follow_line)


		#
		# Adding submenus to upper menus
		#
		sub_control.addMenu(sub_sub_leds)
		sub_control.addMenu(sub_sub_buzzer)
		sub_control.addMenu(sub_sub_light)
		sub_control.addMenu(sub_sub_potentiometer)
		sub_control.addMenu(sub_sub_lcd)
		sub_control.addMenu(sub_sub_keys)
		sub_motor.addMenu(sub_sub_motors)
		sub_motor.addMenu(sub_sub_ir)
		sub_motor.addMenu(sub_sub_ultrasound)
		#sub_behaviour.addAction(None)

		#
		# Adding submenus to parent menu
		#
		exampleMenu = menubar.addMenu('&Examples')
		exampleMenu.addMenu(sub_control)
		exampleMenu.addMenu(sub_motor)
		exampleMenu.addMenu(sub_behaviour)

		
	def switchWidget(self):
		if self.leftWidgetUp.isVisible():
			self.leftWidgetUp.setVisible(False)
			self.leftWidgetDown.setVisible(True)
		else:
			self.leftWidgetUp.setVisible(True)
			self.leftWidgetDown.setVisible(False)


	'''LoadExamples'''
	def loadExample(self, example_name):	
		print("Loading example", example_name)

	def openFile(self):
		filename, _ = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
 
		fh = ''
 
		if QFile.exists(filename):
			fh = QFile(filename)
 
		if not fh.open(QFile.ReadOnly):
			QtGui.qApp.quit()
 
		data = fh.readAll()
		codec = QTextCodec.codecForUtfText(data)
		unistr = codec.toUnicode(data)
 
		tmp = ('Notepad: %s' % filename)
		self.setWindowTitle(tmp)
 
		self.textEdit.setText(unistr)


	def warningDialog(self, message, message_extend):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText(message)
		#msg.setInformativeText()
		msg.setWindowTitle("Error dialog")
		msg.setDetailedText("The details are as follows:\n\n"+ message_extend)
		msg.exec()


		'''
		OTHER WAY (if you want to make a choice)
		buttonReply = QMessageBox.critical(self, "Error dialog", message_extend, QMessageBox.Ok, QMessageBox.Ok)
		if buttonReply == QMessageBox.Yes:
			print('Yes clicked.')
		else:
			print('No clicked.')'''

	def newFile(self):
		print("New file")

	def checkValue(self, linedit):
		try:
			_val = linedit.text()
			if _val != '':
				_val = int(_val)
				if _val < 0 or _val > 7:
					self.warningDialog("Buttons out of range!", "This board has only 8 pin (0-7), please enter a valid value")
		
		except ValueError:
			self.warningDialog("You entered a non-numeric value", "Please enter a valid number (0-7)")

	def ledButtonClicked(self):
		print("Leds click")
		self.checkValue(self.textbox_leds)	

	def buzzerButtonClicked(self):
		print("Buzzer click")

	def lightSensorButtonClicked(self):
		print("Light sensor click")
		self.checkValue(self.textbox_lightSensor)

	def potentiometerButtonClicked(self):
		print("Potentiometer click")

	def keysButtonClicked(self):
		print("Keys click")

	def motorsButtonClicked(self):
		print("Motors click")

	def irSensorsButtonClicked(self):
		print("IR sensors click")

	def ultrasoundButtonClicked(self):
		print("ultrasound click")
		self.checkValue(self.textbox_ultrasound)
