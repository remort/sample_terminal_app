from dto import Coordinates, Point, Size


def make_coordinates_from_size(size: Size):
    """Makes only coordinates object with starting point at 0,0."""

    return Coordinates(
        tl=Point(x=0, y=0), tr=Point(x=size.w - 1, y=0),
        br=Point(x=size.w - 1, y=size.h - 1), bl=Point(x=0, y=size.h - 1),
    )
