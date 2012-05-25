#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, -1)
window.connect("destroy", lambda q: Gtk.main_quit())

filechooserbutton = Gtk.FileChooserButton()
filechooserbutton.set_title("FileChooserButton")
window.add(filechooserbutton)

window.show_all()

Gtk.main()
