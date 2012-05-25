#!/usr/bin/env python

from gi.repository import Gtk

def row_selected(treeview, treepath, treeviewcolumn):
    cellview.set_displayed_row(treepath)

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
window.add(vbox)

liststore = Gtk.ListStore(str, str)
liststore.append(["Zenwalk", "http://www.zenwalk.org"])
liststore.append(["Knoppix", "http://www.knoppix.com"])
liststore.append(["Frugalware", "http://frugalware.org"])

treeview = Gtk.TreeView(model=liststore)
treeview.connect("row-activated", row_selected)
vbox.pack_start(treeview, True, True, 0)

treeviewcolumn = Gtk.TreeViewColumn("Distribution")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
treeviewcolumn = Gtk.TreeViewColumn("Website")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 1)

cellview = Gtk.CellView()
cellview.set_model(liststore)
vbox.pack_start(cellview, True, True, 0)
cellrenderertext = Gtk.CellRendererText()
cellview.pack_start(cellrenderertext, False)
cellview.add_attribute(cellrenderertext, "text", 0)
cellrenderertext = Gtk.CellRendererText()
cellview.pack_start(cellrenderertext, False)
cellview.add_attribute(cellrenderertext, "text", 1)

window.show_all()

Gtk.main()
