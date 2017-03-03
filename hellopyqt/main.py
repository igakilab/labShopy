from PyQt4 import QtGui
import sys
import mainWindow
import test1
import test2

class mainWindow(QtGui.QMainWindow, mainWindow.Ui_MainWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		
class test1Widget(QtGui.QWidget, test1.Ui_Form):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.setupUi(self)
    self.pushButton.clicked.connect(lambda: change(self, test2Widget))
		
class test2Widget(QtGui.QWidget, test2.Ui_Form):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.setupUi(self)
    self.pushButton.clicked.connect(lambda: change(self, test1Widget))

def change(widget, next):
	widget.parentWidget().setCentralWidget(next())
  
def main():
	app = QtGui.QApplication(sys.argv)
	window = mainWindow()
	window.setCentralWidget(test1Widget())
	window.show()

	app.exec_()

if __name__ == "__main__":
	main()
