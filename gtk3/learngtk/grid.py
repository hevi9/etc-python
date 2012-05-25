#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

grid = Gtk.Grid()
window.add(grid)

button1 = Gtk.Button("Button\nThis button text has been set to use a single line")
grid.attach(button1, 0, 0, 1, 1)

label1 = Gtk.Label("Label\nThis label text\nhas been separated onto\nmultiple lines")
grid.attach_next_to(label1, button1, Gtk.PositionType.RIGHT, 1, 1)

button2 = Gtk.Button("Button\nThis button text\nhas been set to use\nmultiple lines")
grid.attach_next_to(button2, label1, Gtk.PositionType.BOTTOM, 1, 1)

label2 = Gtk.Label("Label\nThis label text\nhas also been separated\nonto multiple lines")
grid.attach_next_to(label2, label1, Gtk.PositionType.RIGHT, 1, 2)

label3 = Gtk.Label("Label\nThis label contains a very long string\nof text which shows off the Grid widgets ability\n to scale the item in relation to the space it should use\n and the size of the widgets around it.\nThis creates a natural, clean look.")
grid.attach_next_to(label3, button1, Gtk.PositionType.BOTTOM, 1, 1)

window.show_all()

Gtk.main()
