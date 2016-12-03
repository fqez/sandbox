
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time

class Fader ():

	def configFade(self, target, start, end, fade):

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
		self.aIn = self.a
		self.aOut = self.a

	def fadeOut(self):
		
		self.aOut.setDirection(QAbstractAnimation.Forward)
		self.aOut.start(QPropertyAnimation.DeleteWhenStopped)

	def fadeIn(self):
			
		self.aIn.setDirection(QAbstractAnimation.Backward)
		self.aIn.start(QPropertyAnimation.DeleteWhenStopped)
