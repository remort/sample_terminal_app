import curses
from time import sleep


class AnimationRunner:
    def __init__(self, kb_pad, scenes, storage, sleep_time=0.1):
        self._kb_pad = kb_pad
        self._scenes = scenes
        self._storage = storage
        self._sleep_time = sleep_time

    def run(self):
        while True:
            key = self._kb_pad.getch()

            if key == curses.KEY_END:
                break

            if key != -1:
                for scene in self._scenes:
                    scene.process_event(key)

            for scene in self._scenes:
                scene.do_animation()
            curses.doupdate()

            sleep(self._sleep_time)
