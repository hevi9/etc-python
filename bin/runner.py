#!/usr/bin/python3

import sys
import os
import re
import subprocess as sp
import logging
log = logging.getLogger(__name__)
from gi.repository import Gtk, GObject, Pango

re_space = re.compile(r'^\s*$')

start_text = """
********

Start text


********
""".strip()

class style:
  spacing = 1

class Runner(Gtk.Window):
  def __init__(self):
    super().__init__(title=os.path.basename(sys.argv[0]))
    self.connect("delete-event",self.close)
    self.make_layout()
    self.make_accel()
    self.set_default_size(-1,400)
    self.process_cur = None
    
  def make_layout(self):
    #
    vbox = Gtk.VBox()
    self.add(vbox)
    #
    self.cstore = Gtk.ListStore(str)
    ##
    hbox = Gtk.HBox()
    vbox.pack_start(hbox,False,False,style.spacing)
    ##
    combo = self.combo =Gtk.ComboBox.new_with_model_and_entry(self.cstore)
    combo.connect("changed",self.on_combo_changed)
    combo.set_entry_text_column(0)
    entry = combo.get_child()
    entry.connect("activate",self.on_run_clicked)
    hbox.pack_start(combo, True, True, style.spacing)
    ##
    run = Gtk.Button.new_from_stock(Gtk.STOCK_MEDIA_PLAY)
    run.connect("clicked",self.on_run_clicked)
    #run.set_property("label",None)
    hbox.pack_start(run, False, False, style.spacing)
    #
    scroll = Gtk.ScrolledWindow()    
    vbox.pack_start(scroll,True,True,0)
    ##
    self.stdout = Gtk.TextBuffer()
    self.stdout.set_text(start_text)
    ##
    text = self.text_stdout = Gtk.TextView(buffer=self.stdout)
    fd = Pango.FontDescription("Monospace 10")
    text.modify_font(fd)
    scroll.add(text)
    
  def make_accel(self):
    accels = Gtk.AccelGroup()
    #accels.connect_by_path("e",self.on_run_clicked)
    key,mod = Gtk.accelerator_parse("Return")
    accels.connect(key,mod,0,self.on_accel_return)
    #entry = self.combo.get_child()
    #entry.add_accel_group(accels)
    
  def close(self,window,arg):
    log.debug("quitting")
    Gtk.main_quit()            
    
  def on_accel_return(self,a,b,c,d):
    log.debug("on_accel_return")
    
  def on_run_clicked(self,w):
    log.debug("on_run_clicked")
    runtext = self.combo.get_child().get_text()
    ## checks
    if re_space.match(runtext):
      self.error("enter command to run")
      return
    append = True
    for row in self.cstore:
      if runtext == row[0]:
        append = False
    if append is True:
      self.cstore.append([runtext])
    self.run_process(runtext)

  def on_idle(self):
    #log.debug("on_idle")
    text = self.process_cur.stdout.readline()
    if len(text) == 0:
      return False
    else:
      text = text.decode("utf-8")
      self.stdout.insert(self.stdout.get_end_iter(),text)
      return True      
    
  def run_process(self,runtext):
    self.process_cur = sp.Popen([runtext],shell=True,stdout=sp.PIPE)
    #self.stdout.delete(self.stdout.get_start_iter(),
    #                   self.stdout.get_end_iter())
    tokill = self.stdout
    self.stdout = Gtk.TextBuffer()
    self.text_stdout.set_buffer(self.stdout)
    del tokill
    GObject.idle_add(self.on_idle)        
    
  def error(self,msg):
    self.stdout.insert(self.stdout.get_start_iter(),
                       "Error: " + msg + "\n")  
    
  def on_combo_changed(self,combo):
    iter = combo.get_active_iter()
    if iter is not None:
      model = combo.get_model()
      name = model[iter][0]
      log.debug("on_combo_changed model {0}".format(name))
    else:
      entry = combo.get_child()
      log.debug("on_combo_changed entry {0}".format(entry.get_text()))
    
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