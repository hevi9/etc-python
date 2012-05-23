#!/usr/bin/python3

from gi.repository import Gtk

class MyWindow(Gtk.Window):
  
  def __init__(self):
    super().__init__(title="Container Box Example")
    c = self.box = Gtk.Box(spacing=6)
    self.add(self.box)
    
    self.b1 = Gtk.Button(label="Button 1")
    self.b1.connect("clicked",self.on_b1_clicked)
    c.pack_start(self.b1, True, True, 0)
    
    self.b2 = Gtk.Button(label="Button 2")
    self.b2.connect("clicked",self.on_b2_clicked)
    c.pack_start(self.b2, True, True, 0)
    
  def on_b1_clicked(self,widget):
    print("on_b1_clicked")    
    
  def on_b2_clicked(self,widget):
    print("on_b2_clicked")
    
win = MyWindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()

Gtk.main()    