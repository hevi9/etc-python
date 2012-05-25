#!/usr/bin/env python

from gi.repository import Gtk

def right_button_click(icon, button, time):
    menu = Gtk.Menu()
    
    menuitemAbout = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ABOUT, None)
    menu.append(menuitemAbout)
    menuitemQuit = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT, None)
    menuitemQuit.connect("activate", lambda q: Gtk.main_quit())
    menu.append(menuitemQuit)
    menu.show_all()

    def func(a, b):
        print(a)
        print(b)
    
    menu.popup(None, None, Gtk.StatusIcon.position_menu, button, time)

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

statusicon = Gtk.StatusIcon()
statusicon.set_from_stock(Gtk.STOCK_HOME)
statusicon.connect("popup-menu", right_button_click)

window.show_all()

Gtk.main()
