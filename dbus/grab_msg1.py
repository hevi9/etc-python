# works, needs eavesdrop='true' after dbus 1.6
# info from http://lists.freedesktop.org/pipermail/dbus/2013-April/015576.html

from gi.repository import Gtk
import dbus
from dbus.mainloop.glib import DBusGMainLoop
 
def msg_filter(_bus, msg):
  print(msg)
 
if __name__ == '__main__':
  DBusGMainLoop(set_as_default = True)
  bus = dbus.SessionBus()
  bus.add_match_string("type='method_call',eavesdrop='true'")
  bus.add_message_filter(msg_filter)
  Gtk.main()