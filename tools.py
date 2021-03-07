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

    def addch(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        self._pad.addch(*args, **kwargs)

    def erase(self) -> t.Any:
        self._pad.erase()

    def noutrefresh(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        self._pad.noutrefresh(*args, **kwargs)
