import random

from asciimatics.effects import Effect
from asciimatics.screen import Screen


class SurfaceFX(Effect):
    def __init__(self, screen, drawer, **kwargs):
        super(SurfaceFX, self).__init__(screen, **kwargs)
        self._drawer = drawer

    def _update(self, frame_no):
        if frame_no % 10 == 0 or frame_no == 1:
            self.draw_canvas()
            self.random_picks()

    @property
    def stop_frame(self):
        return self._stop_frame

    def reset(self):
        pass

    def draw_canvas(self, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_BLACK, char='.'):
        height, width = self._screen.dimensions
        self._drawer.fill_rect(sx=0, sy=0, x=width, y=height, char=char, colour=colour, bg=bg)

    def random_picks(self):
        height, width = self._screen.dimensions
        for i in range(0, 10):
            x, y = random.randint(0, width), random.randint(0, height)
            self._screen.print_at('*', x, y)


class FlagFX(Effect):
    def __init__(self, screen, drawer, **kwargs):
        super(FlagFX, self).__init__(screen, **kwargs)
        self._drawer = drawer

    def _update(self, frame_no):
        self.draw_flag()

    @property
    def stop_frame(self):
        return self._stop_frame

    def reset(self):
        pass

    def draw_flag(self):
        self._drawer.fill_rect(sx=4, sy=1, x=15, y=2, colour=Screen.COLOUR_WHITE)
        self._drawer.fill_rect(sx=4, sy=3, x=15, y=2, colour=Screen.COLOUR_BLUE)
        self._drawer.fill_rect(sx=4, sy=5, x=15, y=2, colour=Screen.COLOUR_RED)
