#!/usr/bin/env python

from gi.repository import Gtk

def radiobutton_toggled(radiobutton):
    if radiobutton.get_active():
        print(radiobutton.get_label(), "selected")

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=True, spacing=5)
window.add(vbox)

radiobutton = Gtk.RadioButton(group=None, label="Radio Button 1")
radiobutton.connect("toggled", radiobutton_toggled)
vbox.pack_start(radiobutton, False, False, 0)

radiobutton = Gtk.RadioButton(group=radiobutton, label="Radio Button 2")
radiobutton.connect("toggled", radiobutton_toggled)
radiobutton.set_active(True)
vbox.pack_start(radiobutton, False, False, 0)

radiobutton = Gtk.RadioButton(group=radiobutton, label="Radio Button 3")
radiobutton.connect("toggled", radiobutton_toggled)
vbox.pack_start(radiobutton, False, False, 0)

window.show_all()

Gtk.main()
