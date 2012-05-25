#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

toolpalette = Gtk.ToolPalette()
window.add(toolpalette)

toolitemgroup = Gtk.ToolItemGroup(label="Group 1")
toolpalette.add(toolitemgroup)

toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_ADD)
toolitemgroup.add(toolbutton)
toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_REMOVE)
toolitemgroup.add(toolbutton)

toolitemgroup = Gtk.ToolItemGroup(label="Group 2")
toolpalette.add(toolitemgroup)

toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_HOME)
toolitemgroup.add(toolbutton)
toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_ABOUT)
toolitemgroup.add(toolbutton)
toolbutton = Gtk.ToolButton(stock_id=Gtk.STOCK_PREFERENCES)
toolitemgroup.add(toolbutton)

window.show_all()

Gtk.main()
