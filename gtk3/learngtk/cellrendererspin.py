#!/usr/bin/env python

from gi.repository import Gtk

def value_changed(cellrendererspin, path, value):
    liststore[int(path)][1] = int(value)

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

liststore = Gtk.ListStore(str, int)
liststore.append(["Orange", 3])
liststore.append(["Apple", 6])
liststore.append(["Banana", 4])

adjustment = Gtk.Adjustment(0, 0, 10, 1, 2, 0)

treeview = Gtk.TreeView(model=liststore)
window.add(treeview)

treeviewcolumn = Gtk.TreeViewColumn("Fruit")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

treeviewcolumn = Gtk.TreeViewColumn("Quantity")
treeview.append_column(treeviewcolumn)
cellrendererspin = Gtk.CellRendererSpin()
cellrendererspin.set_property("adjustment", adjustment)
cellrendererspin.set_property("editable", True)
cellrendererspin.connect("edited", value_changed)
treeviewcolumn.pack_start(cellrendererspin, False)
treeviewcolumn.add_attribute(cellrendererspin, "text", 1)

window.show_all()

Gtk.main()
