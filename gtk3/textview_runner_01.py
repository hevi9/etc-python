#!/usr/bin/python3

import logging
log = logging.getLogger(__name__)
from gi.repository import Gtk, Gdk 

class Runner(Gtk.Window):
  def __init__(self):
    super().__init__(title="TextView Runner 01")
    self.connect("delete-event",self.close)
    self.make_layout()
    
  def make_layout(self):
    c = Gtk.VBox()
    self.add(c)
    #
    w = self.combo = Gtk.ComboBoxText.new_with_entry()
    w.connect("key-press-event",self.on_combo_keypress)
    w.connect("changed",self.combo_changed)
    #w.connect("activate",self.on_combo_activate)    
    c.pack_start(w,False,False,0)    
    #
    d = Gtk.ScrolledWindow()
    c.pack_start(d,True,True,0)
    #
    self.buffer = Gtk.TextBuffer()
    w = Gtk.TextView(buffer=self.buffer)
    d.add(w)
    
  def close(self,window,arg):
    log.debug("quitting")
    Gtk.main_quit()        
    
  def on_combo_keypress(self,w,e,d):
    log.debug("on_combo_keypress")

  def on_combo_activate(self,w,d):
    log.debug("on_combo_activate")

    
  def combo_changed(self,w):
    log.debug("combo_changed {0}".format(w.get_active_text()))
    
  def run(self):
    log.debug("running")
    self.show_all()
    Gtk.main()

def run():
  w = Runner()
  w.run()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  run()