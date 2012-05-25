#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

table = Gtk.Table(n_rows=3, n_columns=3, homogeneous=True)
window.add(table)

button = Gtk.Button(label="Button 1")
table.attach(button, 0, 1, 0, 1, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0, 0)
button = Gtk.Button(label="Button 2")
table.attach(button, 1, 3, 0, 1, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0, 0)
button = Gtk.Button(label="Button 3")
table.attach(button, 0, 1, 1, 3, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0, 0)
button = Gtk.Button(label="Button 4")
table.attach(button, 1, 3, 1, 3, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0, 0)

window.show_all()

Gtk.main()
