#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

notebook = Gtk.Notebook()
window.add(notebook)

for page in range(1, 100):
    label = Gtk.Label(label="Page %s" % page)
    vbox = Gtk.VBox()
    notebook.append_page(vbox, label)

window.show_all()

Gtk.main()
