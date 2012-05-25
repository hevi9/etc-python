#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=True, spacing=5)
window.add(vbox)

button = Gtk.Button(label="Button")
button.set_tooltip_text("Button Tooltip")
vbox.pack_start(button, False, False, 0)
label = Gtk.Label(label="Label")
label.set_tooltip_text("Label Tooltip")
vbox.pack_start(label, False, False, 0)
entry = Gtk.Entry()
entry.set_tooltip_text("Entry Tooltip")
vbox.pack_start(entry, False, False, 0)

window.show_all()

Gtk.main()
