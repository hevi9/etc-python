# works,needs eavesdrop='true'

from gi.repository import Gtk
import dbus
from dbus.mainloop.glib import DBusGMainLoop
 
def msg_filter(_bus, msg):
  if msg.get_member() != "Notify":
    return
  args = msg.get_args_list()
  print("%s:%s" % (args[3], args[4]))
 
if __name__ == '__main__':
  DBusGMainLoop(set_as_default = True)
  bus = dbus.SessionBus()
  bus.add_match_string("interface='org.freedesktop.Notifications',eavesdrop='true'")
  bus.add_message_filter(msg_filter)
  Gtk.main()