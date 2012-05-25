#!/usr/bin/env python

from gi.repository import Gtk

def display_menu(widget, event):
    if event.button == 3:
        menu.popup(None, None, None, None, event.button, event.time)
        menu.show_all()

def display_text(widget):
    print("Item clicked was %s" % widget.get_child().get_text())

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

eventbox = Gtk.EventBox()
eventbox.connect("button-release-event", display_menu)
window.add(eventbox)

menu = Gtk.Menu()
menuitem = Gtk.MenuItem(label="MenuItem 1")
menuitem.connect("activate", display_text)
menu.append(menuitem)
menuitem = Gtk.MenuItem(label="MenuItem 2")
menuitem.connect("activate", display_text)
menu.append(menuitem)
menuitem = Gtk.MenuItem(label="MenuItem 3")
menuitem.connect("activate", display_text)
menu.append(menuitem)

window.show_all()

Gtk.main()
