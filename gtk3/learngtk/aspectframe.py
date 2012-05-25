#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

aspectframe = Gtk.AspectFrame(label="Aspect Frame", xalign=0.5, yalign=0.5, ratio=1.0, obey_child=False)
window.add(aspectframe)

image = Gtk.Image()
image.set_from_file("gtk.png")
aspectframe.add(image)

window.show_all()

Gtk.main()
