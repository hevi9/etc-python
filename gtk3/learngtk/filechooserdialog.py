#!/usr/bin/env python

from gi.repository import Gtk

filechooserdialog = Gtk.FileChooserDialog(title="FileChooserDialog", parent=None, buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

response = filechooserdialog.run()

if response == Gtk.ResponseType.OK:
    print("Selected file: %s" % filechooserdialog.get_filename())

filechooserdialog.destroy()
