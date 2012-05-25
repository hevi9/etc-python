#!/usr/bin/env python

from gi.repository import Gtk

def cell_edited(cellrenderertext, treepath, text):
    treepath = int(treepath)
    liststore[treepath][1] = text

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

liststore = Gtk.ListStore(str, str)
liststore.append(["Debian", "http://www.debian.org/"])
liststore.append(["Sabayon", "http://www.sabayonlinux.org/"])
liststore.append(["Fedora", "http://fedoraproject.org/"])

treeview = Gtk.TreeView(model=liststore)
window.add(treeview)

treeviewcolumn = Gtk.TreeViewColumn("Distribution")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

treeviewcolumn = Gtk.TreeViewColumn("Website")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
cellrenderertext.set_property("editable", True)
cellrenderertext.connect("edited", cell_edited)
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 1)

window.show_all()

Gtk.main()
