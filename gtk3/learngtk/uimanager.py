#!/usr/bin/env python

from gi.repository import Gtk

interface = """
<ui>
    <menubar name="MenuBar">
        <menu action="File">
            <menuitem action="New"/>
            <menuitem action="Open"/>
            <menuitem action="Save"/>
            <menuitem action="Quit"/>
        </menu>
        <menu action="Edit">
            <menuitem action="Preferences"/>
        </menu>
        <menu action="Help">
            <menuitem action="About"/>
        </menu>
    </menubar>
</ui>
"""

window = Gtk.Window()
window.set_default_size(200, 200)
window.connect("destroy", lambda q: Gtk.main_quit())

uimanager = Gtk.UIManager()
accelgroup = uimanager.get_accel_group()
window.add_accel_group(accelgroup)

actiongroup = Gtk.ActionGroup("uimanager")
actiongroup.add_action([
                       ("New", Gtk.STOCK_NEW, "_New", None, "Create a New Document"),
                       ("Open", Gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document"),
                       ("Save", Gtk.STOCK_SAVE, "_Save", None, "Save the Current Document"),
                       ("Quit", Gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", lambda w: Gtk.main_quit()),
                       ("File", None, "_File"), 
                       ("Preferences", Gtk.STOCK_PREFERENCES, "_Preferences", None, "Edit the Preferences"),
                       ("Edit", "None", "_Edit"),
                       ("About", Gtk.STOCK_ABOUT, "_About", None, "Open the About dialog"),
                       ("Help", "None", "_Help")
                       ])

uimanager.insert_action_group(actiongroup, 0)
uimanager.add_ui_from_string(interface)
        
menubar = uimanager.get_widget("/MenuBar")

vbox = Gtk.VBox(homogeneous=False, spacing=0)
vbox.pack_start(menubar, False, False, 0)

window.show_all()

Gtk.main()
