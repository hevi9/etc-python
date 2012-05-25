#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

scrolledwindow = Gtk.ScrolledWindow()
window.add(scrolledwindow)

textview = Gtk.TextView()
scrolledwindow.add(textview)

window.show_all()

Gtk.main()
