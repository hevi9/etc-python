#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, -1)
window.connect("destroy", lambda w: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
window.add(vbox)
        
sizegroup = Gtk.SizeGroup(mode=Gtk.SizeGroupMode.BOTH)
       
button = Gtk.Button(label="Button 1")
sizegroup.add_widget(button)
vbox.pack_start(button, False, False, 0)
button = Gtk.Button(label="Button 2")
sizegroup.add_widget(button)
vbox.pack_start(button, False, False, 0)
button = Gtk.Button(label="Button 3")
sizegroup.add_widget(button)
vbox.pack_start(button, False, False, 0)
      
window.show_all()

Gtk.main()
