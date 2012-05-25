#!/usr/bin/env python

from gi.repository import Gtk

def item_clicked(menuitem):
    selection = recentchoosermenu.get_current_item()
    print("Display name: %s" % selection.get_display_name())
    print("File URI: %s" % selection.get_uri())
    print("Last application: %s" % selection.last_application())

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

menubar = Gtk.MenuBar()
window.add(menubar)

menuitem = Gtk.MenuItem(label="Recent Items")
menubar.append(menuitem)

recentchoosermenu = Gtk.RecentChooserMenu()
recentchoosermenu.connect("item-activated", item_clicked)
menuitem.set_submenu(recentchoosermenu)

window.show_all()

Gtk.main()
