#!/usr/bin/env python

from gi.repository import Gtk

def spinner_started(button):
    spinner.start()

def spinner_stopped(button):
    spinner.stop()

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
window.add(vbox)

spinner = Gtk.Spinner()
vbox.add(spinner)

hbox = Gtk.HBox(homogeneous=True, spacing=5)
vbox.pack_start(hbox, False, False, 0)

button_start = Gtk.Button(label="Start")
button_start.connect("clicked", spinner_started)
hbox.pack_start(button_start, True, True, 0)
button_stop = Gtk.Button(label="Stop")
button_stop.connect("clicked", spinner_stopped)
hbox.pack_start(button_stop, True, True, 0)

window.show_all()

Gtk.main()
