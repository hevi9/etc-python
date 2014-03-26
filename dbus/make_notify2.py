# from http://www.piware.de/2011/01/na-zdravi-pygi/

from gi.repository import Gio, GLib

d = Gio.bus_get_sync(Gio.BusType.SESSION, None)
notify = Gio.DBusProxy.new_sync(d, 0, None, 'org.freedesktop.Notifications',
    '/org/freedesktop/Notifications', 'org.freedesktop.Notifications', None)

result = notify.Notify('(susssasa{sv}i)', 'test', 1, 'gtk-ok', 'Hello World!',
            'Subtext', [], {}, 10000)
print(result)

