
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gui.widget_right import RightWidget
from gui.widget_leftUp import WidgetControl
from gui.widget_leftDown import WidgetMotor

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

		self.leftWidgetUp = WidgetControl(self)
		self.leftWidgetDown = WidgetMotor(self)
		self.rightWidget = RightWidget(self)

		self.mainLayout.addWidget(self.leftWidgetUp)
		self.mainLayout.addWidget(self.leftWidgetDown)
		self.mainLayout.addWidget(self.rightWidget)

		self.leftWidgetUp.setVisible(True)
		self.leftWidgetDown.setVisible(False)

		self.setCentralWidget(self.horizontalLayoutWidget)
		self.show()


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


	

	def newFile(self):
		print("New file")

	

	
