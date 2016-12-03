
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time

class Fader ():

	def __init__(self, target, start, end, fade):

		self.target = target
		self.op = QByteArray().append("opacity")
		self.eff = QGraphicsOpacityEffect(self.target)
		self.target.setGraphicsEffect(self.eff)
		self.eff.setOpacity(1)
		self.a = QPropertyAnimation(self.eff, self.op, self.target)
		self.a.setDuration(fade)
		self.a.setStartValue(start)
		self.a.setEndValue(end)
		self.a.setEasingCurve(QEasingCurve.Linear)

	def fade(self):
		self.a.setDirection(QAbstractAnimation.Backward)
		self.a.start(QPropertyAnimation.DeleteWhenStopped)

	def getAnimation(self):
		return self.a

class FadeOut(Fader):

	def __init__(self, target, start, end, fade):
		
		Fader.__init__(self, target, start, end, fade)

	def fade(self):
		self.a.setDirection(QAbstractAnimation.Forward)
		self.a.start(QPropertyAnimation.DeleteWhenStopped)

class FadeIn(Fader):
			
	def __init__(self, target, start, end, fade):
		
		Fader.__init__(self, target, start, end, fade)

	def fade(self):
		self.a.setDirection(QAbstractAnimation.Backward)
		self.a.start(QPropertyAnimation.DeleteWhenStopped)
