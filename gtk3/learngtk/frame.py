#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, 200)
window.set_border_width(5)
window.connect("destroy", lambda q: Gtk.main_quit())

frame = Gtk.Frame(label="Frame")
window.add(frame)

window.show_all()

Gtk.main()
