#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

frame = Gtk.Frame()
frame.set_shadow_type(Gtk.ShadowType.NONE)
window.add(frame)

label = Gtk.Label(label="<b>Common Frame</b>")
label.set_use_markup(True)
frame.set_label_widget(label)

alignment = Gtk.Alignment()
alignment.set_padding(5, 0, 12, 0)
alignment.set(0.5, 0.5, 1.0, 1.0)
frame.add(alignment)
        
label = Gtk.Label(label="Label inside Common Frame")
alignment.add(label)

window.show_all()

Gtk.main()
