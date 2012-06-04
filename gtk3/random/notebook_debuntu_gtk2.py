#!/usr/bin/env python

"""
http://coding.debuntu.org/python-gtk-how-set-gtk.notebook-tab-custom-widget

gtk.Notebook is a great feature as it help keep your application footprint on the desktop occupation low. I personnally would not even think of using a web brower without a tab feature as it would take me a help of a time to go from one application to another.

A gtk.Notebook page is composed of a child widget and a label gtk.Widget. From there on, we can fit anything we like in a tab label such as an icon on the side representing the content, a title and a handy close button on the right side a bit like firefox's tabs.

This tutorial will detail how to customize the content of a Notebook tab label but really is a kickstart to any plausible gui arrangement.

Customized GTK Notebook tabsCustomized GTK Notebook tabsBy running the code below, you will get the window shown in the image.

The tab label is composed of an HBox to hold the 3 components: the gtk.Image, the gtk.Label and the gtk.Button.
"""

import gtk
import sys
 
#global variables
window = None
notebook = None
 
class MyNotebook(gtk.Notebook):
 
  def __init__(self):
    gtk.Notebook.__init__(self)
    #set the tab properties
    self.set_property('homogeneous', True)
    #we do not show the tab if there is only one tab i total
    self.set_property('show-tabs', False)
 
  def new_tab(self):
    #we create a "Random" image to put in the tab
    icons = [gtk.STOCK_ABOUT, gtk.STOCK_ADD, gtk.STOCK_APPLY, gtk.STOCK_BOLD]
    image = gtk.Image()
    nbpages = self.get_n_pages()
    icon = icons[nbpages%len(icons)]
    image.set_from_stock(icon, gtk.ICON_SIZE_DIALOG)
    self.append_page(image)
   
    #we want to show the tabs if there is more than 1
    if nbpages + 1 > 1:
      self.set_property('show-tabs', True)
    #creation of a custom tab. the left image and
    #the title are made of the stock icon name
    #we pass the child of the tab so we can find the
    #tab back upon closure
    label = self.create_tab_label(icon, image)
    label.show_all()
   
    self.set_tab_label_packing(image, True, True, gtk.PACK_START)
    self.set_tab_label(image, label)
    image.show_all()
    self.set_current_page(nbpages)
 
  def create_tab_label(self, title, tab_child):
    box = gtk.HBox()
    icon = gtk.Image()
    icon.set_from_stock(title, gtk.ICON_SIZE_MENU)
    label = gtk.Label(title)
    closebtn = gtk.Button()
    #the close button is made of an empty button
    #where we set an image
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
    closebtn.connect("clicked", self.close_tab, tab_child)
    closebtn.set_image(image)
    closebtn.set_relief(gtk.RELIEF_NONE)
    box.pack_start(icon, False, False)
    box.pack_start(label, True, True)
    box.pack_end(closebtn, False, False)
    return box
 
  def close_tab(self, widget, child):
    pagenum = self.page_num(child)
 
    if pagenum != -1:
      self.remove_page(pagenum)
      child.destroy()
      if self.get_n_pages() == 1:
        self.set_property('show-tabs', False)
 
def on_destroy(win):
  gtk.main_quit()
 
def on_delete_event(widget, event):
  gtk.main_quit()
 
def new_tab(widget):
  notebook.new_tab()
 
if __name__ == '__main__':
 
  window = gtk.Window()
  window.set_title("Custom Gtk.Notebook Tabs example")
  window.resize(600,400)
  box = gtk.VBox()
  button = gtk.Button("New Tab")
  box.pack_start(button,False)
  button.connect("clicked", new_tab)
  notebook = MyNotebook()
  box.pack_start(notebook)
  window.add(box)
  window.connect("destroy", on_destroy)
  window.connect("delete-event", on_delete_event)
  window.show_all()
  gtk.main()
  sys.exit(0)