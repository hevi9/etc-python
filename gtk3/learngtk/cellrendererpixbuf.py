#!/usr/bin/env python

from gi.repository import Gtk, GdkPixbuf

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

liststore = Gtk.ListStore(str, str)
liststore.append(["New", Gtk.STOCK_NEW])
liststore.append(["Open", Gtk.STOCK_OPEN])
liststore.append(["Save", Gtk.STOCK_SAVE])

treeview = Gtk.TreeView(model=liststore)
window.add(treeview)

treeviewcolumn = Gtk.TreeViewColumn("Text")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

treeviewcolumn = Gtk.TreeViewColumn("Image")
treeview.append_column(treeviewcolumn)
cellrendererpixbuf = Gtk.CellRendererPixbuf()
treeviewcolumn.pack_start(cellrendererpixbuf, False)
treeviewcolumn.add_attribute(cellrendererpixbuf, "stock-id", 1)

window.show_all()

Gtk.main()
