#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

linkbutton = Gtk.LinkButton(label="Link Button")
linkbutton.set_uri("http://www.learnpygtk.org/")
window.add(linkbutton)

window.show_all()

Gtk.main()
