#!/usr/bin/env python3

# from http://cheesehead-techblog.blogspot.fi/2012/11/dbus-tutorial-gobject-introspection.html

import gi.repository
from gi.repository import Gio, GLib

# Create the DBus message
destination = 'org.freedesktop.NetworkManager'
path        = '/org/freedesktop/NetworkManager'
interface   = 'org.freedesktop.DBus.Introspectable'
method      = 'Introspect'
args        = None
answer_fmt  = GLib.VariantType.new ('(s)')
proxy_prpty = Gio.DBusCallFlags.NONE
timeout     = -1
cancellable = None

# Connect to DBus, send the DBus message, and receive the reply
bus   = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
reply = bus.call_sync(destination, path, interface,
                      method, args, answer_fmt,
                      proxy_prpty, timeout, cancellable)

# Convert the result value to a formatted python element
print(reply.unpack()[0])

