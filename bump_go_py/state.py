from transition import *

class State:

	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.transitions = []
		self.highlight = False


	def addTransition(self, id, end, name):
		t = Transition(id, self.id, end, name)
		self.transitions.append(t)

	def getTransitions(self):
		return self.transitions

	def getTransition(self, n):
		return self.transitions[n]

	def setName(self, name):
		self.name = name

	def getName(self):
		return self.name

	def getId(self):
		return self.id	

	def setHighlight(self, flag):
		self.highlight = flag

	def setPos(self, x, y):
		self.x = x
		self.y = y

	def getPos(self):
		return [self.x, self.y]
