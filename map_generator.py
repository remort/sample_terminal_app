#!/usr/bin/python3

import random
import typing as t
from pprint import pprint

Point = t.Tuple[int, int]
Coordinates = t.Tuple[Point, Point, Point, Point]


class MapGen:
    def __init__(self, scale):
        if scale < 2 or scale > 10:
            raise ValueError('Size should lays in 2..10.')

        self.heights_spectre = 8
        # 2 ** 3 == 8
        self.heights_spectre_bits = 3
        self.roughness_factor = self.heights_spectre // 2

        self.steps_to_finish = scale - 1
        self.size: int = self.get_map_size(scale)
        self.map: t.List[t.List[int]] = self.init_map()
        self.coords: Coordinates = self.get_map_corners_coords()

    @staticmethod
    def get_map_size(scale: int) -> int:
        return 2 ** scale + 1

    @staticmethod
    def round(x):
        """2.5 -> 3, 2.4 -> 2, unlike modern round()."""
        return int(x + 0.5)

    def get_random_factor(self) -> int:
        value = random.getrandbits(1)
        if not value:
            return 0
        return value if random.getrandbits(1) else -value

    def get_rand_height(self) -> int:
        # works much faster than random.randint()
        return random.getrandbits(3)

    def init_map(self) -> t.List[t.List[int]]:
        matrix = list()
        for x in range(0, self.size):
            row = list()
            for y in range(0, self.size):
                if x in (0, self.size - 1) and y in (0, self.size - 1):
                    row.append(self.get_rand_height() + self.get_random_factor())
                else:
                    row.append(-1)
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

    def get_coords_mid_point_pos(self, coords: Coordinates) -> Point:
        return (
            self.get_middle(coords[2][0], coords[1][0]),
            self.get_middle(coords[1][1], coords[0][1]),
        )

    def calc_avg_for_coords(self, coords: Coordinates) -> int:
        avg = sum((
            self.map[coords[0][0]][coords[0][1]],
            self.map[coords[1][0]][coords[1][1]],
            self.map[coords[2][0]][coords[2][1]],
            self.map[coords[3][0]][coords[3][1]],
        )) / 4

        return self.round(avg + self.get_random_factor())

    def calc_four_points_avg(self, point_1: Point, point_2: Point, point_3: Point, point_4: Point) -> int:
        avg = sum((
            self.map[point_1[0]][point_1[1]],
            self.map[point_2[0]][point_2[1]],
            self.map[point_3[0]][point_3[1]],
            self.map[point_4[0]][point_3[1]] if point_4 else 0,
        )) / 4 if point_4 else 3

        return self.round(avg + self.get_random_factor())

    @staticmethod
    def get_edge_size_by_coords(coords: Coordinates) -> int:
        """Assume that matrix is always a square (same edges length)."""
        return coords[1][1] - coords[0][1] + 1

    def set_center_point_for_coords(self, coords: Coordinates) -> None:
        avg_val = self.calc_avg_for_coords(coords)
        center_point = self.get_coords_mid_point_pos(coords)
        self.map[center_point[0]][center_point[1]] = avg_val

    def set_edge_midpoints_for_coords(self, coords: Coordinates, edge_size: int) -> None:
        center_point = self.get_coords_mid_point_pos(coords)

        upper_mid_point = None
        upper_mid_point_x = center_point[0] - edge_size
        if upper_mid_point_x > 0:
            upper_mid_point = (upper_mid_point_x, center_point[1])

        lower_mid_point = None
        lower_mid_point_x = center_point[0] + edge_size
        if lower_mid_point_x < self.size:
            lower_mid_point = (lower_mid_point_x, center_point[1])

        rightmost_mid_point = None
        righmost_mid_point_y = center_point[1] + edge_size
        if righmost_mid_point_y < self.size:
            rightmost_mid_point = (center_point[0], righmost_mid_point_y)

        leftmost_mid_point = None
        leftmost_mid_point_y = center_point[1] - edge_size
        if leftmost_mid_point_y > self.size:
            leftmost_mid_point = (center_point[0], leftmost_mid_point_y)

        # top edge center point
        if self.map[coords[0][0]][center_point[1]] == -1:
            self.map[coords[0][0]][center_point[1]] = self.calc_four_points_avg(
                coords[0], coords[1], center_point, upper_mid_point
            )

        # bottom edge center point
        if self.map[coords[3][0]][center_point[1]] == -1:
            self.map[coords[3][0]][center_point[1]] = self.calc_four_points_avg(
                coords[3], coords[2], center_point, lower_mid_point
            )

        # right edge center point
        if self.map[center_point[0]][coords[2][1]] == -1:
            self.map[center_point[0]][coords[2][1]] = self.calc_four_points_avg(
                coords[1], coords[2], center_point, rightmost_mid_point
            )

        # left edge center point
        if self.map[center_point[0]][coords[3][1]] == -1:
            self.map[center_point[0]][coords[3][1]] = self.calc_four_points_avg(
                coords[0], coords[3], center_point, leftmost_mid_point
            )

    def get_middle(self, int_one: int, int_two: int) -> int:
        return (int_one + int_two) // 2

    def get_subsquares_coords(self, coords: Coordinates) -> t.Tuple[Coordinates, ...]:
        # top left point = coords[0]
        # top right point = coords[1]
        # bottom right point = coords[2]
        # bottom left point = coords[3]

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
        edge_size = self.get_edge_size_by_coords(coords_set[0])
        new_coords_set = list()
        for coords in coords_set:
            self.set_center_point_for_coords(coords)

        for coords in coords_set:
            self.set_edge_midpoints_for_coords(coords, edge_size)

            new_coords_set.extend(self.get_subsquares_coords(coords))

        return new_coords_set

    def print(self):
        pprint(self.map, width=200)

    def gen(self) -> None:
        coords_set = self.run_algo([self.coords])

        while True:
            new_coords_set = self.run_algo(coords_set)
            if self.get_edge_size_by_coords(new_coords_set[0]) <= 2:
                break

            coords_set = new_coords_set
            self.steps_to_finish -= 1


class MapGenTest(MapGen):
    def __init__(self):
        super(MapGenTest, self).__init__(scale=4)
        self.expected_map = [[5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5],
                             [3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3],
                             [3, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 3],
                             [3, 3, 3, 4, 4, 4, 3, 4, 4, 4, 3, 4, 4, 4, 3, 3, 3],
                             [3, 2, 3, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 3, 3, 2, 3],
                             [3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3],
                             [3, 2, 3, 2, 3, 3, 4, 3, 4, 3, 4, 3, 3, 2, 3, 2, 3],
                             [3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3],
                             [3, 2, 2, 2, 3, 2, 3, 3, 5, 3, 3, 2, 3, 2, 2, 2, 3],
                             [3, 3, 3, 3, 3, 3, 3, 4, 3, 4, 4, 4, 4, 3, 3, 3, 3],
                             [3, 2, 3, 2, 3, 2, 4, 3, 3, 3, 4, 3, 4, 2, 3, 2, 3],
                             [3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3],
                             [3, 2, 2, 2, 4, 3, 3, 2, 3, 2, 3, 3, 4, 2, 2, 2, 3],
                             [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                             [3, 2, 4, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 4, 2, 3],
                             [3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 3],
                             [5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5]]

    def get_random_factor(self):
        return 0

    def get_rand_height(self) -> int:
        return 5

    def test(self):
        self.gen()
        assert self.map == self.expected_map


if __name__ == "__main__":
    map_gen = MapGen(6)
    map_gen.gen()
    map_gen.print()
