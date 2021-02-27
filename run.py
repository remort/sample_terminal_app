#!/usr/bin/python3

import curses
from curses import wrapper

from colors import init_color_pairs
from controllers.actor import ActorControler
from controllers.map import MapController
from controllers.status_bar import StatusBarController
from dto import Size
from runner import AnimationRunner
from storage import RuntimeStorage
from tools import Pad


def main(stdscr):
    curses.curs_set(0)
    init_color_pairs()

    screen_height, screen_width = stdscr.getmaxyx()

    kb_pad = Pad(1, 1)
    map_pad = Pad(100, 100)
    actor_pad = Pad(2, 2)
    status_pad = Pad(1, screen_width)

    storage = RuntimeStorage()
    storage.bar_height = 1

    map_size = Size(w=80, h=30)

    surface = MapController(map_pad, storage, map_size, Size(w=screen_width, h=screen_height - storage.bar_height))
    actor = ActorControler(actor_pad, storage)
    status_bar = StatusBarController(status_pad, storage)

    scenes = [surface, actor, status_bar]

    runner = AnimationRunner(kb_pad, scenes, storage)
    runner.run()


wrapper(main)
