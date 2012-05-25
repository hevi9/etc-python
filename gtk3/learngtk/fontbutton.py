#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, -1)
window.connect("destroy", lambda q: Gtk.main_quit())

fontbutton = Gtk.FontButton()
window.add(fontbutton)

window.show_all()

Gtk.main()
