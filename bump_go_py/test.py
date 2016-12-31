#!/usr/bin/env python3
  
  
#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################
  
  
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QPointF, QRectF
from PyQt5.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
		QPainterPath, QPalette, QPen, QPixmap, QPolygon, QRadialGradient, QColor, 
		QTransform, QPolygonF)
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
		QLabel, QSpinBox, QWidget, QPushButton )
  
import basicdrawing_rc

from machine import *
from state import *
from transition import *
import math, time
  
  
class RenderArea(QWidget):
	points = QPolygon([
		QPoint(10, 80),
		QPoint(20, 10),
		QPoint(80, 30),
		QPoint(90, 70)
	])
  
	Line, Points, Polyline, Polygon, Rect, RoundedRect, Ellipse, Arc, Chord, \
			Pie, Path, Text, Pixmap = range(13)
  
	def __init__(self, machine, parent=None):
		super(RenderArea, self).__init__(parent)
  
		self.pen = QPen()
		self.brush = QBrush()
		self.pixmap = QPixmap()
  
		self.shape = RenderArea.Polygon
		self.antialiased = True
		self.transformed = False
		self.pixmap.load(':/images/qt-logo.png')
  
		self.setBackgroundRole(QPalette.Base)
		self.setAutoFillBackground(True)
		
		self.machine = machine

		self.dist_radius = min(self.width() / 4, self.height() / 4) * 1.5
		self.dist_center = QPoint(self.width() / 2.0, self.height() / 2.0)
		self.n_states = len(self.machine.getStates())

		self.state_radius = self.funcc(self.dist_radius, self.n_states)
		self.active = -1
		self.t_active = -1

		self.pts = []


		#Brushes
		linearGradient = QLinearGradient(-self.state_radius, -self.state_radius, self.state_radius, self.state_radius)
		linearGradient.setColorAt(0.0, Qt.darkGreen)
		linearGradient.setColorAt(0.7, Qt.green)
		linearGradient.setColorAt(0.3, Qt.green)
		linearGradient.setColorAt(1.0, Qt.white)
		self.greenGradientBrush = QBrush(linearGradient)

		linearGradient = QLinearGradient(-self.state_radius, -self.state_radius, self.state_radius, self.state_radius)
		linearGradient.setColorAt(0.0, Qt.darkGray)
		linearGradient.setColorAt(0.7, Qt.lightGray)
		linearGradient.setColorAt(0.3, Qt.gray)
		linearGradient.setColorAt(1.0, Qt.white)
		self.grayGradientBrush = QBrush(linearGradient)
		self.setBrush(self.grayGradientBrush)
		#end brushes

	def funcc(self, r, n):
		return int((r*0.05) / (n*0.04))

	def minimumSizeHint(self):
		return QSize(100, 100)
  
	def sizeHint(self):
		return QSize(400, 200)
  
	def setShape(self, shape):
		self.shape = shape
		self.update()
  
	def setPen(self, pen):
		self.pen = pen
		self.update()
  
	def setBrush(self, brush):
		self.brush = brush
		self.update()
  
	def setAntialiased(self, antialiased):
		self.antialiased = antialiased
		self.update()
  
	def setTransformed(self, transformed):
		self.transformed = transformed
		self.update()

	def resizeEvent(self, event):
		self.dist_center = QPoint(self.width() / 2.0, self.height() / 2.0)
		self.dist_radius = min(self.width() / 4, self.height() / 4) * 1.5
		self.state_radius = self.funcc(self.dist_radius, self.n_states)

		self.update()

	def poly(self, pts):
		return QPolygonF(map(lambda p: QPointF(*p), pts))

	def wave(self):
			   
#		print(points[0][0] ,'<', points[1][0], 'and', points[0][1], '>', points[1][1])


		for i in self.machine.getStates():
			for j in i.getTransitions():
				print(j.id, j.orig, j.dest)
		t = self.machine.getTransition(self.active, self.t_active)
		init = QPoint(t.getOrig()[0], t.getOrig()[1])
		end = QPoint(t.getDest()[0], t.getDest()[1])
		angle = t.getAngle()
		for i in range(3):
			self.pts = [[init.x(), init.y()], [end.x(), end.y()]]
			while self.pts[0][0] < self.pts[1][0] and self.pts[0][1] > self.pts[1][1]:
				print(self.pts)
				self.pts[0][0] += (self.state_radius * math.cos(angle) * 0.1)
				self.pts[0][1] -= (self.state_radius * math.sin(angle) * 0.1)
				self.update()
				QApplication.processEvents()
				#time.sleep(0.025)
				time.sleep(1)

	def paintEvent(self, event):
		rect = QRect(10, 20, 80, 60)
  
		path = QPainterPath()
		path.moveTo(20, 80)
		path.lineTo(20, 30)
		path.cubicTo(80, 0, 50, 50, 80, 80)
  
		startAngle = 30 * 16
		arcLength = 120 * 16
  
		painter = QPainter(self)
		painter.setPen(self.pen)
		painter.setBrush(self.brush)
		if self.antialiased:
			painter.setRenderHint(QPainter.Antialiasing)

		angle_step = 360 / self.n_states

		painter.save()
		painter.translate(self.dist_center.x(), self.dist_center.y())

		#painter.drawRect(- self.dist_radius, - self.dist_radius, self.dist_radius *2,self.dist_radius*2)
		#painter.drawEllipse(QPoint(0, 0), self.dist_radius , self.dist_radius)
		painter.rotate(-180)	#to start painting from the left side of the circle
		x = self.dist_radius * math.cos(0)
		y = self.dist_radius * math.sin(0)

		for h in range(self.n_states):

			rot = angle_step * h

			painter.save()
			painter.rotate(rot)
			painter.translate(x,y)

			if self.machine.getState(h).highlight:
				painter.setBrush(self.greenGradientBrush)			
			painter.drawEllipse(QPoint(0,0), self.state_radius, self.state_radius)
			#global position of transformed coordinates
			gx = painter.worldTransform().map(QPoint(0,0)).x()
			gy = painter.worldTransform().map(QPoint(0,0)).y()
			self.machine.getState(h).setPos(gx, gy)

			# text transformation
			painter.save()
			painter.rotate(180)
			painter.rotate(-rot)
			font = painter.font();
			font.setPixelSize(self.state_radius*.4);
			painter.setFont(font);
			rect = QRect(-self.state_radius, -self.state_radius, self.state_radius*2, self.state_radius*2)
			painter.drawText(rect, Qt.AlignCenter, self.machine.getState(h).getName());
			painter.restore()
			#end text transformation


			painter.restore()			
			
		painter.restore()

		
		#drawing transitions.
		painter.save()
		pptv = QTransform()
		pptv.translate(0, self.height())
		pptv.rotate(-180, Qt.XAxis)
		painter.setTransform(pptv)
		s = self.machine.getStates()
		for j in s:
			t = j.getTransitions()
			for i in t:
				#get the points in the canvas
				init = QPoint(j.getPos()[0], j.getPos()[1])
				end = QPoint(self.machine.getState(i.getStateEnd()).getPos()[0], self.machine.getState(i.getStateEnd()).getPos()[1])
				# get the transformed ponts
				init2 = QPoint(painter.worldTransform().map(init))
				end2 = QPoint(painter.worldTransform().map(end))

				#get the angle between states centers
				angle = math.atan2(end2.y() - init2.y(), end2.x() - init2.x())

				#get the coordinates of the starting point of the transition (it starts in the bound, not in the center)
				newX = self.state_radius * math.cos(angle) + init2.x()
				newY = self.state_radius * math.sin(angle) + init2.y()
				init2.setX(newX)
				init2.setY(newY)

				#same for the end of the transition
				angle2 = math.atan2(init2.y() - end2.y(), init2.x() - end2.x())
				newX2 = self.state_radius * math.cos(angle2) + end2.x()
				newY2 = self.state_radius * math.sin(angle2) + end2.y()
				end2.setX(newX2)
				end2.setY(newY2)

				#painter.drawLine(init, end)
				painter.drawLine(init2, end2)
				init = QPoint(painter.worldTransform().map(init2))
				end = QPoint(painter.worldTransform().map(end2))
				i.setOrig(init.x(), init.y())
				i.setDest(end.x(), end.y())	
				i.setAngle(angle)
				#painter.draw
		painter.restore()


		painter.setPen(QPen(QColor(Qt.gray), 3))
		for i in machine.getStates():
			for j in i.getTransitions():
				i = QPoint(j.getOrig()[0], j.getOrig()[1])
				o = QPoint(j.getDest()[0], j.getDest()[1])			
				painter.drawPolyline(init, end)


		if self.t_active != -1:
			t = self.machine.getTransition(self.active, self.t_active)
			init = QPoint(t.getOrig()[0], t.getOrig()[1])
			end = QPoint(t.getDest()[0], t.getDest()[1])
			painter.setPen(QPen(QColor(Qt.darkGreen), 3))
			painter.drawPolyline(init, end)
			
			painter.setPen(QPen(QColor(Qt.gray), 3))
			painter.drawPolyline(self.poly(self.pts))


			painter.setBrush(QBrush(QColor(255, 0, 0)))
			painter.setPen(QPen(QColor(Qt.black), 1))

			
			for x, y in self.pts:
				painter.drawEllipse(QRectF(x - 4, y - 4, 8, 8))

		states = machine.getStates()
		for i in states:
			self.machine.setStateHighligt(i.getId(), False)
		self.machine.setStateHighligt(self.active, True)

		'''for x in range(0, self.width(), 100):
			for y in range(0, self.height(), 100):
				painter.save()
				painter.translate(x, y)
				  
				if self.shape == RenderArea.Line:
					painter.drawLine(rect.bottomLeft(), rect.topRight())
				elif self.shape == RenderArea.Points:
					painter.drawPoints(RenderArea.points)
				elif self.shape == RenderArea.Polyline:
					painter.drawPolyline(RenderArea.points)
				elif self.shape == RenderArea.Polygon:
					painter.drawPolygon(RenderArea.points)
				elif self.shape == RenderArea.Rect:
					painter.drawRect(rect)
				elif self.shape == RenderArea.RoundedRect:
					painter.drawRoundedRect(rect, 25, 25, Qt.RelativeSize)
				elif self.shape == RenderArea.Ellipse:
					painter.drawEllipse(rect)
				elif self.shape == RenderArea.Arc:
					painter.drawArc(rect, startAngle, arcLength)
				elif self.shape == RenderArea.Chord:
					painter.drawChord(rect, startAngle, arcLength)
				elif self.shape == RenderArea.Pie:
					painter.drawPie(rect, startAngle, arcLength)
				elif self.shape == RenderArea.Path:
					painter.drawPath(path)
				elif self.shape == RenderArea.Text:
					painter.drawText(rect, Qt.AlignCenter,
							"PyQt by\nRiverbank Computing")
				elif self.shape == RenderArea.Pixmap:
					painter.drawPixmap(10, 10, self.pixmap)
  
				painter.restore()
				'''
  
		painter.setPen(self.palette().dark().color())
		painter.setBrush(Qt.NoBrush)
		painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))


	def change(self,n):
		print('active', n)
		self.active = n
		#time.sleep(5)
		self.t_active = n
		print(self.active, self.t_active)
		self.wave()

IdRole = Qt.UserRole
  
class Window(QWidget):
	def __init__(self, machine):
		super(Window, self).__init__()
  
		self.renderArea = RenderArea(machine)
  
		mainLayout = QGridLayout()
		mainLayout.setColumnStretch(0, 1)
		mainLayout.setColumnStretch(3, 1)
		mainLayout.addWidget(self.renderArea, 0, 0, 1, 4)
		mainLayout.setRowMinimumHeight(1, 6)

		self.button = QPushButton()
		self.button.setText('Push')

		mainLayout.addWidget(self.button, 1, 2)

		self.button.pressed.connect(self.pressed)

		self.setMinimumSize(QSize(640,480))
				
		self.setLayout(mainLayout)

		self.setWindowTitle("Basic Drawing")
		self.cont = 0

	def pressed(self):
		self.renderArea.change(self.cont)
		self.cont += 1
		print('pressed')
		  
	def shapeChanged(self):
		shape = self.shapeComboBox.itemData(self.shapeComboBox.currentIndex(),
				IdRole)
		self.renderArea.setShape(shape)
  
	def penChanged(self):
		width = self.penWidthSpinBox.value()
		style = Qt.PenStyle(self.penStyleComboBox.itemData(
				self.penStyleComboBox.currentIndex(), IdRole))
		cap = Qt.PenCapStyle(self.penCapComboBox.itemData(
				self.penCapComboBox.currentIndex(), IdRole))
		join = Qt.PenJoinStyle(self.penJoinComboBox.itemData(
				self.penJoinComboBox.currentIndex(), IdRole))
  
		self.renderArea.setPen(QPen(Qt.blue, width, style, cap, join))
  
	def brushChanged(self):
		style = Qt.BrushStyle(self.brushStyleComboBox.itemData(
				self.brushStyleComboBox.currentIndex(), IdRole))
  
		if style == Qt.LinearGradientPattern:
			linearGradient = QLinearGradient(0, 0, 100, 100)
			linearGradient.setColorAt(0.0, Qt.white)
			linearGradient.setColorAt(0.2, Qt.green)
			linearGradient.setColorAt(1.0, Qt.black)
			self.renderArea.setBrush(QBrush(linearGradient))
		elif style == Qt.RadialGradientPattern:
			radialGradient = QRadialGradient(50, 50, 50, 70, 70)
			radialGradient.setColorAt(0.0, Qt.white)
			radialGradient.setColorAt(0.2, Qt.green)
			radialGradient.setColorAt(1.0, Qt.black)
			self.renderArea.setBrush(QBrush(radialGradient))
		elif style == Qt.ConicalGradientPattern:
			conicalGradient = QConicalGradient(50, 50, 150)
			conicalGradient.setColorAt(0.0, Qt.white)
			conicalGradient.setColorAt(0.2, Qt.green)
			conicalGradient.setColorAt(1.0, Qt.black)
			self.renderArea.setBrush(QBrush(conicalGradient))
		elif style == Qt.TexturePattern:
			self.renderArea.setBrush(QBrush(QPixmap(':/images/brick.png')))
		else:
			self.renderArea.setBrush(QBrush(Qt.green, style))
  
  
if __name__ == '__main__':
  
	import sys
  
	machine = Machine(3)
	machine.setStateName(0, 'Forward') 
	machine.setStateName(1, 'Backward')
	machine.setStateName(2, 'Turn')
	machine.setStateHighligt(0, True)
	machine.addTransition(0, 1,'close')
	machine.addTransition(1, 2,'time')
	#machine.addTransition(2, 0,'time2')

	for i in machine.getStates():
		for j in i.getTransitions():
			print(j.id, j.orig, j.dest)
	
	app = QApplication(sys.argv)
	window = Window(machine)
	window.show()
	sys.exit(app.exec_())
  