#!/usr/bin/python3

import random
import typing as t
from pprint import pprint

SurfacePoint = t.Tuple[int, int]
SurfaceCoords = t.Tuple[SurfacePoint, SurfacePoint, SurfacePoint, SurfacePoint]
Surface = t.List[t.List[int]]


def get_map_size_by_scale(scale: int) -> int:
    return 2 ** scale + 1


class SurfaceGenerator:
    def __init__(self, scale: int) -> None:
        if scale < 2 or scale > 10:
            raise ValueError('Size should lays in 2..10.')

        self.scale: int = scale
        self.initial_value: int = -10

        self.steps_to_finish: int = scale - 1
        self.size: int = get_map_size_by_scale(scale)
        self.coords: SurfaceCoords = self.get_map_corners_coords()
        self.surface: Surface = self.init_map()

        self.rnd_power = 3
        self.rnd_denominator_base = 2 ** (self.rnd_power + 0.3)
        self.rnd_denominator_step = self.rnd_denominator_base / (self.scale / 2)

    @staticmethod
    def round(x: float):
        """2.5 -> 3, 2.4 -> 2, unlike modern round()."""
        return int(x + 0.5)

    def get_roughness_factor(self) -> t.Union[float, int]:
        denominator = self.rnd_denominator_base + self.rnd_denominator_step * (self.scale - self.steps_to_finish)
        value = random.getrandbits(self.rnd_power) / denominator

        if not value:
            return 0

        return value if random.getrandbits(1) else -value

    def get_rand_height(self) -> int:
        # works much faster than random.randint()
        return random.getrandbits(3)

    def get_distanced_randoms_for_surface_corners(self) -> t.Tuple[int, int, int, int]:
        tl_height = self.get_rand_height()
        tr_height = self.get_rand_height()
        while abs(tl_height - tr_height) <= 3:
            tr_height = self.get_rand_height()

        br_height = self.get_rand_height()
        while abs(tr_height - br_height) <= 2 or tl_height == br_height:
            br_height = self.get_rand_height()

        bl_height = self.get_rand_height()
        while bl_height in (tl_height, tr_height, br_height):
            bl_height = self.get_rand_height()

        return tl_height, tr_height, br_height, bl_height

    def set_surface_corners(self, tl_height: int, tr_height: int, br_height: int, bl_height: int) -> None:
        tl = self.coords[0]
        tr = self.coords[1]
        br = self.coords[2]
        bl = self.coords[3]

        self.surface[tl[0]][tl[1]] = tl_height
        self.surface[tr[0]][tr[1]] = tr_height
        self.surface[br[0]][br[1]] = br_height
        self.surface[bl[0]][bl[1]] = bl_height

    def init_map(self) -> Surface:
        matrix = list()
        for x in range(0, self.size):
            row = list()
            for y in range(0, self.size):
                row.append(self.initial_value)
            matrix.append(row)

        self.surface = matrix
        self.set_surface_corners(*self.get_distanced_randoms_for_surface_corners())

        return self.surface

    def get_map_corners_coords(self) -> SurfaceCoords:
        end = self.size - 1
        return (
            (0, 0),
            (0, end),
            (end, end),
            (end, 0),
        )

    def get_coords_mid_point_pos(self, coords: SurfaceCoords) -> SurfacePoint:
        return (
            self.get_middle(coords[2][0], coords[1][0]),
            self.get_middle(coords[1][1], coords[0][1]),
        )

    def calc_center_point_avg(self, coords: SurfaceCoords) -> int:
        return self.calc_four_points_avg(*coords)

    def calc_four_points_avg(
            self,
            point_1: SurfacePoint,
            point_2: SurfacePoint,
            point_3: SurfacePoint,
            point_4: t.Optional[SurfacePoint],
    ) -> int:
        avg = sum((
            self.surface[point_1[0]][point_1[1]],
            self.surface[point_2[0]][point_2[1]],
            self.surface[point_3[0]][point_3[1]],
            self.surface[point_4[0]][point_4[1]] if point_4 is not None else 0,
        )) / (4 if point_4 else 3)

        return self.round(avg + self.get_roughness_factor())

    @staticmethod
    def get_edge_size_by_coords(coords: SurfaceCoords) -> int:
        """Assume that matrix is always a square (same edges length)."""
        return coords[1][1] - coords[0][1] + 1

    def set_center_point_for_coords(self, coords: SurfaceCoords) -> None:
        avg_val = self.calc_center_point_avg(coords)
        center_point = self.get_coords_mid_point_pos(coords)
        self.surface[center_point[0]][center_point[1]] = avg_val

    def set_edge_midpoints_for_coords(self, coords: SurfaceCoords, edge_size: int) -> None:
        center_point = self.get_coords_mid_point_pos(coords)

        edge_size_from_0 = edge_size - 1

        upper_mid_point = None
        upper_mid_point_x = center_point[0] - edge_size_from_0
        if upper_mid_point_x > 0:
            upper_mid_point = (upper_mid_point_x, center_point[1])

        lower_mid_point = None
        lower_mid_point_x = center_point[0] + edge_size_from_0
        if lower_mid_point_x < self.size:
            lower_mid_point = (lower_mid_point_x, center_point[1])

        rightmost_mid_point = None
        righmost_mid_point_y = center_point[1] + edge_size_from_0
        if righmost_mid_point_y < self.size:
            rightmost_mid_point = (center_point[0], righmost_mid_point_y)

        leftmost_mid_point = None
        leftmost_mid_point_y = center_point[1] - edge_size_from_0
        if leftmost_mid_point_y > self.size:
            leftmost_mid_point = (center_point[0], leftmost_mid_point_y)

        # top edge center point
        if self.surface[coords[0][0]][center_point[1]] == self.initial_value:
            self.surface[coords[0][0]][center_point[1]] = self.calc_four_points_avg(
                coords[0], coords[1], center_point, upper_mid_point
            )

        # bottom edge center point
        if self.surface[coords[3][0]][center_point[1]] == self.initial_value:
            self.surface[coords[3][0]][center_point[1]] = self.calc_four_points_avg(
                coords[3], coords[2], center_point, lower_mid_point
            )

        # right edge center point
        if self.surface[center_point[0]][coords[2][1]] == self.initial_value:
            self.surface[center_point[0]][coords[2][1]] = self.calc_four_points_avg(
                coords[1], coords[2], center_point, rightmost_mid_point
            )

        # left edge center point
        if self.surface[center_point[0]][coords[3][1]] == self.initial_value:
            self.surface[center_point[0]][coords[3][1]] = self.calc_four_points_avg(
                coords[0], coords[3], center_point, leftmost_mid_point
            )

    def get_middle(self, int_one: int, int_two: int) -> int:
        return (int_one + int_two) // 2

    def get_subsquares_coords(
            self, coords: SurfaceCoords,
    ) -> t.Tuple[SurfaceCoords, SurfaceCoords, SurfaceCoords, SurfaceCoords]:

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

    def run_algo(self, coords_set: t.List[SurfaceCoords]) -> t.List[SurfaceCoords]:
        edge_size = self.get_edge_size_by_coords(coords_set[0])
        new_coords_set = list()
        for coords in coords_set:
            self.set_center_point_for_coords(coords)

        for coords in coords_set:
            self.set_edge_midpoints_for_coords(coords, edge_size)

            new_coords_set.extend(self.get_subsquares_coords(coords))

        return new_coords_set

    def print(self):
        width = self.size * 3 + 2
        pprint(self.surface, width=width)

    def gen(self, print: bool = False) -> Surface:
        coords_set = self.run_algo([self.coords])

        while True:
            new_coords_set = self.run_algo(coords_set)
            if self.get_edge_size_by_coords(new_coords_set[0]) <= 2:
                break

            coords_set = new_coords_set
            self.steps_to_finish -= 1

        if print:
            self.print()

        return self.surface


class SurfaceGeneratorTest(SurfaceGenerator):
    def __init__(self) -> None:
        super(SurfaceGeneratorTest, self).__init__(scale=4)
        self.expected_surface = [[1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                                 [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                 [2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                 [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                 [3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                 [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                 [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                 [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                 [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                                 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                                 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                                 [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                                 [6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                                 [6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                                 [6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                                 [7, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]

    def get_distanced_randoms_for_surface_corners(self) -> t.Tuple[int, int, int, int]:
        return 1, 3, 5, 7

    def get_roughness_factor(self) -> int:
        return 0

    def get_rand_height(self) -> int:
        return 5

    def test(self) -> None:
        self.gen(print=True)
        assert self.surface == self.expected_surface


if __name__ == "__main__":
    SurfaceGenerator(2).gen(print=True)
    SurfaceGeneratorTest().test()
