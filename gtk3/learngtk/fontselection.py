#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

fontselection = Gtk.FontSelection()
window.add(fontselection)

window.show_all()

Gtk.main()
