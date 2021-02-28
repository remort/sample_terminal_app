#!/usr/bin/python3

import random
import typing as t
from pprint import pprint

from dto import Coordinates, Point


class MapGenOld:
    def __init__(self, scale):
        if scale < 2 or scale > 10:
            raise ValueError('Size should lays in 2..9.')

        self.heights_spectre = 8
        # 2 ** 3 == 8
        self.heights_spectre_bits = 3
        self.roughness_factor = self.heights_spectre // 2

        self.steps_to_finish = scale - 1
        self.size: int = self.get_map_size(scale)
        self.map: t.List[t.List[int]] = self.init_map()
        self.coords: Coordinates = self.get_map_corners_coords()

        #self.gen()

    @staticmethod
    def get_map_size(scale: int) -> int:
        return 2 ** scale + 1

    def get_random_factor(self):
        return 0
        # bits: 1 or 2
        #return random.getrandbits(1)

        # factor_bits = self.steps_to_finish // self.roughness_factor
        # if factor_bits > 0:
        #     try:
        #         return random.getrandbits(factor_bits)
        #     except ValueError:
        #         print(factor_bits)
        #         return 0
        # return 0

        #return random.randint(0, round(self.steps_to_finish / self.roughness_factor))

    def get_rand_height(self) -> int:
        return random.getrandbits(3)
        #return random.randint(1, self.heights_spectre)

    def init_map(self) -> t.List[t.List[int]]:
        matrix = list()
        for x in range(0, self.size):
            row = list()
            for y in range(0, self.size):
                if x in (0, self.size - 1) and y in (0, self.size - 1):
                    row.append(self.get_rand_height() + self.get_random_factor())
                else:
                    row.append(0)
            matrix.append(row)

        return matrix

    def get_map_corners_coords(self) -> Coordinates:
        end = self.size - 1
        return Coordinates(
            tl=Point(x=0, y=0),
            tr=Point(x=0, y=end),
            bl=Point(x=end, y=0),
            br=Point(x=end, y=end),
        )

    def get_coords_mid_point_pos(self, coords: Coordinates) -> Point:
        mid_point = Point(
            x=self.get_middle(coords.br.x, coords.tr.x),
            y=self.get_middle(coords.tr.y, coords.tl.y),
        )
        return mid_point

    def calc_avg_for_coords(self, coords: Coordinates) -> int:
        avg = sum((
            self.map[coords.tl.x][coords.tl.y],
            self.map[coords.tr.x][coords.tr.y],
            self.map[coords.br.x][coords.br.y],
            self.map[coords.bl.x][coords.bl.y],
        )) / 4

        return round(avg + self.get_random_factor())

    def calc_three_points_avg(self, point_1: Point, point_2: Point, point_3: Point) -> int:
        avg = round(sum((
            self.map[point_1.x][point_1.y],
            self.map[point_2.x][point_2.y],
            self.map[point_3.x][point_3.y],
        )) / 3)

        return round(avg + self.get_random_factor())

    @staticmethod
    def get_edge_size_by_coords(coords: Coordinates) -> int:
        """Assume that matrix is always a square (same edges length)."""
        return coords.tr.y - coords.tl.y + 1

    def set_center_point_for_coords(self, coords: Coordinates) -> Point:
        avg_val = self.calc_avg_for_coords(coords)
        center_point = self.get_coords_mid_point_pos(coords)
        self.map[center_point.x][center_point.y] = avg_val
        return center_point

    def set_edge_midpoints_for_coords(self, coords: Coordinates, center_point: Point) -> None:
        # top edge center point
        self.map[coords.tl.x][center_point.y] = self.calc_three_points_avg(coords.tl, coords.tr, center_point)

        # bottom edge center point
        self.map[coords.bl.x][center_point.y] = self.calc_three_points_avg(coords.bl, coords.br, center_point)

        # right edge center point
        self.map[center_point.x][coords.br.y] = self.calc_three_points_avg(coords.tr, coords.br, center_point)

        # left edge center point
        self.map[center_point.x][coords.bl.y] = self.calc_three_points_avg(coords.tl, coords.bl, center_point)

    def get_middle(self, int_one: int, int_two: int) -> int:
        s = int_one + int_two
        if s % 2 != 0:
            raise ValueError('Coordinates points not odd:', int_one, int_two)
        return s // 2
        #return int(s / 2)

    def get_subsquares_coords(self, coords: Coordinates) -> t.Tuple[Coordinates, ...]:
        tlp = coords.tl
        trp = coords.tr
        brp = coords.br
        blp = coords.bl

        center_point = Point(x=self.get_middle(brp.x, trp.x), y=self.get_middle(trp.y, tlp.y))
        rows_diff = self.get_middle(blp.x, tlp.x)
        cols_diff = self.get_middle(trp.y, tlp.y)

        tl_square_c = Coordinates(
            tl=tlp,
            tr=Point(x=trp.x, y=cols_diff),
            br=center_point,
            bl=Point(x=rows_diff, y=tlp.y),
        )
        tr_square_c = Coordinates(
            tl=tl_square_c.tr,
            tr=trp,
            br=Point(x=rows_diff, y=trp.y),
            bl=center_point,
        )
        br_square_c = Coordinates(
            tl=center_point,
            tr=tr_square_c.br,
            br=brp,
            bl=Point(x=brp.x, y=cols_diff),
        )
        bl_square_c = Coordinates(
            tl=tl_square_c.bl,
            tr=center_point,
            br=br_square_c.bl,
            bl=blp,
        )

        return tl_square_c, tr_square_c, br_square_c, bl_square_c

    def run_algo(self, coords_set: t.List[Coordinates]) -> t.List[Coordinates]:
        new_coords_set = list()
        for coords in coords_set:
            center_point = self.set_center_point_for_coords(coords)
            self.set_edge_midpoints_for_coords(coords, center_point)
            new_coords_set.extend(self.get_subsquares_coords(coords))

        return new_coords_set

    def gen(self) -> None:

        coords_set = self.run_algo([self.coords])

        while True:
            new_coords_set = self.run_algo(coords_set)
            if self.get_edge_size_by_coords(new_coords_set[0]) <= 2:
                break

            coords_set = new_coords_set
            self.steps_to_finish -= 1

        #pprint(self.map)
        #print(self.steps_to_finish)


if __name__ == "__main__":
    map_gen = MapGenOld(10)
    map_gen.gen()
