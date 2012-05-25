#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

buttonbox = Gtk.HButtonBox()
window.add(buttonbox)

button = Gtk.Button(label="Button 1")
buttonbox.add(button)
button = Gtk.Button(label="Button 2")
buttonbox.add(button)
button = Gtk.Button(label="Button 3")
buttonbox.add(button)

window.show_all()

Gtk.main()
