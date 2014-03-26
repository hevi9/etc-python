# NO WORK, don't get method_call
# from http://askubuntu.com/questions/38733/how-to-read-dbus-monitor-output

#import gtk
from gi.repository import Gtk as gtk
import dbus
from dbus.mainloop.glib import DBusGMainLoop

def filter_cb(bus, message):
    # the NameAcquired message comes through before match string gets applied
    if message.get_member() != "Notify":
        return
    args = message.get_args_list()
    # args are
    # (app_name, notification_id, icon, summary, body, actions, hints, timeout)
    print("Notification from app '%s'" % args[0])
    print("Summary: %s" % args[3])
    print("Body: %s", args[4])


DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
bus.add_match_string(
    "type='method_call',interface='org.freedesktop.Notifications',member='Notify'")
bus.add_message_filter(filter_cb)
gtk.main()