#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore # http://www.riverbankcomputing.com/static/Docs/PyQt4/html/qtgui.html
# http://zetcode.com/tutorials/pyqt4/
import logging
log = logging.getLogger(__name__)

class Board(QtGui.QWidget):
  
  def __init__(self):
    super().__init__()
    self.setMinimumSize(200, 200)
    self.rows = 10
    self.cols = 10
    ## init Map
    self.map = list() # rows
    for r in range(0,self.rows):
      self.map.append(list())
      for c in range(0,self.cols):
        self.map[r].append(None)
    # image
    self.xmark = QtGui.QImage("x.png")
          
  def paintEvent(self, event):
    painter = QtGui.QPainter()
    painter.begin(self)
    self.draw(painter)
    painter.end()

  def mousePressEvent(self,event):
    #log.debug("mousePressEvent {0},{1}".format(event.x(),event.y()))
    x = event.x()
    y = event.y()
    size = self.size()
    w = size.width()
    h = size.height()
    r = int(y / (h / self.rows))
    c = int(x / (w / self.cols))
    log.debug("mousePressEvent row={0}, col={1}".format(r,c))
    #
    self.set(r,c,"X")
    self.repaint()

  def draw(self,p):
    size = self.size()
    w = size.width()
    h = size.height()
    pen = QtGui.QPen(QtGui.QColor(0,0,0),1,QtCore.Qt.SolidLine)
    p.setPen(pen)
    p.setBrush(QtCore.Qt.NoBrush)
    p.drawRect(0,0,w-1,h-1)
    # draw grid by rows
    step = int(round(h / self.rows))
    for i in range(step, h, step):
      p.drawLine(0,i,w,i)
    # draw grid by cols
    step = int(round(w / self.cols))
    for i in range(step, w, step):
      p.drawLine(i,0,i,h)
    # scaled image
    image = self.xmark.scaled(w / self.cols, h / self.rows)
    # draw unit
    for r in range(0,self.rows):
      for c in range(0,self.cols):
        if self.map[r][c] is not None:
          x = c * round(w / self.cols)
          y = r * round(h / self.rows)
          p.drawImage(x,y,image)
    del image
        
  def set(self,row,col,value=None):
    self.map[row][col] = value
        
    
class Ui(QtGui.QWidget):
  
  def __init__(self):
    super().__init__()
    self.init_layout()
    
  def init_layout(self):
    #
    self.setGeometry(150,150,150,150)
    self.setWindowTitle("TTT UI")
    #
    self.board = Board()
    self.board2 = Board()
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(self.board)
    hbox.addWidget(self.board2)
    self.setLayout(hbox)
    #
    self.show()
    
def run():
  app = QtGui.QApplication(sys.argv)
  ui = Ui()
  app.exec_()
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  run()
  
  
  
    