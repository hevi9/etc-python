#!/usr/bin/env python

from gi.repository import Gtk

def application_activated(appchooserwidget, appinfo):
    print("Application activated: %s" % appinfo.get_name())

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

appchooserwidget = Gtk.AppChooserWidget(content_type="audio/flac")
appchooserwidget.connect("application-activated", application_activated)
window.add(appchooserwidget)

window.show_all()

Gtk.main()
