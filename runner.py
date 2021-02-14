from time import sleep

from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import StopApplication

Q_KEY = 113
F_KEY = 102
UP_BUTT = -204
DOWN_BUTT = -206
RIGHT_BUTT = -205
LEFT_BUTT = -203


class AnimationRunner:
    def __init__(self, screen, sleep_time=0.8):
        self._screen = screen
        self._sleep_time = sleep_time

    def run(self):
        i = 0
        while True:
            self._screen.draw_next_frame()
            if self.process_event(self._screen.get_event()) is False:
                raise StopApplication(message='Stopped by user.')

            i += 1
            self._screen.print_at(i, 0, 0)
            self._screen.refresh()
            sleep(0.05)

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            key_code = event.key_code
            if key_code == F_KEY:
                self._screen.close()
                return False

            if key_code == UP_BUTT:
                self._screen.scroll(1)
            if key_code == DOWN_BUTT:
                self._screen.scroll(-1)
