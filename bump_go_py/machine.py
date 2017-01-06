from state import *

class Machine:

	def __init__(self, n):

		self.states = []
		self.transitions = []
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
		t = self.states[orig].addTransition(self.t_cont, end, name)
		self.t_cont += 1
		if not t in self.transitions:
			self.transitions.append(t)


	def getStates(self):
		return self.states

	def setStateActive(self, n_state, flag):
		self.states[n_state].setActive(flag)

	def setTransitionActive(self, n_transition, flag):
		self.transitions[n_transition].setActive(flag)
		for i in self.transitions:
				print (i.isActive())

	def setStateName(self, n_state, name):
		self.states[n_state].setName(name)

	def getState(self, n_state):
		return self.states[n_state]

	def getTransition(self, id):
		return self.transitions[id]

	def getTransitions(self):
		return self.transitions
