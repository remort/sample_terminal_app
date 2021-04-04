#!/usr/bin/python3

import argparse
import curses
import logging
import sys
import traceback
from curses import wrapper

from colors import init_color_pairs
from configuration.file_storage import ConfigurationFileStorageHandler
from configuration.main import Configuration
from constants import BAR_HEIGHT
from controllers.actor import ActorController
from controllers.map import MapController
from controllers.status_bar import StatusBarController
from dto import Size
from errors import BaseAppError
from pad_wrapper import Pad
from runner import ApplicationRunner
from surface_generator import SurfaceGenerator, get_map_size_by_scale
from utils import generate_map_from_surface, get_map_scale_by_screen_size, make_coordinates_by_size

logging.basicConfig(
    filename='application.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
)

log = logging.getLogger(__name__)


def get_args() -> argparse.Namespace:
    log.debug('Parsing command arguments.')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', action='store_true',
        help='Run in debug mode. This unveils map on start, runs no map discover on every move, moves faster.',
    )
    parser.add_argument(
        '--square-tiles', action='store_true',
        help='Map tile is being drawn as two terminal symbols. Horizontal movements jump over two tiles a time.',
    )
    parser.add_argument(
        '--load-config', action='store',
        help='Point a name of previously saved config file here to continue on the saved state.',
    )
    return parser.parse_args()


def configure(screen_height: int, screen_width: int, args: argparse.Namespace) -> Configuration:
    log.debug('Program configuring.')
    config = Configuration(ConfigurationFileStorageHandler())

    if args.debug:
        config.debug = True

    if args.square_tiles:
        config.square_tiles = True

    config.map_scale = get_map_scale_by_screen_size(screen_height, screen_width)
    config.map_size = get_map_size_by_scale(config.map_scale)

    config.map_pad_h = config.map_size
    config.map_pad_w = (config.map_size * 2) if config.square_tiles else config.map_size

    config.scene_size = Size(w=screen_width, h=screen_height - BAR_HEIGHT)
    config.scene_pad_coords = make_coordinates_by_size(Size(w=screen_width, h=screen_height - BAR_HEIGHT))

    config.status_bar_width = screen_width

    if args.load_config:
        config.load(args.load_config)
    else:
        config.surface = SurfaceGenerator(config.map_scale).gen()
        config.map = generate_map_from_surface(config.surface)

    return config


def main(stdscr: curses.window) -> None:
    log.debug('Program starting.')

    command_args = get_args()
    screen_height, screen_width = stdscr.getmaxyx()
    config = configure(screen_height, screen_width, command_args)

    curses.curs_set(0)
    init_color_pairs()

    kb_pad = Pad(1, 1)
    map_pad = Pad(config.map_pad_h, config.map_pad_w)
    actor_pad = Pad(1, 1 + (1 if config.square_tiles else 0))
    status_bar_pad = Pad(1, config.status_bar_width)

    map = MapController(map_pad, config)
    actor = ActorController(actor_pad, config)
    status_bar = StatusBarController(status_bar_pad, config)

    pad_controllers = [map, actor, status_bar]

    runner = ApplicationRunner(kb_pad, pad_controllers, config)
    runner.run()


args = get_args()
try:
    wrapper(main)
except BaseAppError as error:
    log.exception('Fatal error: %s', error)
    print(f'Fatal error: "{error}": See logs for details.')
    exit(1)
except Exception as error:
    log.exception('Unknown fatal error: %s', error)
    traceback.print_exception(*sys.exc_info())
    exit(127)
