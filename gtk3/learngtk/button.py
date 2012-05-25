#!/usr/bin/env python

from gi.repository import Gtk

def button_clicked(button):
    print("Button clicked")

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

button = Gtk.Button(label="Button")
button.connect("clicked", button_clicked)
window.add(button)

window.show_all()

Gtk.main()
