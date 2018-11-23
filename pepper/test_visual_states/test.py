#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, threading, time, rospy
from geometry_msgs.msg import Twist
from visualstates.codegen.python.state import State
from visualstates.codegen.python.temporaltransition import TemporalTransition
from visualstates.codegen.python.conditionaltransition import ConditionalTransition
from visualstates.codegen.python.runtimegui import RunTimeGui
from PyQt5.QtWidgets import QApplication


class GlobalNamespace():
	def __init__(self):
		rospy.init_node("test", anonymous=True)

		self.cmd_velPub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
		time.sleep(1) # wait for initialization of the node, subscriber, and publisher

	def stop(self):
		rospy.signal_shutdown("exit ROS node")

	def publishcmd_vel(self, cmd_vel):
		self.cmd_velPub.publish(cmd_vel)



class State0(State):
	def __init__(self, id, initial, globalNamespace, namespace, cycleDuration, parent=None, gui=None):
		State.__init__(self, id, initial, cycleDuration, parent, gui)
		self.globalNamespace = globalNamespace
		self.namespace = namespace

	def runCode(self):
		pass


class Namespace0():
	def __init__(self, globalNamespace):
		self.globalNamespace = globalNamespace


class State1(State):
	def __init__(self, id, initial, globalNamespace, namespace, cycleDuration, parent=None, gui=None):
		State.__init__(self, id, initial, cycleDuration, parent, gui)
		self.globalNamespace = globalNamespace
		self.namespace = namespace

	def runCode(self):
		velCommand = Twist()
		velCommand.linear.x = 0.3
		velCommand.angular.z = 0.0
		self.globalNamespace.publishcmd_vel(velCommand)


class Namespace1():
	def __init__(self, globalNamespace):
		self.globalNamespace = globalNamespace


class State3(State):
	def __init__(self, id, initial, globalNamespace, namespace, cycleDuration, parent=None, gui=None):
		State.__init__(self, id, initial, cycleDuration, parent, gui)
		self.globalNamespace = globalNamespace
		self.namespace = namespace

	def runCode(self):
		velCommand = Twist()
		velCommand.linear.x = 0.0
		velCommand.angular.z = 0.0
		self.globalNamespace.publishcmd_vel(velCommand)


class Namespace3():
	def __init__(self, globalNamespace):
		self.globalNamespace = globalNamespace


class State4(State):
	def __init__(self, id, initial, globalNamespace, namespace, cycleDuration, parent=None, gui=None):
		State.__init__(self, id, initial, cycleDuration, parent, gui)
		self.globalNamespace = globalNamespace
		self.namespace = namespace

	def runCode(self):
		velCommand = Twist()
		velCommand.linear.x = 0.0
		velCommand.angular.z = 0.2
		self.globalNamespace.publishcmd_vel(velCommand)


class Namespace4():
	def __init__(self, globalNamespace):
		self.globalNamespace = globalNamespace


class State5(State):
	def __init__(self, id, initial, globalNamespace, namespace, cycleDuration, parent=None, gui=None):
		State.__init__(self, id, initial, cycleDuration, parent, gui)
		self.globalNamespace = globalNamespace
		self.namespace = namespace

	def runCode(self):
		velCommand = Twist()
		velCommand.linear.x = 0.0
		velCommand.angular.z = 0.0
		self.globalNamespace.publishcmd_vel(velCommand)


class Namespace5():
	def __init__(self, globalNamespace):
		self.globalNamespace = globalNamespace


class Tran3(TemporalTransition):

	def runCode(self):
		pass

class Tran4(TemporalTransition):

	def runCode(self):
		pass

class Tran6(TemporalTransition):

	def runCode(self):
		pass

displayGui = False
guiThread = None
gui = None

def readArgs():
	global displayGui
	for arg in sys.argv:
		splitedArg = arg.split('=')
		if splitedArg[0] == '--displaygui':
			if splitedArg[1] == 'True' or splitedArg[1] == 'true':
				displayGui = True
				print('runtime gui enabled')
			else:
				displayGui = False
				print('runtime gui disabled')

def runGui():
	global gui
	app = QApplication(sys.argv)
	gui = RunTimeGui()
	gui.show()
	app.exec_()

if __name__ == "__main__":

	globalNamespace = GlobalNamespace()


	readArgs()
	if displayGui:
		guiThread = threading.Thread(target=runGui)
		guiThread.start()


	if displayGui:
		while(gui is None):
			time.sleep(0.1)

		gui.addState(0, "root", True, 0.0, 0.0, None)
		gui.addState(1, "go_forward", True, 946.0, 854.0, 0)
		gui.addState(3, "stop", False, 1067.0, 974.0, 0)
		gui.addState(4, "turn", False, 923.0, 1079.0, 0)
		gui.addState(5, "final", False, 843.0, 955.0, 0)

		gui.addTransition(3, "transition 3", 1, 3, 1070.5, 854.5)
		gui.addTransition(4, "transition 4", 3, 4, 1069.5, 1075.0)
		gui.addTransition(6, "transition 6", 4, 5, 840.5, 1080.0)

	if displayGui:
		gui.emitLoadFromRoot()
		gui.emitActiveStateById(0)

	namespace0 = Namespace0(globalNamespace)
	state0 = State0(0, True, globalNamespace, None, 100, None, gui)
	namespace1 = Namespace1(globalNamespace)
	state1 = State1(1, True, globalNamespace, namespace0, 100, state0, gui)
	namespace3 = Namespace3(globalNamespace)
	state3 = State3(3, False, globalNamespace, namespace0, 100, state0, gui)
	namespace4 = Namespace4(globalNamespace)
	state4 = State4(4, False, globalNamespace, namespace0, 100, state0, gui)
	namespace5 = Namespace5(globalNamespace)
	state5 = State5(5, False, globalNamespace, namespace0, 100, state0, gui)

	tran3 = Tran3(3, 3, 3000)
	state1.addTransition(tran3)

	tran4 = Tran4(4, 4, 1000)
	state3.addTransition(tran4)

	tran6 = Tran6(6, 5, 3000)
	state4.addTransition(tran6)

	try:
		state0.startThread()
		state0.join()
		globalNamespace.stop()
		sys.exit(0)
	except:
		state0.stop()
		if displayGui:
			gui.close()
			guiThread.join()

		state0.join()
		globalNamespace.stop()
		sys.exit(1)
