#!/usr/bin/python

import sys
from PyQt4 import QtGui

class Icon(QtGui.QWidget):
  def __init__(self,parent=None):
    QtGui.QWidget.__init__(self,parent)
    self.setGeometry(300,300,250,150)
    self.setWindowTitle("Icon")
    self.setWindowIcon(QtGui.QIcon("icons/web.png"))
    
if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  icon = Icon()
  icon.show()
  sys.exit(app.exec_())

