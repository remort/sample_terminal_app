#!/usr/bin/python3

import curses
from curses import wrapper
from time import sleep


def get_line(pad, line_no, line_len):
    return [
        (chr(pad.inch(line_no, x) & 0xFF), pad.inch(line_no, x) & curses.A_ATTRIBUTES) for x in range(0, line_len)
    ]


def print_line(pad, line_no, line_len, line=None):
    for char_no in range(0, line_len):
        pad.addch(line_no, char_no, line[char_no][0] if line else ' ', line[char_no][1] if line else curses.A_NORMAL)


def scroll_v(step, coords, pad):
    line = None
    for y in range(0, coords[2]):
        if step > 0:
            line_no = y
        else:
            line_no = coords[2] - y - 1

        if not line:
            line = get_line(pad, line_no, coords[3])
            print_line(pad, line_no, coords[3])
        else:
            curr_l = get_line(pad, line_no, coords[3])
            print_line(pad, line_no, coords[3], line)
            line = curr_l


def get_char_and_attr(pad, line_no, col_no):
    attrs = pad.inch(line_no, col_no)
    ch = chr(attrs & 0xFF)
    attr = attrs & curses.A_ATTRIBUTES
    return ch, attr


def scroll_h(step, coords, pad):
    column = []
    for x in range(0, coords[3]):
        if step > 0:
            col_no = coords[3] - x - 1
        else:
            col_no = x

        tmp_column = []
        if not column:
            for y in range(0, coords[2]):
                column.append(get_char_and_attr(pad, y, col_no))
                pad.addch(y, col_no, ' ', curses.A_NORMAL)
        else:
            for y in range(0, coords[2]):
                tmp_column.append(get_char_and_attr(pad, y, col_no))
                pad.addch(y, col_no, *column[y])
            column = tmp_column


def main(stdscr):
    curses.curs_set(1)
    pad = curses.newpad(100, 100)
    pad.keypad(True)
    pad.nodelay(True)

    my, mx = stdscr.getmaxyx()
    screen_coords = (0, 0, my, mx)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    for y in range(0, my):
        for x in range(0, mx):
            sym = '.' if x % 2 == 0 else ','
            pad.addch(y, x, ord(sym), curses.A_DIM)

    pad.addstr(3, 0, f"{screen_coords}", curses.color_pair(1))

    pad.noutrefresh(0,0, 0,0, my - 1,mx - 1)
    curses.doupdate()

    while True:
        key = pad.getch()

        if key == curses.KEY_END:
            break

        if key == curses.KEY_UP:
            scroll_v(1, screen_coords, pad)
        if key == curses.KEY_DOWN:
            scroll_v(-1, screen_coords, pad)
        if key == curses.KEY_RIGHT:
            scroll_h(1, screen_coords, pad)
        if key == curses.KEY_LEFT:
            scroll_h(-1, screen_coords, pad)

        pad.addstr(3, 0, f"{screen_coords}", curses.color_pair(1))

        pad.noutrefresh(0, 0, 0, 0, my - 1, mx - 1)
        curses.doupdate()
        sleep(0.1)


wrapper(main)
