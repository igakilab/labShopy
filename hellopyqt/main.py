from PyQt4 import QtGui
import sys
import mainWindow
import test1
import test2

class mainWindow(QtGui.QMainWindow, mainWindow.Ui_MainWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		
class test1Widget(QtGui.QMainWindow, test1.Ui_Form):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		
class test2Widget(QtGui.QMainWindow, test2.Ui_Form):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)

def change(window):
	window.setCentralWidget(test2Widget())
  
def main():
	app = QtGui.QApplication(sys.argv)
	window = mainWindow()
	test1 = test1Widget()
	window.setCentralWidget(test1)
	test1.pushButton.clicked.connect(lambda: change(window))
	window.show()

	app.exec_()

if __name__ == "__main__":
	main()
