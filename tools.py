import curses
import typing as t

from colors import COLOR_DEFAULT


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
            x1 = x * 2
            x2 = x1 + 1
            self._pad.insstr(y, x1, string, attrs)
            self._pad.insstr(y, x2, string, attrs)
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
        if sq:
            x1 = x * 2
            x2 = x1 + 1
            self._pad.addch(y, x1, char, attrs)
            self._pad.addch(y, x2, char, attrs)
        else:
            self._pad.addch(y, x, char, attrs)

    def noutrefresh(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        self._pad.noutrefresh(*args, **kwargs)

    def refresh(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        self._pad.noutrefresh(*args, **kwargs)

    def bkgd(self, ch: str, cp: int, attr: int = curses.A_NORMAL):
        self._pad.bkgdset(ch, curses.color_pair(cp) | attr)
