#!/usr/bin/env python

from gi.repository import Gtk

recentchooserdialog = Gtk.RecentChooserDialog(title="RecentChooserDialog", parent=None, buttons=(Gtk.STOCK_OPEN, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
response = recentchooserdialog.run()

if response == Gtk.ResponseType.OK:
    print(recentchooserdialog.get_current_uri())

recentchooserdialog.destroy()
