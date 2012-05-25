#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, -1)
window.connect("destroy", lambda q: Gtk.main_quit())

handlebox = Gtk.HandleBox()
window.add(handlebox)

toolbar = Gtk.Toolbar()
toolbar.set_size_request(200, -1)
handlebox.add(toolbar)

toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_ADD)
toolbar.add(toolbutton)
toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_EDIT)
toolbar.add(toolbutton)
toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_REMOVE)
toolbar.add(toolbutton)

window.show_all()

Gtk.main()
