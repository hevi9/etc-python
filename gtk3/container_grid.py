#!/usr/bin/python3

from gi.repository import Gtk

class TableWindow(Gtk.Window):
  
  def __init__(self):
    super().__init__(title="Grid Container Example")
    
    c = Gtk.Grid()
    self.add(c)
    
    b1 = Gtk.Button(label="Button 1")
    b2 = Gtk.Button(label="Button 2")
    b3 = Gtk.Button(label="Button 3")    
    b4 = Gtk.Button(label="Button 4")
    b5 = Gtk.Button(label="Button 5")
    b6 = Gtk.Button(label="Button 6")
    
    c.add(b1)
    c.attach(b2, 1, 0, 2, 1)
    c.attach_next_to(b3,b1,Gtk.PositionType.BOTTOM, 1, 2)
    c.attach_next_to(b4, b3, Gtk.PositionType.RIGHT, 2, 1)
    c.attach(b5, 1, 2, 1, 1)
    c.attach_next_to(b6, b5, Gtk.PositionType.RIGHT, 1, 1)

    
win = TableWindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()

Gtk.main()                