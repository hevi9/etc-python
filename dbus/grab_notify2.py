# from https://gist.github.com/stesie/6561696
# NO WORK, don't get method_call

#import gobject
from gi.repository import Gtk
import dbus
from dbus.mainloop.glib import DBusGMainLoop
 
def msg_filter(_bus, msg):
  print(msg)
  if msg.get_member() != "Notify":
    return
  args = msg.get_args_list()
  print("%s:%s" % (args[3], args[4]))
 
if __name__ == '__main__':
  DBusGMainLoop(set_as_default = True)
  bus = dbus.SessionBus()
  bus.add_match_string("type='method_call',interface='org.freedesktop.Notifications'")
  bus.add_message_filter(msg_filter)
  #gobject.MainLoop().run()
  Gtk.main()