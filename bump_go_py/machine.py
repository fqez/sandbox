from state import *

class Machine:

	def __init__(self, n):

		self.states = []
		self.cont = 0
		self.t_cont = 0
		
		for i in range (n):
			state = State(self.cont, '')
			self.states.append(state)
			self.cont += 1

	def addState(self, name):
		state = State(cont, name)
		self.states.append(state)
		self.cont += 1

	def addTransition(self, orig, end, name):
		self.states[orig].addTransition(self.t_cont, end, name)
		self.t_cont += 1

	def getStates(self):
		return self.states

	def setStateHighligt(self, n_state, flag):
		self.states[n_state].setHighlight(flag)

	def setStateName(self, n_state, name):
		self.states[n_state].setName(name)

	def getState(self, n_state):
		return self.states[n_state]

	def getTransition(self, orig, id):
		return self.states[orig].getTransition(id)
