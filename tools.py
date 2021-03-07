import curses

from colors import COLOR_DEFAULT


class Pad:
    def __init__(self, height, width):
        pad = curses.newpad(height, width)
        pad.keypad(True)
        pad.nodelay(True)
        self._pad = pad

    @property
    def pad(self):
        return self._pad

    def print(
            self,
            string,
            y=0,
            x=0,
            attr=curses.A_NORMAL,
            n=None,
            cp=COLOR_DEFAULT,
    ):
        if not n:
            self._pad.addstr(y, x, string, curses.color_pair(cp) | attr)
        else:
            self._pad.addnstr(y, x, string, n, curses.color_pair(cp) | attr)

    def getch(self, *args, **kwargs):
        return self._pad.getch(*args, **kwargs)

    def addch(self, *args, **kwargs):
        self._pad.addch(*args, **kwargs)

    def erase(self):
        self._pad.erase()

    def noutrefresh(self, *args, **kwargs):
        self._pad.noutrefresh(*args, **kwargs)
