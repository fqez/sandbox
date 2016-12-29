class Transition:

	def __init__(self, init, end, name):
		self.init = init
		self.end = end
		self.name = name
		self.highlight = False

	def setName(self, name):
		self.name = name

	def setTransitionHighlight(self):
		self.highlight = not self.highlight

	def getInit(self):
		return self.init

	def getEnd(self):
		return self.end
