#!/usr/bin/env python
# example notebook.py

import pygtk
pygtk.require('2.0')
import gtk

class NotebookExample:
  def add_icon_to_button(self, button):
    iconBox = gtk.HBox(False, 0)
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
    gtk.Button.set_relief(button, gtk.RELIEF_NONE)
    #gtk.Button.set_focus_on_click(button,False)
    settings = gtk.Widget.get_settings (button)
    (w,h) = gtk.icon_size_lookup_for_settings (settings, gtk.ICON_SIZE_MENU)
    gtk.Widget.set_size_request (button, w + 4, h + 4)
    image.show()
    iconBox.pack_start(image, True, False, 0)
    button.add(iconBox)
    iconBox.show()
    return


  def create_custom_tab(self, text, child):
    #create a custom tab for notebook containing a
    #label and a button with STOCK_ICON
    eventBox = gtk.EventBox()
    tabBox = gtk.HBox(False, 2)
    tabLabel = gtk.Label(text)

    tabButton=gtk.Button()
    tabButton.connect('clicked', self.remove_book, child)

    #Add a picture on a button
    self.add_icon_to_button(tabButton)
    iconBox = gtk.HBox(False, 0)

    eventBox.show()
    tabButton.show()
    tabLabel.show()

    tabBox.pack_start(tabLabel, False)
    tabBox.pack_start(tabButton, False)

    # needed, otherwise even calling show_all on the notebook won't
    # make the hbox contents appear.
    tabBox.show_all()
    eventBox.add(tabBox)
    return eventBox


  # Remove a page from the notebook
  def remove_book(self, button, child):
    page = self.notebook.page_num(child)
    if page != -1:
      self.notebook.remove_page(page)
    # Need to refresh the widget --
    # This forces the widget to redraw itself.
    self.notebook.queue_draw_area(0, 0, -1, -1)


  def remove_current_book(self, *arguments, **keywords):
    page = self.notebook.get_current_page()
    if page != -1:
      self.notebook.remove_page(page)
    return True

  def delete(self, widget, event=None, *arguments, **keywords):
    gtk.main_quit()
    return False

  def add_new_book(self, *arguments, **keywords):
    self.page_number += 1
    frame = gtk.Frame("Frame %d" % self.page_number)
    frame.set_border_width(10)
    frame.set_size_request(100, 75)
    frame.show()
    label = gtk.Label("Inside of Frame %d" % self.page_number)
    frame.add(label)
    label.show()

    eventBox = self.create_custom_tab("Tab %d" % self.page_number, frame)
    self.notebook.append_page(frame, eventBox)

    # Set the new page
    pages = gtk.Notebook.get_n_pages(self.notebook)
    self.notebook.set_current_page(pages - 1)
    return True
  
  def __init__(self):
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("delete_event", self.delete)
    window.set_border_width(10)

    # Create a new notebook
    self.notebook = gtk.Notebook()
    window.add(self.notebook)
    self.notebook.show()

    # key accelerators
    self.accel_group = gtk.AccelGroup()
    self.accel_group.connect_group(ord('q'), 
                     gtk.gdk.CONTROL_MASK, 
                     gtk.ACCEL_LOCKED, 
                     self.delete)
    self.accel_group.connect_group(ord('w'), 
                     gtk.gdk.CONTROL_MASK, 
                     gtk.ACCEL_LOCKED, 
                     self.remove_current_book)
    self.accel_group.connect_group(ord('t'), 
                     gtk.gdk.CONTROL_MASK, 
                     gtk.ACCEL_LOCKED, 
                     self.add_new_book)
                     
    window.add_accel_group(self.accel_group)

    # Add some tab pages for demonstrating
    for i in range(5):
      self.page_number = i
      self.add_new_book()

    # Set what page to start at (page 4)
    self.notebook.set_current_page(3)
    window.show()


def main():
  gtk.main()
  return 0


if __name__ == "__main__":
  NotebookExample()
  main()
