#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.text = self.__class__.__name__ + " " + hex(id(self))
        self.setWindowTitle(self.text)
        self.resize(300,200)
        self.show()

    def paintEvent(self, event):
        p = QtGui.QPainter()
        p.begin(self)
        p.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)
        p.save()
        p.rotate(10)
        p.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)
        p.restore()
        p.drawText(event.rect(), QtCore.Qt.AlignBottom, self.text)
        p.end()

def main():
    app = QtGui.QApplication(sys.argv)
    win1 = Window()
    win2 = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
