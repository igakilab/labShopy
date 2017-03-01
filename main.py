from PyQt4 import QtGui
import sys
import input

class Example(QtGui.QMainWindow, input.Ui_MainWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		#self.textEdit.setText("test textEdit")

	#def clicked(self):
	#	self.textEdit.append("clicked")


def main():
	app = QtGui.QApplication(sys.argv)
	form = Example()
	form.show()

	#form.btn1.clicked.connect(lambda: form.clicked())
	#form.btn2.clicked.connect(app.quit)

	app.exec_()

if __name__ == "__main__":
	main()
