#!/usr/bin/env python

from gi.repository import Gtk

distributions = ["Fedora", "Sabayon", "Debian", "Arch Linux", "Crunchbang"]

def change_selected(combobox):
    print("ComboBox item was changed to %s" % combobox.get_active_text())

window = Gtk.Window()
window.set_default_size(200, -1)
window.connect("destroy", lambda q: Gtk.main_quit())

liststore = Gtk.ListStore(str)
for item in distributions:
    liststore.append([item])

combobox = Gtk.ComboBox(model=liststore)
combobox.set_active(0)
combobox.connect("changed", change_selected)
window.add(combobox)

cell = Gtk.CellRendererText()
combobox.pack_start(cell, True)
combobox.add_attribute(cell, "text", 0)

window.show_all()

Gtk.main()
