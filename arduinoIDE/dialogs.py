
from PyQt5.QtWidgets import QMessageBox


class Dialog():

	def warningDialog(self, message, message_extend):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText(message)
		#msg.setInformativeText()
		msg.setWindowTitle("Error dialog")
		msg.setDetailedText("The details are as follows:\n\n"+ message_extend)
		msg.exec()


		'''
		OTHER WAY (if you want to make a choice)
		buttonReply = QMessageBox.critical(self, "Error dialog", message_extend, QMessageBox.Ok, QMessageBox.Ok)
		if buttonReply == QMessageBox.Yes:
			print('Yes clicked.')
		else:
			print('No clicked.')'''