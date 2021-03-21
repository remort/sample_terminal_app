#!/usr/bin/python3
import argparse
import curses
import logging
from curses import wrapper

from colors import init_color_pairs
from controllers.actor import ActorController
from controllers.map import MapController
from controllers.status_bar import StatusBarController
from dto import Size
from runner import AnimationRunner
from storage import RuntimeStorage
from surface_generator import SurfaceGenerator, get_map_size_by_scale
from tools import Pad
from utils import (
    generate_map_from_surface,
    get_map_scale_by_screen_size,
    make_coordinates_by_size,
    make_map_coordinates_by_pad_dimensions,
)

logging.basicConfig(
    filename='application.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
)

log = logging.getLogger(__name__)


def configure(screen_height: int, screen_width: int) -> RuntimeStorage:
    log.debug('Program configuring.')
    storage = RuntimeStorage()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', action='store_true',
        help='Run in debug mode. This unveils map on start, runs no map discover on every move, moves faster.',
    )
    parser.add_argument(
        '--square-tiles', action='store_true',
        help='Map tile is being drawn as two terminal symbols. Horizontal movements jump over two tiles a time.',
    )

    args = parser.parse_args()
    if args.debug:
        storage.debug = True

    if args.square_tiles:
        storage.square_tiles = True

    storage.map_scale = get_map_scale_by_screen_size(screen_height, screen_width)
    storage.map_size = get_map_size_by_scale(storage.map_scale)

    storage.map_pad_h = storage.map_size
    storage.map_pad_w = (storage.map_size * 2) if storage.square_tiles else storage.map_size

    storage.map_pad_coords = make_map_coordinates_by_pad_dimensions(storage.map_pad_h, storage.map_pad_w)

    storage.surface = SurfaceGenerator(storage.map_scale).gen()
    storage.scene_size = Size(w=screen_width, h=screen_height - storage.bar_height)
    storage.scene_pad_coords = make_coordinates_by_size(Size(w=screen_width, h=screen_height - storage.bar_height))

    storage.status_bar_width = screen_width

    storage.map = generate_map_from_surface(storage)

    return storage


def main(stdscr: curses.window) -> None:
    log.debug('Program starting.')
    curses.curs_set(0)
    init_color_pairs()

    screen_height, screen_width = stdscr.getmaxyx()

    storage = configure(screen_height, screen_width)

    kb_pad = Pad(1, 1)
    map_pad = Pad(storage.map_pad_h, storage.map_pad_w)
    actor_pad = Pad(1, 1 + (1 if storage.square_tiles else 0))
    status_bar_pad = Pad(1, storage.status_bar_width)

    map = MapController(map_pad, storage)
    actor = ActorController(actor_pad, storage)
    status_bar = StatusBarController(status_bar_pad, storage)

    scenes = [map, actor, status_bar]

    runner = AnimationRunner(kb_pad, scenes, storage)
    runner.run()


wrapper(main)
