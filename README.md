#### 2d surface generation app to be run in terminal.

Generates map on every run, draws it and gives the interface to navigate on it.

Run it with `./run.py` in linux terminal.

`./run -h` for usage.

#### Controls

Navigate over map with `<Up>, <Down>, <Left>` and `<Right>` arrows on keyboard.

Key `<End>` ends the execution.

#### Misc

Uses python curses to draw in terminal and work with it.

Surface generator uses Diamond-Square algorithm:
[Diamond-Square](https://en.wikipedia.org/wiki/Diamond-square_algorithm)

Eyesight logic for map discovering calculations,
uses "linear interpolation" to get intermediary points between player and distant point on the map.
[Linear interpolation](https://x-engineer.org/undergraduate-engineering/advanced-mathematics/numerical-methods/linear-interpolation-and-extrapolation-with-calculator/)

#### TODO:

Try to re-implement this algorithm also as an alternative to Diamond-Square:
[pymap](https://github.com/octaviotron/pymap)
