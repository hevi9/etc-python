#!/usr/bin/env python

from gi.repository import Gtk

count = 0

def push_button_clicked(button):
    global count
    count += 1
    statusbar.push(context_id, "Message number %s" % str(count))

def pop_button_clicked(button):
    statusbar.pop(context_id)

window = Gtk.Window()
window.set_default_size(200, -1)
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
window.add(vbox)

button_push = Gtk.Button(label="Push Message")
button_push.connect("clicked", push_button_clicked)
vbox.pack_start(button_push, False, False, 0)

button_pop = Gtk.Button(label="Pop Message")
button_pop.connect("clicked", pop_button_clicked)
vbox.pack_start(button_pop, False, False, 0)

statusbar = Gtk.Statusbar()
context_id = statusbar.get_context_id("Example")
vbox.pack_end(statusbar, False, False, 0)

window.show_all()

Gtk.main()
