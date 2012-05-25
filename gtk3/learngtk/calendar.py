#!/usr/bin/env python

from gi.repository import Gtk

def showheading_toggled(checkbutton):
    calendar.set_property("show-heading", checkbutton.get_active())

def weeknumbers_toggled(checkbutton):
    calendar.set_property("show-week-numbers", checkbutton.get_active())

def daynames_toggled(checkbutton):
    calendar.set_property("show-day-names", checkbutton.get_active())

def datechange_toggled(checkbutton):
    calendar.set_property("no-month-change", checkbutton.get_active())

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())

hbox = Gtk.HBox(homogeneous=False, spacing=5)
window.add(hbox)

calendar = Gtk.Calendar()
hbox.pack_start(calendar, False, False, 0)

vbox = Gtk.VBox(homogeneous=False, spacing=5)
hbox.pack_start(vbox, False, False, 0)

checkbutton_showheading = Gtk.CheckButton(label="Show Heading")
checkbutton_showheading.set_active(True)
checkbutton_showheading.connect("toggled", showheading_toggled)
vbox.pack_start(checkbutton_showheading, False, False, 0)
checkbutton_weeknumbers = Gtk.CheckButton(label="Show Week Numbers")
checkbutton_weeknumbers.connect("toggled", weeknumbers_toggled)
vbox.pack_start(checkbutton_weeknumbers, False, False, 0)
checkbutton_daynames = Gtk.CheckButton(label="Show Day Names")
checkbutton_daynames.set_active(True)
checkbutton_daynames.connect("toggled", daynames_toggled)
vbox.pack_start(checkbutton_daynames, False, False, 0)
checkbutton_datechange = Gtk.CheckButton(label="Prevent Month/Year Changes")
checkbutton_datechange.connect("toggled", datechange_toggled)
vbox.pack_start(checkbutton_datechange, False, False, 0)

window.show_all()

Gtk.main()
