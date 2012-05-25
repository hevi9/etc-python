#!/usr/bin/env python

from gi.repository import Gtk

def response_received(infobar, response):
    if response == Gtk.ResponseType.OK:
        infobar.hide()

def message_type(button, message):
    infobar.set_message_type(message)
    infobar.show_all()

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
window.add(vbox)

infobar = Gtk.InfoBar()
infobar.add_button("Hide", Gtk.ResponseType.OK)
infobar.connect("response", response_received)
vbox.add(infobar)

hbox = Gtk.HBox(homogeneous=True, spacing=5)
vbox.pack_end(hbox, False, False, 0)

label = Gtk.Label(label="InfoBar Example")
content = infobar.get_content_area()
content.add(label)

buttonInfo = Gtk.Button(label="_Information", use_underline=True)
buttonInfo.connect("clicked", message_type, Gtk.MessageType.INFO)
hbox.pack_start(buttonInfo, True, True, 0)
buttonWarning = Gtk.Button(label="_Warning", use_underline=True)
buttonWarning.connect("clicked", message_type, Gtk.MessageType.WARNING)
hbox.pack_start(buttonWarning, True, True, 0)
buttonQuestion = Gtk.Button(label="_Question", use_underline=True)
buttonQuestion.connect("clicked", message_type, Gtk.MessageType.QUESTION)
hbox.pack_start(buttonQuestion, True, True, 0)
buttonError = Gtk.Button(label="_Error", use_underline=True)
buttonError.connect("clicked", message_type, Gtk.MessageType.ERROR)
hbox.pack_start(buttonError, True, True, 0)

window.show_all()

Gtk.main()
