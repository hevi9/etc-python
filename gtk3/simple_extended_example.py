#!/usr/bin/python3

from gi.repository import Gtk

class MyWindow(Gtk.Window):
  
  def __init__(self):
    super().__init__(title="Simple Extended Example")
    
    self.button = Gtk.Button(label="CLICK")
    self.button.connect("clicked",self.on_button_clicked)
    self.add(self.button)
    
  def on_button_clicked(self,widget):
    print("on_button_clicked")
    
win = MyWindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()

Gtk.main()