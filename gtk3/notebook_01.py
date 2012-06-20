#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
"""
What is this.
"""

##############################################################################
## Uses

import sys
import os
import logging
log = logging.getLogger(__name__)
from gi.repository import Gtk, GObject, Pango

##############################################################################
## Code

class MyWindow(Gtk.Window):
  """ """
  
  def __init__(self):
    super().__init__(title=os.path.basename(sys.argv[0]))
    self.connect("delete-event",self.close)
    self.make_layout()
    self.set_default_size(-1,200)
    
  def make_layout(self):
    nb = Gtk.Notebook()
    self.add(nb)
    #
    vbox = Gtk.VBox()
    nb.append_page(vbox,Gtk.Label(label="Page"))
    #
    button = Gtk.Button(label="A Button")
    button.connect("clicked",self.on_button_clicked)
    vbox.add(button)
        
  def close(self,window,arg):
    log.debug("quitting")
    Gtk.main_quit()            
        
  def on_button_clicked(self,w):
    log.debug("on_button_clicked")
    generator = self.on_idle()
    GObject.idle_add(generator.__next__)

  def on_idle(self):    
    log.debug("on_idle yield 1")
    yield True
    log.debug("on_idle yield 2")
    yield True    
    log.debug("on_idle yield 3")
    yield False    
        
  def run(self):
    log.debug("running")
    self.show_all()
    Gtk.main()

##############################################################################
## Deploy & Run

def run():
  w = MyWindow()
  w.run()

##############################################################################
## This file start
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  run()
