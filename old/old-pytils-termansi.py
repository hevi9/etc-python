#!/usr/bin/env python
## $Id: termansi.py,v 1.2 2003-07-16 17:58:16 hevi Exp $
## MODULE

"""

"""
__version__ = "$Revision: 1.2 $"
__todo__ = """
"""

#from __future__ import generators

######################################################################
## dependencies

#import sys
#import os

import os
import sys
try:
    import termios
except ImportError:
    import TERMIOS
    termios = TERMIOS
import string

######################################################################
## hevi-term-show-ansi-colors

"""
#!/bin/bash
  # Display ANSI colours.
  #
  esc="\033["
  echo -n " _ _ _ _ _40 _ _ _ 41_ _ _ _42 _ _ _ 43"
  echo "_ _ _ 44_ _ _ _45 _ _ _ 46_ _ _ _47 _"
  for fore in 30 31 32 33 34 35 36 37; do
    line1="$fore  "
    line2="    "
    for back in 40 41 42 43 44 45 46 47; do
      line1="${line1}${esc}${back};${fore}m Normal  ${esc}0m"
      line2="${line2}${esc}${back};${fore};1m Bold    ${esc}0m"
    done
    echo -e "$line1\n$line2"
  done
"""

######################################################################
## termansi

enable_color = 1

## - clearing does not work well
def color(text, fg, bg=None):
    """Return colored text.

    Uses terminal color codes; set avk_util.enable_color to 0 to
    return plain un-colored text. If fg is a tuple, it's assumed to
    be (fg, bg).

    quated this from somewhere
    """

    if type(fg) == tuple:
        fg, bg = fg
    xterm = 0
    if os.environ["TERM"] == "xterm": 
        xterm = 1
    if enable_color:
        col_dict = {
            "black"     :   "30m",
            "red"       :   "31m",
            "green"     :   "32m",
            "brown"     :   "33m",
            "blue"      :   "34m",
            "purple"    :   "35m",
            "cyan"      :   "36m",
            "lgray"     :   "37m",
            "gray"      :   "1;30m",
            "lred"      :   "1;31m",
            "lgreen"    :   "1;32m",
            "yellow"    :   "1;33m",
            "lblue"     :   "1;34m",
            "pink"      :   "1;35m",
            "lcyan"     :   "1;36m",
            "white"     :   "1;37m",
        }
        b = "0m"
        s = "\033["
        clear = "0m"
        # In xterm, brown comes out as yellow..
        if xterm and fg == "yellow": fg = "brown"
        f = col_dict[fg]
        if bg:
            if bg == "yellow" and xterm: 
                bg = "brown"
            try: 
                b = col_dict[bg].replace('3', '4', 1)
            except KeyError: 
                pass
        return "%s%s%s%s%s%s%s" % (s, b, s, f, text, s, clear)
    else:
        return text

#def beep():
#    """Beep terminal bell one time."""
#    print '\a'


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

