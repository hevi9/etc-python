#!/usr/bin/env python

from gi.repository import Gtk

dialog = Gtk.Dialog(title="Dialog", parent=None, flags=0, buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
dialog.set_default_size(250, 300)

response = dialog.run()

if response == Gtk.ResponseType.OK:
    print("OK button pressed")
elif response == Gtk.ResponseType.CANCEL:
    print("Cancel button pressed")

dialog.destroy()
