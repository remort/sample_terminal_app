from asciimatics.screen import Screen


class Drawer:
    def __init__(self, screen):
        self._screen = screen

    def fill_rect(self, sx=0, sy=0, x=1, y=1, char='#', colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_BLACK):
        for i in range(0, y):
            self._screen.move(sx, sy + i)
            self._screen.draw(sx+x, sy+i, char=char, colour=colour, thin=True, bg=bg)
