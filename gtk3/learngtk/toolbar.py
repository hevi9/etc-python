#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, -1)
window.connect("destroy", lambda q: Gtk.main_quit())

toolbar = Gtk.Toolbar()
window.add(toolbar)

toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_NEW)
toolbar.add(toolbutton)
toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_OPEN)
toolbar.add(toolbutton)
toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_SAVE)
toolbar.add(toolbutton)

window.show_all()

Gtk.main()
