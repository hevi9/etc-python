#!/usr/bin/env python

from gi.repository import Gtk

def color_selected(widget):
    print("Colour selected: %s" % colorselection.get_current_color())

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

colorselection = Gtk.ColorSelection()
colorselection.connect("color-changed", color_selected)
window.add(colorselection)

window.show_all()

Gtk.main()
