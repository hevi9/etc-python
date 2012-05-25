#!/usr/bin/env python

from gi.repository import Gtk, GdkPixbuf

icons = [Gtk.STOCK_HOME, Gtk.STOCK_ABOUT, Gtk.STOCK_NEW, Gtk.STOCK_OPEN, Gtk.STOCK_SAVE, Gtk.STOCK_PRINT]

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

liststore = Gtk.ListStore(GdkPixbuf.Pixbuf)

iconview = Gtk.IconView(model=liststore)
iconview.set_pixbuf_column(0)
window.add(iconview)

for icon in icons:
    pixbuf = iconview.render_icon(icon, Gtk.IconSize.DIALOG, None)
    liststore.append([pixbuf])

window.show_all()

Gtk.main()
