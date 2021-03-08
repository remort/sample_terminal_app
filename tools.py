import curses
import typing as t

from colors import COLOR_DEFAULT


class Pad:
    def __init__(self, height: int, width: int) -> None:
        pad = curses.newpad(height, width)
        pad.keypad(True)
        pad.nodelay(True)
        self._pad: t.Any = pad

    @property
    def pad(self) -> t.Any:
        return self._pad

    def print(
            self,
            string: str,
            y: int = 0,
            x: int = 0,
            attr: int = curses.A_NORMAL,
            n: t.Optional[int] = None,
            cp: t.Optional[int] = COLOR_DEFAULT,
    ) -> None:
        if not n:
            self._pad.addstr(y, x, string, curses.color_pair(cp) | attr)
        else:
            self._pad.addnstr(y, x, string, n, curses.color_pair(cp) | attr)

    def getch(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        return self._pad.getch(*args, **kwargs)

    def addch(
            self,
            char: str,
            y: int = 0,
            x: int = 0,
            attr: int = curses.A_NORMAL,
            cp: t.Optional[int] = COLOR_DEFAULT,
    ) -> t.Any:
        self._pad.addch(y, x, char, curses.color_pair(cp) | attr)

    def erase(self) -> t.Any:
        self._pad.erase()

    def noutrefresh(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        self._pad.noutrefresh(*args, **kwargs)

    def refresh(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        self._pad.noutrefresh(*args, **kwargs)

    def bkgd(self, ch: str, cp: int, attr: int = curses.A_NORMAL):
        self._pad.bkgdset(ch, curses.color_pair(cp) | attr)
