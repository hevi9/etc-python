#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore # http://www.riverbankcomputing.com/static/Docs/PyQt4/html/qtgui.html
# http://zetcode.com/tutorials/pyqt4/
import logging
log = logging.getLogger(__name__)

##############################################################################
## Game Board

class Board(QtGui.QWidget):
  
  def __init__(self,ui):
    super().__init__()
    self.ui = ui
    self.setMinimumSize(200, 200)
    self.rows = 5
    self.cols = 5
    ## init Map
    self.map = list() # rows
    for r in range(0,self.rows):
      self.map.append(list())
      for c in range(0,self.cols):
        self.map[r].append(None)
    # image
    self.xmark = QtGui.QImage("x.png")
    self.omark = QtGui.QImage("o.png")
          
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
    self.ui.place(r,c)

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
    ximage = self.xmark.scaled(w / self.cols, h / self.rows)
    oimage = self.omark.scaled(w / self.cols, h / self.rows)
    # draw unit
    for r in range(0,self.rows):
      for c in range(0,self.cols):
        if self.map[r][c] is not None:
          x = c * round(w / self.cols)
          y = r * round(h / self.rows)
          if self.map[r][c] == "X":
            p.drawImage(x,y,ximage)
          else:
            p.drawImage(x,y,oimage)
    del ximage
    del oimage
        
  def set(self,row,col,value=None):
    self.map[row][col] = value
    self.repaint()

##############################################################################
## Ui
            
class Ui(QtGui.QWidget):
  
  def __init__(self):
    super().__init__()
    self.init_layout()
    
  def init_layout(self):
    vbox = QtGui.QVBoxLayout()
    #
    self.status = QtGui.QLabel("status")
    vbox.addWidget(self.status)
    #
    self.board = Board(self)
    vbox.addWidget(self.board,1) # 1 = resize this part
    #
    hbox = QtGui.QHBoxLayout()
    vbox.addLayout(hbox)
    self.host = QtGui.QLineEdit("localhost")
    hbox.addWidget(self.host)
    self.port = QtGui.QLineEdit("12345")
    hbox.addWidget(self.port)
    self.go = QtGui.QPushButton("Go")
    self.go.clicked.connect(self.go_clicked)
    hbox.addWidget(self.go)
    #
    self.msgs = QtGui.QTextEdit()
    self.msgs.setReadOnly(True)
    self.msgs.setSizePolicy(QtGui.QSizePolicy
                            (QtGui.QSizePolicy.Expanding,
                             QtGui.QSizePolicy.Minimum))
    vbox.addWidget(self.msgs)
    self.enter = QtGui.QLineEdit()
    self.enter.returnPressed.connect(self.enter_returnPressed)
    vbox.addWidget(self.enter)
    #
    self.setGeometry(150,150,150,150)
    self.setWindowTitle("TTT UI")
    self.setLayout(vbox)
    self.show()
    
  def msg(self,text):
    #self.msgs.append(text)
    self.msgs.insertHtml(text + "<br/>\n")
    sb = self.msgs.verticalScrollBar()
    sb.setValue(sb.maximum())
    
  def error(self,text):
    self.msg('<div style="color:red">Error {0}</div>'.format(text))
        
  def place(self,row,col):
    self.msg('<div style="color:blue">Place ({0},{1})</div>'.format(row,col))
    #
    if row * col % 2 == 0:
      self.board.set(row,col,"X")
    else:
      self.board.set(row,col,"O")    
    
  def enter_returnPressed(self):
    log.debug("enter_returnPressed " + self.enter.text())
    self.msg("<i>" + self.enter.text() + "</i>")
    self.enter.clear()
  
  def go_clicked(self):    
    host = self.host.text()
    try:
      port = int(self.port.text())
    except ValueError as ex:
      self.error(str(ex))
      return 
    log.debug("go_clicked {0} {1}".format(host,port))
    self.msg('<div style="color:green">Connect to {0} {1}</div>'.format(host,port))
  
##############################################################################
##    
    
def run():
  app = QtGui.QApplication(sys.argv)
  ui = Ui()
  app.exec_()
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  run()
  
  
  
    