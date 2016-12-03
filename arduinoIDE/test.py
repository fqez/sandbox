#!/usr/bin/python3
from gui.testWidget import MyWidget1
from PyQt5.QtWidgets import QApplication

import sys

if __name__ == "__main__":

	app = QApplication(sys.argv)
	print("Hello")
	myw = MyWidget1()
	myw.show()
	print("Bye")

	app.exec()
