#!/usr/bin/env python

from gi.repository import Gtk

aboutdialog = Gtk.AboutDialog()
aboutdialog.set_name("PyGObject Tutorial")
aboutdialog.set_version("1.0")
aboutdialog.set_website("http://learnpygtk.org/")

aboutdialog.run()
aboutdialog.destroy()
