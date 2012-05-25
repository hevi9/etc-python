#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(400, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

hbox = Gtk.HBox(homogeneous=False, spacing=5)
window.add(hbox)

hpane = Gtk.HPaned()
hbox.pack_start(hpane, True, True, 0)

label = Gtk.Label(label="HPane Left")
hpane.add1(label)
label = Gtk.Label(label="HPane Right")
hpane.add2(label)

vpane = Gtk.VPaned()
hbox.pack_start(vpane, True, True, 0)

label = Gtk.Label(label="VPane Top")
vpane.add1(label)
label = Gtk.Label(label="VPane Bottom")
vpane.add2(label)

window.show_all()

Gtk.main()
