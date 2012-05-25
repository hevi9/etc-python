#!/usr/bin/env python

from gi.repository import Gtk

def cell_edited(cell, path):
    selection = treeview.get_selection()
    boolean, model, treeiter = selection.get_selected()
    
    if cell.get_active():    
        liststore.set_value(treeiter, 1, False)
    else:
        liststore.set_value(treeiter, 1, True)
    
window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

liststore = Gtk.ListStore(str, bool)
liststore.append(["GParted", True])
liststore.append(["OpenSuSE", False])
liststore.append(["Debian", False])

treeview = Gtk.TreeView(model=liststore)
window.add(treeview)

treeviewcolumn = Gtk.TreeViewColumn("Distribution")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

treeviewcolumn = Gtk.TreeViewColumn("Active")
treeview.append_column(treeviewcolumn)
cellrenderertoggle = Gtk.CellRendererToggle()
cellrenderertoggle.connect("toggled", cell_edited)
treeviewcolumn.pack_start(cellrenderertoggle, True)
treeviewcolumn.add_attribute(cellrenderertoggle, "active", 1)

window.show_all()

Gtk.main()
