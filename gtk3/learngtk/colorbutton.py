#!/usr/bin/env python

from gi.repository import Gtk

def color_selected(colorbutton):
    print("Colour selected:", colorbutton.get_color())

window = Gtk.Window()
window.set_default_size(200, -1)
window.connect("destroy", lambda q: Gtk.main_quit())

colorbutton = Gtk.ColorButton()
colorbutton.connect("color-set", color_selected)
window.add(colorbutton)

window.show_all()

Gtk.main()
