
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):

	updateGUI=pyqtSignal()
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.setWindowTitle("Arduino Robot")
		self.initUI()


	def initUI(self):  
		qApp.setStyleSheet("QGroupBox {border: 1px solid gray;border-color:blue;border-radius: 5px;margin-top: 0.5em;} QGroupBox::title {subcontrol-origin: margin;left: 10px;padding: 0 3px 0 3px;}");

		self.initMenuBar()

		self.hSpacer = QSpacerItem(30, 30, QSizePolicy.Ignored, QSizePolicy.Ignored);

		'''main layout'''
		self.horizontalLayoutWidget = QWidget(self)
		self.horizontalLayoutWidget.setGeometry(QRect(20, 30, 800, 600))
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.mainLayout = QHBoxLayout(self.horizontalLayoutWidget)
		self.mainLayout.setObjectName("mainLayout")

		'''right and left layouts main window'''
		self.rightLayout = QVBoxLayout()
		self.rightLayout.setObjectName("rightLayout")
		self.leftLayout = QVBoxLayout()
		self.leftLayout.setObjectName("leftLayout")

		'''leds layout (left layout)'''
		self.ledGroupBox = QGroupBox()
		self.ledGroupBox.setTitle("LEDs")
		self.ledsLayout = QGridLayout()
		self.ledsLayout.setObjectName("ledsLayout")
		self.textbox_leds = QLineEdit()
		self.textbox_leds.setMaximumSize(50,40)
		self.button_leds = QPushButton("Light!")
		self.ledsLayout.addWidget(self.textbox_leds,0,0)
		self.ledsLayout.addWidget(self.button_leds,0,1)
		self.ledGroupBox.setLayout(self.ledsLayout) 

		'''buzzer layout (left layout)'''
		self.buzzerLayout = QGridLayout()
		self.buzzerLayout.setObjectName("buzzerLayout")
		self.label_buzzer = QLabel("Buzzer")
		self.button_buzzer = QPushButton("Play!")
		self.buzzerLayout.addWidget(self.label_buzzer,0,0)
		self.buzzerLayout.addWidget(self.button_buzzer,1,0)
		#self.ledsLayout.addItem(self.hSpacer,1,2)

		self.leftLayout.addWidget(self.ledGroupBox)
		self.leftLayout.addLayout(self.buzzerLayout)
		

		self.mainLayout.addLayout(self.leftLayout)
		self.mainLayout.addLayout(self.rightLayout)

		'''signals'''
		self.button_leds.clicked.connect(lambda:self.ledButtonClicked())

		self.setCentralWidget(self.horizontalLayoutWidget)
		self.show()
 

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

		'''Examples menu'''
		sub_control = QMenu('Arduino Control',self)
		sub_motor = QMenu('Arduino Motor',self)
		sub_behaviour = QMenu('Behaviours', self)	# comportamientos: sigue linea, sigue luz...

		sub_sub_leds = QMenu('LEDs', self)
		sub_sub_buzzer = QMenu('Buzzer', self)
		sub_sub_ultrasound = QMenu('Ultrasound', self)
		sub_sub_light = QMenu('Light sensors', self)
		sub_sub_ir = QMenu('IR sensors', self)
		sub_sub_motors = QMenu('Motors', self)
		sub_sub_potentiometer = QMenu('Potentiometer', self)
		sub_sub_lcd = QMenu('LCD', self)
		sub_sub_keys = QMenu('Keys', self)


		turn_on_led = QAction('Key Leds', self)
		turn_on_led.setStatusTip('Turn on a specific LED pushing a key')
		turn_on_led.triggered.connect(self.keys_led)

		exampleMenu = menubar.addMenu('&Examples')
		exampleMenu.addMenu(sub_control)
		exampleMenu.addMenu(sub_motor)
		exampleMenu.addMenu(sub_behaviour)

		sub_control.addAction(turn_on_led)
		#sub_motor.addAction(None)
		#sub_behaviour.addAction(None)



	def keys_led(self):
		print("Turn a led on")

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

	def ledButtonClicked(self):
		print("Leds click")