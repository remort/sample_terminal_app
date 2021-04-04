import typing as t

from dataclasses import asdict, dataclass


@dataclass()
class Point:
    x: int
    y: int

    def serialize(self):
        return asdict(self)


@dataclass()
class Tile:
    ch: str
    color: int
    height: int
    x: int
    y: int
    is_veiled: bool = True
    attr: t.Optional[int] = None

    @property
    def loc(self):
        return Point(x=self.x, y=self.y)

    def serialize(self):
        return asdict(self)


@dataclass()
class Size:
    w: int
    h: int

    def serialize(self):
        return asdict(self)


@dataclass()
class Coordinates:
    tl: Point
    tr: Point
    br: Point
    bl: Point

    def serialize(self):
        return asdict(self)


MapType = t.List[t.List[Tile]]
