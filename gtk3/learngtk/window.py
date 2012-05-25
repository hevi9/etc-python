#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_title("Window")
window.connect("destroy", lambda q: Gtk.main_quit())

window.show_all()

Gtk.main()
