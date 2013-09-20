"""Miscellaneous small utility functions.

    vol(vol=None) - get or set volume using aumix

    progress(ratio, length=40, col=1, cols=("yellow", None, "cyan"),
            nocol="=.")
        Text mode progress bar.

    yes(question, [default answer]) 
        i.e. if yes("erase file?", 'n'): erase_file()

    color(text, fg, [bg])
        colorize text using terminal color codes

    beep() - beep terminal bell once

    ftime(seconds) - returns h:m:s or m:s if there's no hours.

    Term() - terminal stuff
        term.size() => height, width
        term.clear() => clear terminal
        term.getch() => get one char at a time

 Copyright (C) 2002 Andrei Kulakov <ak@silmarill.org>
 Licence: GPL [see http://www.gnu.org/copyleft/gpl.html]
 """

import os
import sys
try:
    import termios
except ImportError:
    import TERMIOS
    termios = TERMIOS
import commands
import string
from types import *





def progress(ratio, length=40, col=1, cols=("yellow", None, "cyan"),
            nocol="=."):
    """Text mode progress bar.

    ratio   - current position / total (e.g. 0.6 is 60%)
    length  - bar size
    col     - color bar
    cols    - tuple: (elapsed, left, percentage num)
    nocol   - string, if default="=.", bar is [=======.....]
    """

    # TODO: percent display in the middle of the bar
    if ratio > 1:
        ratio = 1
    elchar, leftchar = nocol
    elapsed = int(round(ratio*length))
    left = length - elapsed
    bar = elchar*elapsed + leftchar*left
    bar = bar[:length]
    if col:
        c_elapsed, c_left, perc = cols
        bar = color(' '*elapsed, "gray", c_elapsed)
        bar = bar + color(' '*left, "gray", c_left)
    else:
        bar = elchar*elapsed + leftchar*left
    return bar




class Term:
    """Linux terminal management.
    
    clear   - calls os.system("clear")
    getch   - get one char at a time
    size    - return height, width of the terminal
    """

    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)
        self.ver = None
        if sys.version_info[0] == 2 and sys.version_info[1] == 0:
            self.ver = 20
        if self.ver == 20:
            self.new_term[3] = (self.new_term[3] & ~TERMIOS.ICANON & 
                ~TERMIOS.ECHO)
        else:
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & 
                ~termios.ECHO)

    def normal(self):
        """Set 'normal' terminal settings."""

        if self.ver == 20:
            termios.tcsetattr(self.fd, TERMIOS.TCSAFLUSH, self.old_term)
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def clear(self):
        """Clear screen."""

        os.system("clear")

    def curses(self):
        """Set 'curses' terminal settings."""

        if self.ver == 20:
            termios.tcsetattr(self.fd, TERMIOS.TCSAFLUSH, self.new_term)
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

    def getch(self):
        """Get one character at a time.
        
        NOTE: if the user suspends (^Z) running program, then brings it
        back to foreground, you have to instantiate Term class again.
        Otherwise getch() won't work. Even after that, the user has to
        hit 'enter' once before he can enter commands.
        """

        self.curses()
        c = os.read(self.fd, 1)
        self.normal()
        return c

    def size(self):
        """Return terminal size as tuple (height, width)."""

        import struct, fcntl
        h,w = 0,0
        if self.ver == 20:
            h, w = struct.unpack("hhhh", fcntl.ioctl(0, 
                    TERMIOS.TIOCGWINSZ, "\000"*8))[0:2]
        else:
            h, w = struct.unpack("hhhh", fcntl.ioctl(0, 
                    termios.TIOCGWINSZ, "\000"*8))[0:2]
        if not h and w:
            h, w = 24, 80
        return h, w
