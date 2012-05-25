#!/usr/bin/python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(400, 250)
window.connect("destroy", lambda q: Gtk.main_quit())

table = Gtk.Table(n_rows=2, n_columns=2, homogeneous=False)
window.add(table)

layout = Gtk.Layout()
layout.set_size(600, 400)
table.attach(layout, 0, 1, 0, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0, 0)

vadjustment = layout.get_vadjustment()
vscrollbar = Gtk.VScrollbar(adjustment=vadjustment)
table.attach(vscrollbar, 1, 2, 0, 1, Gtk.AttachOptions.SHRINK, Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL, 0, 0)
hadjustment = layout.get_hadjustment()
hscrollbar = Gtk.HScrollbar(adjustment=hadjustment)
table.attach(hscrollbar, 0, 1, 1, 2, Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.SHRINK, 0, 0)

button = Gtk.Button(label="Button 1")
layout.put(button, 180, 220)
button = Gtk.Button(label="Button 2")
layout.put(button, 20, 100)
button = Gtk.Button(label="Button 3")
layout.put(button, 450, 320)

window.show_all()

Gtk.main()
