#!/usr/bin/env python

from gi.repository import Gtk

def tooltip_queried(item, x, y, key_mode, tooltip, text):
    tooltip.set_text("Advanced Tooltip on %s" % text)
    return True

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=True, spacing=5)
window.add(vbox)

button = Gtk.Button(label="Button")
button.set_has_tooltip(True)
button.connect("query-tooltip", tooltip_queried, "Button")
vbox.pack_start(button, False, False, 0)

label = Gtk.Label(label="Label")
label.set_has_tooltip(True)
label.connect("query-tooltip", tooltip_queried, "Label")
vbox.pack_start(label, False, False, 0)

entry = Gtk.Entry()
entry.set_has_tooltip(True)
entry.connect("query-tooltip", tooltip_queried, "Entry")
vbox.pack_start(entry, False, False, 0)

window.show_all()

Gtk.main()
