#!/usr/bin/env python

from gi.repository import Gtk

def application_activated(appchooserbutton):
    print("Application activated: %s" % appchooserbutton.get_app_info().get_name())

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

appchooserbutton = Gtk.AppChooserButton(content_type="audio/flac")
appchooserbutton.connect("changed", application_activated)
window.add(appchooserbutton)

window.show_all()

Gtk.main()
