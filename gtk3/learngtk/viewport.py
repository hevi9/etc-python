#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

viewport = Gtk.Viewport()
viewport.set_size_request(200, 200)
vadjustment = viewport.get_vadjustment()
vscrollbar = Gtk.VScrollbar(adjustment=vadjustment)
hadjustment = viewport.get_hadjustment()
hscrollbar = Gtk.HScrollbar(adjustment=hadjustment)

table = Gtk.Table(n_rows=2, n_columns=2, homogeneous=False)
table.attach(viewport, 0, 1, 0, 1, Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND, 0, 0)
table.attach(vscrollbar, 1, 2, 0, 1, Gtk.AttachOptions.FILL | Gtk.AttachOptions.SHRINK, Gtk.AttachOptions.FILL | Gtk.AttachOptions.SHRINK, 0, 0)
table.attach(hscrollbar, 0, 1, 1, 2, Gtk.AttachOptions.FILL | Gtk.AttachOptions.SHRINK, Gtk.AttachOptions.FILL | Gtk.AttachOptions.SHRINK, 0, 0)
window.add(table)

table = Gtk.Table()
table.set_homogeneous(True)
viewport.add(table)
for i in range(0, 15):
    button = Gtk.Button(label=str(i + 1))
    table.attach(button, 0 + i, 1 + i, 0 + i, 1 + i, Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.FILL | Gtk.AttachOptions.EXPAND, 0, 0)

window.show_all()

Gtk.main()
