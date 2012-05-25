#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(400, 200)
window.connect("destroy", lambda q: Gtk.main_quit())
        
hbox = Gtk.HBox(homogeneous=False, spacing=5)
window.add(hbox)

hseparator = Gtk.HSeparator()
hbox.pack_start(hseparator, True, True, 0)
vseparator = Gtk.VSeparator()
hbox.pack_start(vseparator, True, True, 0)

window.show_all()

Gtk.main()
