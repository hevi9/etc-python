#!/usr/bin/env python3

# from http://cheesehead-techblog.blogspot.fi/2012/11/dbus-tutorial-gobject-introspection.html

import gi.repository
from gi.repository import Gio, GLib

# Create the DBus message
destination = 'org.freedesktop.NetworkManager'
path        = '/org/freedesktop/NetworkManager/ActiveConnection/19'
interface   = 'org.freedesktop.DBus.Properties'
method      = 'GetAll'
args        = GLib.Variant('(ss)', 
              ('org.freedesktop.NetworkManager.Connection.Active', 'None'))
answer_fmt  = GLib.VariantType.new ('(v)')
proxy_prpty = Gio.DBusCallFlags.NONE
timeout     = -1
cancellable = None

# Connect to DBus, send the DBus message, and receive the reply
bus   = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
reply = bus.call_sync(destination, path, interface,
                      method, args, answer_fmt,
                      proxy_prpty, timeout, cancellable)

# Convert the result value to a useful python object and print
[print(item[0], item[1]) for item in result.unpack()[0].items()]