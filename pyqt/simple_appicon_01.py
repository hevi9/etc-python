#!/usr/bin/python

import sys
from PyQt4 import QtGui

import logging
log = logging.getLogger(__name__)



def run():
  app = QtGui.QApplication(sys.argv)
  widget = QtGui.QWidget()
  widget.resize(250,150)
  widget.setWindowTitle("Simple with Icon")
  ##
  widget.show()
  sys.exit(app.exec_())

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  run()
