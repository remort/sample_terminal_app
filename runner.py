import curses
import typing as t
from time import sleep

from controllers.base import BaseController
from storage import RuntimeStorage
from tools import Pad


class AnimationRunner:
    def __init__(
            self,
            kb_pad: Pad,
            scenes: t.List[BaseController],
            storage: RuntimeStorage,
            sleep_time: t.Optional[float] = 0.05,
    ):
        self._kb_pad = kb_pad
        self._scenes = scenes
        self._st = storage
        self._sleep_time = sleep_time
        self._step_waits = self._st.heights_to_wait_time_map

    def calc_wait_time(self) -> float:
        tile = self._st.map[self._st.actor_location.y][self._st.actor_location.x]
        return self._step_waits[tile.height]

    def run(self):
        while True:
            key = self._kb_pad.getch()
            curses.flushinp()

            if key == curses.KEY_END:
                break

            if key != -1:
                for scene in self._scenes:
                    scene.process_event(key)

            for scene in self._scenes:
                scene.do_animation()

            curses.doupdate()
            sleep(self.calc_wait_time())
