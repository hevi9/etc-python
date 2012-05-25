#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

scalebutton = Gtk.ScaleButton(icons=(Gtk.STOCK_ZOOM_IN, Gtk.STOCK_ZOOM_OUT))
window.add(scalebutton)

window.show_all()

Gtk.main()
