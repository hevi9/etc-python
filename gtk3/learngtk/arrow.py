#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(400, 100)
window.connect("destroy", lambda q: Gtk.main_quit())

hbox = Gtk.HBox(homogeneous=True, spacing=5)
window.add(hbox)

arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.LEFT, shadow_type=Gtk.ShadowType.NONE)
hbox.pack_start(arrow, False, False, 0)
arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.UP, shadow_type=Gtk.ShadowType.NONE)
hbox.pack_start(arrow, False, False, 0)
arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.RIGHT, shadow_type=Gtk.ShadowType.NONE)
hbox.pack_start(arrow, False, False, 0)
arrow = Gtk.Arrow(arrow_type=Gtk.ArrowType.DOWN, shadow_type=Gtk.ShadowType.NONE)
hbox.pack_start(arrow, False, False, 0)

window.show_all()

Gtk.main()
