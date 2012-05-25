#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=True, spacing=5)
window.add(vbox)

label = Gtk.Label(label="Label 1")
vbox.pack_start(label, False, False, 0)
label = Gtk.Label(label="Label 2")
vbox.pack_start(label, False, False, 0)

hbox = Gtk.HBox(homogeneous=True, spacing=5)
vbox.pack_start(hbox, False, False, 0)

label = Gtk.Label(label="Label 3")
hbox.pack_start(label, False, False, 0)
label = Gtk.Label(label="Label 4")
hbox.pack_start(label, False, False, 0)

window.show_all()

Gtk.main()
