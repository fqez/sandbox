# General imports
import sys

# Practice imports
from gui.GUI import MainWindow
from gui.threadGUI import ThreadGUI
from PyQt5.QtWidgets import QApplication

# from mmg_nlp_base.preprocessor import TextProcessor

if __name__ == "__main__":

    app = QApplication(sys.argv)
    myGUI = MainWindow()
    myGUI.show()

    t2 = ThreadGUI(myGUI)
    t2.daemon=True
    t2.start()

    sys.exit(app.exec_())
