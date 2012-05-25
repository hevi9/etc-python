#!/usr/bin/env python

from gi.repository import Gtk

def togglebutton_toggled(checkbutton):
    print(checkbutton.get_label(), "toggled %s" % ("off", "on")[checkbutton.get_active()])

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=True, spacing=5)
window.add(vbox)

checkbutton = Gtk.CheckButton(label="Toggle Button 1")
checkbutton.set_active(True)
checkbutton.connect("toggled", togglebutton_toggled)
vbox.pack_start(checkbutton, False, False, 0)

checkbutton = Gtk.CheckButton(label="Toggle Button 2")
checkbutton.connect("toggled", togglebutton_toggled)
vbox.pack_start(checkbutton, False, False, 0)

window.show_all()

Gtk.main()
