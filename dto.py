from dataclasses import dataclass


@dataclass()
class Tile:
    x: int
    y: int
    ch: str
    attr: int
    height: int


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
