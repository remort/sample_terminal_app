import curses
import logging
import typing as t

from colors import COLOR_DEFAULT

log = logging.getLogger(__name__)


class Pad:
    def __init__(self, height: int, width: int) -> None:
        pad = curses.newpad(height, width)
        pad.keypad(True)
        pad.nodelay(True)
        self._pad: t.Any = pad
        self.height, self.width = self._pad.getmaxyx()

    @property
    def pad(self) -> t.Any:
        return self._pad

    def print(
            self,
            string: str,
            y: int = 0,
            x: int = 0,
            attr: int = curses.A_NORMAL,
            cp: t.Optional[int] = COLOR_DEFAULT,
            sq: bool = False,
    ) -> None:
        attrs = curses.color_pair(cp) | attr
        if sq:
            x = x * 2
            self._pad.insstr(y, x, string, attrs)
            self._pad.insstr(y, x + 1, string, attrs)
        else:
            self._pad.insstr(y, x, string, attrs)

    def getch(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        return self._pad.getch(*args, **kwargs)

    def addch(
            self,
            char: str,
            y: int = 0,
            x: int = 0,
            attr: int = curses.A_NORMAL,
            cp: t.Optional[int] = COLOR_DEFAULT,
            sq: bool = False,
    ) -> t.Any:
        attrs = curses.color_pair(cp) | attr
        try:
            if sq:
                x = x * 2
                self._pad.addch(y, x, char, attrs)
                self._pad.addch(y, x + 1, char, attrs)
            else:
                self._pad.addch(y, x, char, attrs)
        except curses.error as error:
            log.warning('Error adding character: "%s".', error)
            log.warning('Line, col: %s, %s, Pad: H %s, W %s', y, x, self.height, self.width)
            if (y + 1, x + 2 if sq else 1) == (self.height, self.width):
                log.info('Ignore curses failure on carriage return on last line.')
                return
            raise error

    def noutrefresh(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        self._pad.noutrefresh(*args, **kwargs)

    def refresh(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        self._pad.noutrefresh(*args, **kwargs)

    def bkgd(self, ch: str, cp: int, attr: int = curses.A_NORMAL):
        self._pad.bkgdset(ch, curses.color_pair(cp) | attr)

    def erase(self):
        self._pad.erase()

    def move(self, new_x, new_y):
        self._pad.move(new_x, new_y)
