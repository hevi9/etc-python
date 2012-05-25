#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

adjustment = Gtk.Adjustment(value=5, lower=0, upper=10, step_increment=1, page_increment=1, page_size=0)
spinbutton = Gtk.SpinButton(adjustment=adjustment)
window.add(spinbutton)

window.show_all()

Gtk.main()
