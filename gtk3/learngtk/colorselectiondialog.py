#!/usr/bin/env python

from gi.repository import Gtk

colorselectiondialog = Gtk.ColorSelectionDialog(title="ColorSelectionDialog")
colorselection = colorselectiondialog.get_color_selection()

response = colorselectiondialog.run()

if response == Gtk.ResponseType.OK:
    color = colorselection.get_current_color()
    print("Colour selected: %s" % color)

colorselectiondialog.destroy()
