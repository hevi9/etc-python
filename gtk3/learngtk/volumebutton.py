#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

volumebutton = Gtk.VolumeButton()
window.add(volumebutton)

window.show_all()

Gtk.main()
