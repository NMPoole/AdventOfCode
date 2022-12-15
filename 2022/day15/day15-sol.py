#######################################################################################################################
# Advent of Code 2022 - Day 15
#######################################################################################################################

import re
from typing import Tuple, Set, List, NamedTuple


class Point(NamedTuple):
    """
    Point is a tuple of x and y co-ordinate values
    """
    x: int
    y: int


class Line(NamedTuple):
    """
    Line is represented by gradient, m, and intersect, b
    """
    m: float
    b: float


class Range(NamedTuple):
    """
    Range of ints from start to end
    """
    start: int
    end: int


def manhattan_dist(a: Point, b: Point) -> int:
    """
    Compute the Manhattan distance between two Points

    :param a: First Point
    :param b: Second Point
    :return: int - Manhattan dist between points
    """
    return abs(a.x - b.x) + abs(a.y - b.y)


def is_range_overlap(a: Range, b: Range) -> bool:
    """
    Determine whether two ranges overlap
    Two ranges overlap if the end of one range is after the start of another

    :param a: First Range
    :param b: Second Range
    :return: bool - True if ranges overlap, False otherwise
    """
    return a.end > b.start or a.start < b.end


def combine_ranges(ranges: List[Range]) -> List[Range]:
    """
    Combine a list of ranges to remove overlapping ranges (Part 1 utility method)

    :param ranges: List of ranges to combine
    :return: List[Range] -
    """
    new_ranges: List[Range] = []
    ranges_0: Range = ranges.pop(0)

    while len(ranges) > 1:
        ranges_1: Range = ranges.pop(0)
        was_consumed: bool = False

        while is_range_overlap(ranges_0, ranges_1):
            ranges_0 = Range(min(ranges_0.start, ranges_1.start), max(ranges_0.end, ranges_1.end))
            if ranges:
                ranges_1 = ranges.pop(0)
            else:
                break
            was_consumed = True

        new_ranges.append(ranges_0)

        if was_consumed:
            if ranges:
                ranges_0 = ranges.pop(0)
        else:
            ranges_0 = ranges_1

    return new_ranges


def line_intersection(line_1: Line, line_2: Line) -> Point:
    """
    Calculate the intersection of two lines (Part 2 utility method)

    :param line_1: First line
    :param line_2: Second line
    :return: Point - Line intersection
    """
    x = (line_1.b - line_2.b) / (line_2.m - line_1.m)
    y = (line_1.m * x) + line_1.b

    return Point(round(x), round(y))


def part_1() -> int:
    """
    Part 1 Solution:

    :return: int - Number of positions that cannot contain a beacon
    """
    sensor_beacons: Set[Tuple[Point, Point]] = set()
    beacons: Set[Point] = set()

    # Read input from file:
    with open("day15-input.txt", "r") as input_file:
        for line in input_file:
            sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall("-?\d+", line))
            sensor = Point(sensor_x, sensor_y)
            beacon = Point(beacon_x, beacon_y)
            sensor_beacons.add((sensor, beacon))
            beacons.add(beacon)

    row = 2000000
    ranges: List[Range] = []

    for sensor, beacon in sensor_beacons:
        m_dist = manhattan_dist(sensor, beacon)
        dist_to_row = abs(row - sensor.y)

        if m_dist >= dist_to_row:
            flex_along_row = abs(m_dist - dist_to_row)
            cov_along_row = Range(sensor.x - flex_along_row, sensor.x + flex_along_row)
            ranges.append(cov_along_row)

    ranges = sorted(ranges, key=lambda curr_range: curr_range.start)
    ranges = combine_ranges(ranges)

    count = 0
    for r in ranges:
        count += r.end + 1 - r.start
    count -= len([beacon for beacon in beacons if beacon.y == row])

    return count


def part_2():
    """
    Part 2 Solution:

    "To isolate the distress beacon's signal, you need to determine its tuning frequency, which can be found by
    multiplying its x coordinate by 4000000 and then adding its y coordinate"

    :return: int - Tuning frequency
    """
    lines: Set[Line] = set()

    # Read input from file:
    with open("day15-input.txt", "r") as input_file:
        for line in input_file:
            sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall("-?\d+", line))
            sensor = Point(sensor_x, sensor_y)
            beacon = Point(beacon_x, beacon_y)
            dist = manhattan_dist(sensor, beacon)
            points: List[Point] = [
                Point(sensor.x + dist, sensor.y),
                Point(sensor.x - dist, sensor.y),
                Point(sensor.x, sensor.y + dist),
                Point(sensor.x, sensor.y - dist),
            ]

            for a, b in [(a, b) for i, a in enumerate(points) for b in points[i + 1:]]:
                if not a.x == b.x and not a.y == b.y:
                    m = (a.x - b.x) / (a.y - b.y)
                    b = a.y - m * a.x
                    lines.add(Line(m, b))

    line_pairs: Set[Tuple[Line, Line]] = set()

    for line_1 in lines:
        for line_2 in lines:
            if line_1 is not line_2:
                if line_1.m == line_2.m and abs(line_1.b - line_2.b) == 2 and line_1.b != line_2.b:
                    line_pairs.add((
                        min(line_1, line_2, key=lambda x: x.b),
                        max(line_1, line_2, key=lambda x: x.b)
                    ))

    pairs: List[Tuple[Line, Line]] = sorted(list(line_pairs), key=lambda x: x[0].b)
    intersection: Point = line_intersection(pairs[0][1], pairs[1][0])  # Intersection of lower line from each pair

    return intersection.x * 4_000_000 + intersection.y  # Tuning frequency


def main():
    part1_sol = part_1()
    print(f"Consult the report from the sensors you just deployed."
          f"\nIn the row where y=2000000, how many positions cannot contain a beacon?"
          f"\nAnswer: {part1_sol}")

    part2_sol = part_2()
    print(f"Find the only possible position for the distress beacon."
          f"\nWhat is its tuning frequency?"
          f"\nAnswer: {part2_sol}")


if __name__ == "__main__":
    main()
