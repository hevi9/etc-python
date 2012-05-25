#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

alignment = Gtk.Alignment(xalign=0.5, yalign=0.25, xscale=1.0, yscale=0.5)
window.add(alignment)

label = Gtk.Label(label="Label in an Alignment")
alignment.add(label)

window.show_all()

Gtk.main()
