#!/usr/bin/python3

from gi.repository import Gtk

class TableWindow(Gtk.Window):
  
  def __init__(self):
    super().__init__(title="Table Container Example")
    
    c = Gtk.Table(3,3,True)
    self.add(c)
    
    b1 = Gtk.Button(label="Button 1")
    b2 = Gtk.Button(label="Button 2")
    b3 = Gtk.Button(label="Button 3")    
    b4 = Gtk.Button(label="Button 4")
    b5 = Gtk.Button(label="Button 5")
    b6 = Gtk.Button(label="Button 6")
    
    c.attach(b1,0, 1, 0, 1)    
    c.attach(b2,1, 3, 0, 1)    
    c.attach(b3,0, 1, 1, 3)            
    c.attach(b4,1, 3, 1, 2)    
    c.attach(b5,1, 2, 2, 3)    
    c.attach(b6,2, 3, 2, 3)
    
win = TableWindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()

Gtk.main()                