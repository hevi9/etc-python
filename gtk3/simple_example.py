#!/usr/bin/python3
## http://readthedocs.org/docs/python-gtk-3-tutorial/en/latest/introduction.html

from gi.repository import Gtk

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
