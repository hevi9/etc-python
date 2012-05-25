#!/usr/bin/env python

from gi.repository import Gtk, GObject

def pulse_spinner():    
    for item in liststore:
        count = item[2]
        count = count + 1
        item[2] = count
    
    return True

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

liststore = Gtk.ListStore(str, bool, int)
liststore.append(["OpenSuSE", True, 1])
liststore.append(["Aptosid", False, 0])
liststore.append(["Crunchbang", True, 3])

treeview = Gtk.TreeView(model=liststore)
window.add(treeview)

treeviewcolumn = Gtk.TreeViewColumn("Distribution")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

treeviewcolumn = Gtk.TreeViewColumn("Active")
treeview.append_column(treeviewcolumn)
cellrendererspinner = Gtk.CellRendererSpinner()
treeviewcolumn.pack_start(cellrendererspinner, False)
treeviewcolumn.add_attribute(cellrendererspinner, "active", 1)
treeviewcolumn.add_attribute(cellrendererspinner, "pulse", 2)

window.show_all()

GObject.timeout_add(100, pulse_spinner)

Gtk.main()
