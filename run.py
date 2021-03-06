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
from surface_generator import SurfaceGenerator, get_map_size_by_scale
from tools import Pad
from utils import get_map_scale_by_screen_size, make_map_coordinates_by_map_size


def main(stdscr):
    curses.curs_set(0)
    init_color_pairs()

    screen_height, screen_width = stdscr.getmaxyx()

    storage = RuntimeStorage()

    storage.map_scale = get_map_scale_by_screen_size(screen_height, screen_width)
    storage.map_size = get_map_size_by_scale(storage.map_scale)
    storage.map_coords = make_map_coordinates_by_map_size(storage.map_size)
    storage.surface = SurfaceGenerator(storage.map_scale).gen()

    kb_pad = Pad(1, 1)
    map_pad = Pad(storage.map_size+1, storage.map_size+1)
    actor_pad = Pad(2, 2)
    status_pad = Pad(1, screen_width + 1)

    surface = MapController(map_pad, storage, Size(w=screen_width, h=screen_height - storage.bar_height))
    actor = ActorControler(actor_pad, storage)
    status_bar = StatusBarController(status_pad, storage, screen_width)

    scenes = [surface, actor, status_bar]

    runner = AnimationRunner(kb_pad, scenes, storage)
    runner.run()


wrapper(main)
