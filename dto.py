import typing as t

from dataclasses import dataclass


@dataclass()
class Tile:
    x: int
    y: int
    ch: str
    color: int
    height: int
    attr: t.Optional[int] = None
    is_veiled: bool = True


@dataclass()
class Size:
    w: int
    h: int


@dataclass()
class Point:
    x: int
    y: int


@dataclass()
class Coordinates:
    tl: Point
    tr: Point
    br: Point
    bl: Point
