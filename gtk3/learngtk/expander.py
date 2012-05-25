#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

label = Gtk.Label(label="Label within an Expander")
label.set_size_request(200, 200)

expander = Gtk.Expander(label="Expander")
expander.add(label)
window.add(expander)

window.show_all()

Gtk.main()
