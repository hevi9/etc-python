#!/usr/bin/env python

from gi.repository import Gtk

assistant = Gtk.Assistant()
assistant.connect("apply", lambda q: Gtk.main_quit())
assistant.connect("cancel", lambda q: Gtk.main_quit())

vbox = Gtk.VBox(homogeneous=False, spacing=5)
vbox.set_border_width(5)
page = assistant.append_page(vbox)
assistant.set_page_title(vbox, "Page 1: Starting Out")
assistant.set_page_type(vbox, Gtk.AssistantPageType.INTRO)
label = Gtk.Label(label="This is an example label within an Assistant widget. The Assistant is used to guide the user through the configuration of an application.")
label.set_line_wrap(True)
vbox.pack_start(label, True, True, 0)
assistant.set_page_complete(vbox, True)

vbox = Gtk.VBox(homogeneous=False, spacing=5)
vbox.set_border_width(5)
page = assistant.append_page(vbox)
assistant.set_page_title(vbox, "Page 2: Moving On...")
assistant.set_page_type(vbox, Gtk.AssistantPageType.CONTENT)
label = Gtk.Label(label="This is an example of a label and button within a page. This is a content page primarily used to display options to the end user.")
label.set_line_wrap(True)
vbox.pack_start(label, True, True, 0)
assistant.set_page_complete(vbox, True)

vbox = Gtk.VBox(homogeneous=False, spacing=5)
vbox.set_border_width(5)
page = assistant.append_page(vbox)
assistant.set_page_title(vbox, "Page 3: The Finale")
assistant.set_page_type(vbox, Gtk.AssistantPageType.CONFIRM)
label = Gtk.Label(label="This is the inal page of the Assistant Widget. It would be used to confirm the preferences we have set in the previous pages.")
label.set_line_wrap(True)
vbox.pack_start(label, True, True, 0)
assistant.set_page_complete(vbox, True)

assistant.show_all()

Gtk.main()
