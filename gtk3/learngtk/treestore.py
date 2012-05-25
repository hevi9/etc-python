#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(225, 250)
window.connect("destroy", lambda q: Gtk.main_quit())

treestore = Gtk.TreeStore(str)
item = treestore.append(None, ["Debian"])
treestore.append(item, ["http://www.debian.org/"])
item = treestore.append(None, ["Sabayon"])
treestore.append(item, ["http://www.sabayonlinux.org/"])
item = treestore.append(None, ["Fedora"])
treestore.append(item, ["http://fedoraproject.org/"])
item = treestore.append(None, ["Xubuntu"])
treestore.append(item, ["http://www.xubuntu.org/"])
item = treestore.append(None, ["Gentoo"])
treestore.append(item, ["http://www.gentoo.org/"])

treeview = Gtk.TreeView(model=treestore)
window.add(treeview)

treeviewcolumn = Gtk.TreeViewColumn("Distribution")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

window.show_all()

Gtk.main()
