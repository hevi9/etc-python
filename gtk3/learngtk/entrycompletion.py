#!/usr/bin/env python

from gi.repository import Gtk

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

liststore = Gtk.ListStore(str)
for item in ["Debian", "Sabayon", "Arch Linux", "Fedora", "OpenSuSE", "Slackware", "Mandriva", "MEPIS"]:
    liststore.append([item])

entrycompletion = Gtk.EntryCompletion()
entrycompletion.set_model(liststore)
entrycompletion.set_text_column(0)

entry = Gtk.Entry()
entry.set_completion(entrycompletion)
window.add(entry)

window.show_all()

Gtk.main()
