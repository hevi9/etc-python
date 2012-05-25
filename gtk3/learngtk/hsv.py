#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

hsv = Gtk.HSV()
hsv.set_metrics(200, 20)
window.add(hsv)

window.show_all()

Gtk.main()
