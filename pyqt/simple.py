#!/usr/bin/python3

import sys
from PyQt4 import QtGui # http://www.riverbankcomputing.com/static/Docs/PyQt4/html/qtgui.html

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  widget = QtGui.QWidget()
  widget.resize(250,150)
  widget.setWindowTitle("simple")
  widget.show()
  sys.exit(app.exec_())
  