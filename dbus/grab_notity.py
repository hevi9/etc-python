# NO WORK, don't get method_call

# from http://askubuntu.com/questions/89279/listening-to-incoming-libnotify-notifications-using-dbus
# from http://cheesehead-techblog.blogspot.fi/2012/10/dbus-tutorial-create-service.html

# import glib # ImportError: No module named 'glib'

from gi.repository import Gtk
import dbus
from dbus.mainloop.glib import DBusGMainLoop

def notifications(bus, message):
  print(message)
  if message.get_member() == "Notify":
    print([arg for arg in message.get_args_list()])

DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("interface='org.freedesktop.Notifications'")
#bus.add_match_string_non_blocking("type='method_call',interface='org.freedesktop.Notifications'")
bus.add_message_filter(notifications)


print("looping ..")
Gtk.main()