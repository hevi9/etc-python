#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(300, 250)
window.connect("destroy", lambda q: Gtk.main_quit())

layout = Gtk.Layout()
window.add(layout)

button = Gtk.Button(label="Button 1")
layout.put(button, 50, 5)
button = Gtk.Button(label="Button 2")
layout.put(button, 235, 200)
button = Gtk.Button(label="Button 3")
layout.put(button, 145, 145)

window.show_all()

Gtk.main()
