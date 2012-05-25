#!/usr/bin/env python

from gi.repository import Gtk

fontselectiondialog = Gtk.FontSelectionDialog(title="FontSelectionDialog")
response = fontselectiondialog.run()

if response == Gtk.ResponseType.OK:
    print(fontselectiondialog.get_font_name())

fontselectiondialog.destroy()
