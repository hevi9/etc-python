#!/usr/bin/env python

from gi.repository import Gtk

appchooserdialog = Gtk.AppChooserDialog(parent=None, flags=0, content_type="audio/flac")
response = appchooserdialog.run()

if response == Gtk.ResponseType.OK:
    print("Application activated: %s" % appchooserdialog.get_app_info().get_name())

appchooserdialog.destroy()
