class Transition:

	def __init__(self, id, init, end, name):
		self.id = id
		self.init = init
		self.end = end
		self.name = name
		self.highlight = False
		self.orig = [0,0]
		self.dest = [0,0]
		self.angle = 0

	def setName(self, name):
		self.name = name

	def setTransitionHighlight(self):
		self.highlight = not self.highlight

	def getStateInit(self):
		return self.init

	def getStateEnd(self):
		return self.end

	def setOrig(self, x, y):
		self.orig[0] = x
		self.orig[1] = y

	def setDest(self, x, y):
		self.dest[0] = x
		self.dest[1] = y

	def setAngle(self, angle):
		self.angle = angle

	def getOrig(self):
		return self.orig

	def getDest(self):
		return self.dest

	def getAngle(self):
		return self.angle
