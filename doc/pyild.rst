pyild - python build system (proto)
***********************************

Goal is to collect software building scripts into
central manageable place.

Sample
======

start
::
  b("""
  git clone git://anongit.freedesktop.org/wayland/wayland
  cd wayland
  ./autogen.sh --prefix=$WLD
  make
  make install
  """)
