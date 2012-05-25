#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(400, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

hbox = Gtk.HBox(homogeneous=True, spacing=5)
window.add(hbox)

hadjustment = Gtk.Adjustment(value=0, lower=0, upper=100, step_increment=1, page_increment=10, page_size=0)
hscale = Gtk.HScale(adjustment=hadjustment)
hbox.pack_start(hscale, True, True, 0)

vadjustment = Gtk.Adjustment(value=0, lower=0, upper=100, step_increment=1, page_increment=10, page_size=0)
vscale = Gtk.VScale(adjustment=vadjustment)
hbox.pack_start(vscale, True, True, 0)

window.show_all()

Gtk.main()
