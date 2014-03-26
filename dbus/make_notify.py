#!/usr/bin/python3

# from https://wiki.archlinux.org/index.php/Desktop_notifications#Python

from gi.repository import Notify
Notify.init ("Hello world")
Hello=Notify.Notification.new ("Hello world","This is an example notification.","dialog-information")
Hello.show ()