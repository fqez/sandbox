#!/usr/bin/python3

import sys

from gui.gui import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":

	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	
	sys.exit(app.exec_())