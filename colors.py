import curses

"""
for i in {0..255} ; do
    printf "\x1b[48;5;%sm%3d\e[0m " "$i" "$i"
    if (( i == 15 )) || (( i > 15 )) && (( (i-15) % 6 == 0 )); then
        printf "\n";
    fi
done
"""

COLOR_DEFAULT = 1
COLOR_ACTOR = 2
COLOR_CURRENT_COORDS = 3
COLOR_STATUS_BAR_STATS = 4
COLOR_STATUS_BAR_MESSAGES = 5
COLOR_UNVEILED_MAP = 6

COLOR_MAP_H1 = 100
COLOR_MAP_H2 = 101
COLOR_MAP_H3 = 102
COLOR_MAP_H4 = 103
COLOR_MAP_H5 = 104
COLOR_MAP_H6 = 105
COLOR_MAP_H7 = 106
COLOR_MAP_H8 = 107
COLOR_MAP_H9 = 108


def init_color_pairs():
    curses.init_pair(COLOR_DEFAULT, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_ACTOR, 167, curses.COLOR_BLACK)
    curses.init_pair(COLOR_CURRENT_COORDS, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_STATUS_BAR_STATS, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(COLOR_STATUS_BAR_MESSAGES, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(COLOR_UNVEILED_MAP, 242, 232)

    curses.init_pair(COLOR_MAP_H1, 247, 17)
    curses.init_pair(COLOR_MAP_H2, 247, 77)
    curses.init_pair(COLOR_MAP_H3, 247, 22)
    curses.init_pair(COLOR_MAP_H4, 247, 70)
    curses.init_pair(COLOR_MAP_H5, 247, 64)
    curses.init_pair(COLOR_MAP_H6, 247, 100)
    curses.init_pair(COLOR_MAP_H7, 247, 136)
    curses.init_pair(COLOR_MAP_H8, 247, 94)
    curses.init_pair(COLOR_MAP_H9, 247, 238)
