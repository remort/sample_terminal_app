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


def init_color_pairs():
    curses.init_pair(COLOR_DEFAULT, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_ACTOR, 167, curses.COLOR_BLACK)
    curses.init_pair(COLOR_CURRENT_COORDS, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_STATUS_BAR_STATS, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(COLOR_STATUS_BAR_MESSAGES, curses.COLOR_BLUE, curses.COLOR_YELLOW)
