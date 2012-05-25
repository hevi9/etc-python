#!/usr/bin/env python

from gi.repository import Gtk

def textview_editable(checkbutton):
    textview.set_editable(checkbuttonEditable.get_active())

def textview_cursor(checkbutton):
    textview.set_cursor_visible(checkbuttonCursor.get_active())

def textview_wrap(radiobutton, wrap_type):
    textview.set_wrap_mode(wrap_type)

def textview_justification(radiobutton, justify_type):
    textview.set_justification(justify_type)

window = Gtk.Window()
window.set_default_size(-1, 350)
window.connect("destroy", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
window.add(vbox)

scrolledwindow = Gtk.ScrolledWindow()
scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
vbox.pack_start(scrolledwindow, True, True, 0)

textbuffer = Gtk.TextBuffer()
textview = Gtk.TextView(buffer=textbuffer)
scrolledwindow.add(textview)

hbox = Gtk.HBox(homogeneous=False, spacing=5)
vbox.pack_start(hbox, False, False, 0)

table = Gtk.Table(n_rows=4, n_columns=4, homogeneous=False)
hbox.pack_start(table, False, False, 0)

checkbuttonEditable = Gtk.CheckButton(label="Editable")
checkbuttonEditable.set_active(True)
checkbuttonEditable.connect("toggled", textview_editable)
table.attach(checkbuttonEditable, 0, 1, 0, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND, 0, 0)
checkbuttonCursor = Gtk.CheckButton(label="Cursor Visible")
checkbuttonCursor.set_active(True)
checkbuttonCursor.connect("toggled", textview_cursor)
table.attach(checkbuttonCursor, 0, 1, 1, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND, 0, 0)

radiobuttonNoWrap = Gtk.RadioButton(group=None, label="No Wrapping")
radiobuttonNoWrap.connect("toggled", textview_wrap, Gtk.WrapMode.NONE)
table.attach(radiobuttonNoWrap, 1, 2, 0, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND, 0, 0)
radiobuttonCharWrap = Gtk.RadioButton(group=radiobuttonNoWrap, label="Character Wrapping")
radiobuttonCharWrap.connect("toggled", textview_wrap, Gtk.WrapMode.CHAR)
table.attach(radiobuttonCharWrap, 1, 2, 1, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND, 0, 0)
radiobuttonWordWrap = Gtk.RadioButton(group=radiobuttonNoWrap, label="Word Wrapping")
radiobuttonWordWrap.connect("toggled", textview_wrap, Gtk.WrapMode.WORD)
table.attach(radiobuttonWordWrap, 1, 2, 2, 3, Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND, 0, 0)

radiobuttonJustifyLeft = Gtk.RadioButton(group=None, label="Justify Left")
radiobuttonJustifyLeft.connect("toggled", textview_justification, Gtk.Justification.LEFT)
table.attach(radiobuttonJustifyLeft, 2, 3, 0, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND, 0, 0)
radiobuttonJustifyCenter = Gtk.RadioButton(group=radiobuttonJustifyLeft, label="Justify Center")
radiobuttonJustifyCenter.connect("toggled", textview_justification, Gtk.Justification.CENTER)
table.attach(radiobuttonJustifyCenter, 2, 3, 1, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND, 0, 0)
radiobuttonJustifyRight = Gtk.RadioButton(group=radiobuttonJustifyLeft, label="Justify Right")
radiobuttonJustifyRight.connect("toggled", textview_justification, Gtk.Justification.RIGHT)
table.attach(radiobuttonJustifyRight, 2, 3, 2, 3, Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND, 0, 0)
radiobuttonJustifyFill = Gtk.RadioButton(group=radiobuttonJustifyLeft, label="Justify Fill")
radiobuttonJustifyFill.connect("toggled", textview_justification, Gtk.Justification.FILL)
table.attach(radiobuttonJustifyFill, 2, 3, 3, 4, Gtk.AttachOptions.FILL, Gtk.AttachOptions.EXPAND, 0, 0)

window.show_all()

Gtk.main()
