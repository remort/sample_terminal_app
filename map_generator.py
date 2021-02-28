#!/usr/bin/python3

import random
import typing as t
from pprint import pprint

from dto import Coordinates, Point


class MapGen:
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
        #
        # #return random.randint(0, round(self.steps_to_finish / self.roughness_factor))

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

    def get_map_corners_coords(self):
        end = self.size - 1
        return (
            (0, 0),
            (0, end),
            (end, 0),
            (end, end),
        )

    def get_coords_mid_point_pos(self, coords):
        mid_point = (
            self.get_middle(coords[2][0], coords[1][0]),
            self.get_middle(coords[1][1], coords[0][1]),
        )
        return mid_point

    def calc_avg_for_coords(self, coords):
        tlp = coords[0]
        trp = coords[1]
        brp = coords[2]
        blp = coords[3]

        avg = sum((
            self.map[tlp[0]][tlp[1]],
            self.map[trp[0]][trp[1]],
            self.map[brp[0]][brp[1]],
            self.map[blp[0]][blp[1]],
        )) / 4

        return round(avg + self.get_random_factor())

    def calc_three_points_avg(self, point_1, point_2, point_3) -> int:
        avg = round(sum((
            self.map[point_1[0]][point_1[1]],
            self.map[point_2[0]][point_2[1]],
            self.map[point_3[0]][point_3[1]],
        )) / 3)

        return round(avg + self.get_random_factor())

    @staticmethod
    def get_edge_size_by_coords(coords) -> int:
        """Assume that matrix is always a square (same edges length)."""
        return coords[1][1] - coords[0][1] + 1

    def set_center_point_for_coords(self, coords: t.Tuple[int, int]) -> t.Tuple[int, int]:
        avg_val = self.calc_avg_for_coords(coords)
        center_point = self.get_coords_mid_point_pos(coords)
        self.map[center_point[0]][center_point[1]] = avg_val
        return center_point

    def set_edge_midpoints_for_coords(self, coords, center_point) -> None:
        # top edge center point
        self.map[coords[0][0]][center_point[1]] = self.calc_three_points_avg(coords[0], coords[1], center_point)

        # bottom edge center point
        self.map[coords[3][0]][center_point[1]] = self.calc_three_points_avg(coords[3], coords[2], center_point)

        # right edge center point
        self.map[center_point[0]][coords[2][1]] = self.calc_three_points_avg(coords[1], coords[2], center_point)

        # left edge center point
        self.map[center_point[0]][coords[3][1]] = self.calc_three_points_avg(coords[0], coords[3], center_point)

    def get_middle(self, int_one: int, int_two: int) -> int:
        return (int_one + int_two) // 2

    def get_subsquares_coords(self, coords: t.Tuple[t.Tuple[int, int]]) -> t.Tuple[t.Tuple[t.Tuple[int, int], ...], ...]:
        # coords = ((x, y), (x, y), (x, y), (x, y))
        # tlp = coords[0]
        # trp = coords[1]
        # brp = coords[2]
        # blp = coords[3]

        center_point = (self.get_middle(coords[2][0], coords[1][0]), self.get_middle(coords[1][1], coords[0][1]))
        rows_diff = self.get_middle(coords[3][0], coords[0][0])
        cols_diff = self.get_middle(coords[1][1], coords[0][1])

        tl_square_c = (
            coords[0],
            (coords[1][0], cols_diff),
            center_point,
            (rows_diff, coords[0][1]),
        )
        tr_square_c = (
            tl_square_c[1],
            coords[1],
            (rows_diff, coords[1][1]),
            center_point,
        )
        br_square_c = (
            center_point,
            tr_square_c[2],
            coords[2],
            (coords[2][0], cols_diff),
        )
        bl_square_c = (
            tl_square_c[3],
            center_point,
            br_square_c[3],
            coords[3],
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
    map_gen = MapGen(10)
    map_gen.gen()
