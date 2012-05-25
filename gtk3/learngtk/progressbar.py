#!/usr/bin/env python

from gi.repository import Gtk

def display_text(checkbutton):
    progressbar.set_show_text(checkbutton.get_active())

window = Gtk.Window()
window.set_default_size(200, -1)
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
window.add(vbox)

progressbar = Gtk.ProgressBar()
vbox.pack_start(progressbar, False, False, 0)

checkbutton = Gtk.CheckButton(label="Display text")
checkbutton.connect("toggled", display_text)
vbox.pack_start(checkbutton, False, False, 0)

window.show_all()

Gtk.main()
