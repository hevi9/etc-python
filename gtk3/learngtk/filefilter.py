#!/usr/bin/env python

from gi.repository import Gtk

filechooserdialog = Gtk.FileChooserDialog("Select a File", None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

filefilter = Gtk.FileFilter()
filefilter.set_name("All Files")
filefilter.add_pattern("*")
filechooserdialog.add_filter(filefilter)

filefilter = Gtk.FileFilter()
filefilter.set_name("Images")
filefilter.add_pattern("*.png")
filefilter.add_pattern("*.jpg")
filefilter.add_pattern("*.bmp")
filechooserdialog.add_filter(filefilter)

filefilter = Gtk.FileFilter()
filefilter.set_name("Sounds")
filefilter.add_pattern("*.ogg")
filefilter.add_pattern("*.flac")
filechooserdialog.add_filter(filefilter)

filechooserdialog.run()
filechooserdialog.destroy()
