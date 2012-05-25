#!/usr/bin/env python

from gi.repository import Gtk

def button_clicked(button, message_type, message_text):
    messagedialog = Gtk.MessageDialog(parent=window, flags=0, title="Message Dialog")
    messagedialog.set_property("message-type", message_type)
    messagedialog.set_markup(message_text)
    messagedialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)

    messagedialog.run()
    messagedialog.destroy()

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

hbox = Gtk.HBox(homogeneous=True, spacing=5)
window.add(hbox)

button = Gtk.Button(label="Information")
button.connect("clicked", button_clicked, Gtk.MessageType.INFO, "This is an information message dialog")
hbox.add(button)
button = Gtk.Button(label="Warning")
button.connect("clicked", button_clicked, Gtk.MessageType.WARNING, "This is a warning message dialog")
hbox.add(button)
button = Gtk.Button(label="Question")
button.connect("clicked", button_clicked, Gtk.MessageType.QUESTION, "This is a question message dialog")
hbox.add(button)
button = Gtk.Button(label="Error")
button.connect("clicked", button_clicked, Gtk.MessageType.ERROR, "This is an error message dialog")
hbox.add(button)

window.show_all()

Gtk.main()
