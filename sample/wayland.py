""" pyilds for wayland """

from hevi_proto.pyild import *

import sys
import os
env = os.environ
j = os.path.join

srcrepo = "/home/src"

prefix = "/opt/wayland"
env["LD_LIBRARY_PATH"] = j(prefix,"lib")
env["PKG_CONFIG_PATH"] = j(prefix,"lib/pkgconfig/") + ":" + j(prefix,"/share/pkgconfig/") 
env["ACLOCAL"] = "aclocal -I $WLD/share/aclocal"

b("wayland","""
git clone git://anongit.freedesktop.org/wayland/wayland
cd wayland
./autogen.sh --prefix=$WLD
make
make install
""")