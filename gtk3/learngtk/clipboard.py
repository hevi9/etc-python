#!/usr/bin/env python

from gi.repository import Gtk, Gdk

def copy(widget, mode):
    clipboard.set_text(entry.get_text(), -1)
        
    if mode == "cut":
        entry.set_text("")
    
def paste(widget):
    text = clipboard.wait_for_text()
    
    if text != None:
        entry.set_text(text)

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

hbox = Gtk.HBox(homogeneous=False, spacing=5)
window.add(hbox)
        
entry = Gtk.Entry()
hbox.pack_start(entry, False, False, 0)

hbox2 = Gtk.HBox(homogeneous=True, spacing=5)
hbox.pack_start(hbox2, True, True, 0)

button_cut = Gtk.Button(label="Cut Text")
button_cut.connect("clicked", copy, "cut")
hbox2.pack_start(button_cut, True, True, 0)
button_copy = Gtk.Button(label="Copy Text")
button_copy.connect("clicked", copy, "copy")
hbox2.pack_start(button_copy, True, True, 0)
button_paste = Gtk.Button(label="Paste Text")
button_paste.connect("clicked", paste)
hbox2.pack_start(button_paste, True, True, 0)

clipboard = Gtk.Clipboard()

window.show_all()

Gtk.main()
