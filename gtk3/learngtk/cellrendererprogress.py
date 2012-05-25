#!/usr/bin/env python

from gi.repository import Gtk, GObject

def move_progressbar():
    for item in liststore:
        step = item[2]
        
        if item[1] == 100:
            item[1] = 0
        else:
        
            if item[1] + step > 100:
                value = 100 - item[1]
                item[1] += value
            else:
                item[1] += step
    
    return True

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

liststore = Gtk.ListStore(str, int, int)
liststore.append(["Debian", 68, 3])
liststore.append(["Fedora", 84, 1])
liststore.append(["Frugalware", 33, 4])

treeview = Gtk.TreeView(model=liststore)
window.add(treeview)

treeviewcolumn = Gtk.TreeViewColumn("Distribution")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, False)
treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

treeviewcolumn = Gtk.TreeViewColumn("Completion")
treeview.append_column(treeviewcolumn)
cellrendererprogress = Gtk.CellRendererProgress()
treeviewcolumn.pack_start(cellrendererprogress, True)
treeviewcolumn.add_attribute(cellrendererprogress, "value", 1)

window.show_all()

GObject.timeout_add(1000, move_progressbar)

Gtk.main()
