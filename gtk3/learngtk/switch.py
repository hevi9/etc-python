#!/usr/bin/env python

from gi.repository import Gtk

def switch_toggled(switch, state):
    print("Switch toggled %s" % ("off", "on")[switch.get_active()])

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

switch = Gtk.Switch()
switch.connect("notify::active", switch_toggled)
window.add(switch)

window.show_all()

Gtk.main()
