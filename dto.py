import typing as t

from dataclasses import dataclass


@dataclass()
class Point:
    x: int
    y: int


@dataclass()
class Tile:
    ch: str
    color: int
    height: int
    is_veiled: bool = True
    loc: Point = None
    attr: t.Optional[int] = None
    x: t.Optional[int] = None
    y: t.Optional[int] = None

    def __post_init__(self):
        self.x = self.loc.x
        self.y = self.loc.y


@dataclass()
class Size:
    w: int
    h: int


@dataclass()
class Coordinates:
    tl: Point
    tr: Point
    br: Point
    bl: Point
