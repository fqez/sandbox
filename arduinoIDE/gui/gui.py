
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gui.widgets.widget_right import *
from gui.widgets.widget_leftUp import WidgetControl
from gui.widgets.widget_leftDown import WidgetMotor
from gui.widgets.miniwidgets import *

from examples import Examples


import os

class MainWindow(QMainWindow):

	updateGUI=pyqtSignal()
	changeWidget = pyqtSignal(int)

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.setWindowTitle("Arduino Robot")
		self.setMinimumSize(1000,700)
		self.setMaximumSize(1000,700)
		self.selectedBoard = -1	#-1:no selection; 0: top; 1: bottom

		self.changeWidget.connect(self.switchWidget)
		self.examples = Examples()

		self.initUI()


	def initUI(self):  

		self.setStyleSheet(self.readStyleSheet("style.stylesheet"))
		self.initMenuBar()
		buzzer = BuzzerWidget(self)
		buzzer.show()

		'''main layout'''
		self.horizontalLayoutWidget = QWidget(self)
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.mainLayout = QHBoxLayout(self.horizontalLayoutWidget)
		self.mainLayout.setObjectName("mainLayout")

		'''Empty left Widget'''
		self.emptyWidget = QWidget()
		self.emptyLayout = QVBoxLayout()
		self.emptyLayout.setObjectName("emptyLayout")
		self.selectBoardLabel = QLabel("Select a board!")
		self.selectBoardLabel.setObjectName("SelectBoardLabel")
		self.emptyLayout.addWidget(self.selectBoardLabel)


		self.emptyWidget.setLayout(self.emptyLayout)

		'''Left and right widgets'''
		self.leftWidgetUp = WidgetControl(self)
		self.leftWidgetDown = WidgetMotor(self)
		self.rightWidget = RightWidget(self)
		self.rightWidgetUp = RightWidgetUp(self)
		self.rightWidgetDown = RightWidgetDown(self)
		#self.leftWidgetUp.setMaximumWidth(300)

		self.mainLayout.addWidget(self.emptyWidget)
		self.mainLayout.addWidget(self.leftWidgetUp)
		self.mainLayout.addWidget(self.leftWidgetDown)
		self.mainLayout.addWidget(self.rightWidget)
		self.mainLayout.addWidget(self.rightWidgetUp)
		self.mainLayout.addWidget(self.rightWidgetDown)

		self.leftWidgetUp.setVisible(False)
		self.leftWidgetDown.setVisible(False)
		self.rightWidgetUp.setVisible(False)
		self.rightWidgetDown.setVisible(False)
		self.rightWidget.setVisible(True)

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

		# LED examples
		l = self.examples.getExample('led')
		for e in l:
			action = QAction(e,self)
			action.setData(e)
			sub_sub_leds.addAction(action)
		# Buzzer examples
		l = self.examples.getExample('buz')
		for e in l:
			action = QAction(e,self)
			action.setData(e)
			sub_sub_buzzer.addAction(action)
		# Light sensor examples
		l = self.examples.getExample('light')
		for e in l:
			action = QAction(e,self)
			action.setData(e)
			sub_sub_light.addAction(action)
		# Potentiometer examples
		l = self.examples.getExample('pot')
		for e in l:
			action = QAction(e,self)
			action.setData(e)
			sub_sub_potentiometer.addAction(action)
		# LCD examples
		l = self.examples.getExample('lcd')
		for e in l:
			action = QAction(e,self)
			action.setData(e)
			sub_sub_lcd.addAction(action)
		# Keys examples
		l = self.examples.getExample('keys')
		for e in l:
			action = QAction(e,self)
			action.setData(e)
			sub_sub_keys.addAction(action)



		# Behaviour examples
		l = self.examples.getExample('behaviour')
		for e in l:
			action = QAction(e,self)
			action.setData(e)
			sub_behaviour.addAction(action)



		'''Adding signals, each example is differente by its name, passed in action.setData'''
		# Arduino Control examples
		sub_sub_leds.triggered.connect(self.loadExample)
		sub_sub_buzzer.triggered.connect(self.loadExample)
		sub_sub_light.triggered.connect(self.loadExample)
		sub_sub_potentiometer.triggered.connect(self.loadExample)
		sub_sub_lcd.triggered.connect(self.loadExample)
		sub_sub_keys.triggered.connect(self.loadExample)

		# Arduino Motors examples

		# Behaviour examples
		sub_behaviour.triggered.connect(self.loadExample)






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

		
	def switchWidget(self, n):
		'''
			n = -1 switch left and right widget to empty
			n = 0 switch left widget to arduino control
			n = 1 switch left widget to arduino motor

			n = 2 switch right widget for arduino control
			n = 3 switch right widget for arduino motor
		'''
		if n == 0:
			self.leftWidgetUp.setVisible(True)
			self.leftWidgetDown.setVisible(False)
			self.emptyWidget.setVisible(False)
		elif n == 1:
			self.leftWidgetUp.setVisible(False)
			self.leftWidgetDown.setVisible(True)
			self.emptyWidget.setVisible(False)
		elif n == 2:
			self.rightWidgetUp.setVisible(True)
			self.rightWidgetDown.setVisible(False)
			self.rightWidget.setVisible(False)
			self.emptyWidget.setVisible(False)
			f = FadeIn(self.rightWidgetUp,1,0,500)
			f.fade()
		elif n == 3:
			self.rightWidgetUp.setVisible(False)
			self.rightWidgetDown.setVisible(True)
			self.rightWidget.setVisible(False)
			self.emptyWidget.setVisible(False)
			f = FadeIn(self.rightWidgetDown,1,0,500)
			f.fade()
		else:
			print("EMitido -1")
			self.leftWidgetUp.setVisible(False)
			self.leftWidgetDown.setVisible(False)
			self.rightWidgetUp.setVisible(False)
			self.rightWidgetDown.setVisible(False)
			self.emptyWidget.setVisible(True)
			self.rightWidget.setVisible(True)
			f = FadeIn(self.rightWidget,1,0,500)
			f.fade()


	'''LoadExamples'''
	def loadExample(self, action):	
		print (action.data())

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

	

	
