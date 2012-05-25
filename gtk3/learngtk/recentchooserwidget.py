#!/usr/bin/env python

from gi.repository import Gtk

def retrieve_info(button):
    selection = recentchooser.get_current_item()
    print("Display name: %s" % selection.get_display_name())
    print("File URI: %s" % selection.get_uri())
    print("Last application: %s" % selection.last_application())

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
window.add(vbox)

recentchooser = Gtk.RecentChooserWidget()
vbox.pack_start(recentchooser, True, True, 0)

button = Gtk.Button(label="Recent Information")
button.connect("clicked", retrieve_info)
vbox.pack_start(button, False, False, 0)

window.show_all()

Gtk.main()
