#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

hbox = Gtk.HBox(homogeneous=False, spacing=5)
window.add(hbox)

vbox = Gtk.VBox(homogeneous=False, spacing=5)
hbox.pack_start(vbox, True, True, 0)

label = Gtk.Label(label="This is a standard label.")
vbox.pack_start(label, True, True, 0)
label = Gtk.Label(label="This is a left-justified label.\n With multiple lines.")
label.set_justify(Gtk.Justification.LEFT)
vbox.pack_start(label, True, True, 0)
label = Gtk.Label(label="This is a center-justified label.\n With multiple lines.")
label.set_justify(Gtk.Justification.CENTER)
vbox.pack_start(label, True, True, 0)
label = Gtk.Label(label="This is a right-justified label.\n With multiple lines.")
label.set_justify(Gtk.Justification.RIGHT)
vbox.pack_start(label, True, True, 0)

vbox = Gtk.VBox(homogeneous=False, spacing=5)
hbox.pack_start(vbox, True, True, 0)

label = Gtk.Label(label="This is a line-wrapped label spread over multiple lines. "
                        "It supports multiple lines and correctly inserts several    spaces   .")
label.set_line_wrap(True)
vbox.pack_start(label, True, True, 0)
label = Gtk.Label(label="This label is line-wrapped and filled. It takes the entire space "
                        "allocated to it.\n\nIt also supports multiple lines and correctly inserts   many   spaces   .")
label.set_line_wrap(True)
label.set_justify(Gtk.Justification.FILL)
vbox.pack_start(label, True, True, 0)

window.show_all()

Gtk.main()
