#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=True, spacing=5)
window.add(vbox)

entrybuffer = Gtk.EntryBuffer(text="Entry with EntryBuffer")

entry1 = Gtk.Entry()
entry1.set_buffer(entrybuffer)
vbox.pack_start(entry1, False, False, 0)
entry2 = Gtk.Entry()
entry2.set_buffer(entrybuffer)
vbox.pack_start(entry2, False, False, 0)
entry3 = Gtk.Entry()
entry3.set_buffer(entrybuffer)
vbox.pack_start(entry3, False, False, 0)

window.show_all()

Gtk.main()
