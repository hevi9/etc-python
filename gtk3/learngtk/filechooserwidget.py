#!/usr/bin/env python

from gi.repository import Gtk

def file_selected(filechooser):
    filename = str(filechooser.get_filename())
    label2.set_text(filename)

window = Gtk.Window()
window.set_border_width(5)
window.set_default_size(600, 400)
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
window.add(vbox)

filechooserwidget = Gtk.FileChooserWidget()
filechooserwidget.connect("selection-changed", file_selected)
vbox.pack_start(filechooserwidget, True, True, 0)

hbox = Gtk.HBox(homogeneous=False, spacing=5)
vbox.pack_start(hbox, False, False, 0)

label1 = Gtk.Label(label="Selected file:")
hbox.pack_start(label1, False, False, 0)
label2 = Gtk.Label()
label2.set_use_markup(True)
hbox.pack_start(label2, False, False, 0)

window.show_all()

Gtk.main()
