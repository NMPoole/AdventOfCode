#######################################################################################################################
# Advent of Code 2022 - Day 12
#######################################################################################################################

from __future__ import annotations
from collections import deque
from copy import deepcopy
from dataclasses import dataclass


@dataclass(frozen=True)  # Adds sunder methods automatically - frozen makes attributes read-only after creation
class Point:
    """
    Point class:
    A point knows how to return a list of all adjacent coordinates
    """
    x: int
    y: int

    def neighbours(self) -> list[Point]:
        """
        Return all adjacent orthogonal (not diagonal) Points
        """
        return [Point(self.x + dx, self.y + dy)
                for dx in range(-1, 2)
                for dy in range(-1, 2)
                if abs(dy) != abs(dx)
                ]


class Grid:
    """
    2D Grid class (comprised of Points):
    """

    def __init__(self, grid_array: list[str]) -> None:
        """
        Generate Grid instance from 2D array:

        :param grid_array: List of strings representing rows of elevations which comprise the Grid
        """
        self.array = deepcopy(grid_array)  # Store a deep copy of input data to prevent mutation

        self.x_size = len(self.array[0])
        self.y_size = len(self.array)

        self.start = self._get_point_for_elevation("S")
        self.goal = self._get_point_for_elevation("E")

    def _all_points(self) -> list[Point]:
        """
        Get all points in the Grid as a list

        :return: list[Point] - List of Points comprising the grid
        """
        points = [Point(x, y) for x in range(self.x_size) for y in range(self.y_size)]
        return points

    def all_lowest_elevation_points(self) -> set[Point]:
        """
        Get all points at the lowest elevation in the Grid

        :return: set[Point] - Set of all lowest elevation points in the grid
        """
        low_points = {point for point in self._all_points()
                      if self.array[point.y][point.x] == "a" or self.array[point.y][point.x] == "S"
                      }
        return low_points

    def _get_point_for_elevation(self, x: str) -> Point:
        """
        Find the point where specified start, "S", or end, "E", are located

        :param x: Either 'S' to get start location, or 'E' to get end location (in Grid)
        :return Point - Location of start or end, as specified
        """
        if x not in ("S", "E"):
            print("Specified point must be Start (S) or End (E)!")
            exit(-1)

        for row_num, row in enumerate(self.array):
            if x in row:
                return Point(row.index(x), row_num)

    def elevation_at_point(self, point: Point) -> int:
        """
        Elevation value at this point

        :param point: Point to retrieve elevation for
        :return int - Elevation at given point
        """
        if point not in (self.start, self.goal):
            return ord(self.array[point.y][point.x])
        if point == self.start:
            return ord("a")  # Start location is elevation 'a'
        if point == self.goal:
            return ord("z")  # End location is elevation 'z'

    def _point_in_grid(self, point: Point) -> bool:
        """
        Check if a location is within the grid

        :param point: Point to check if within grid for
        :return bool - True if point within Grid, False otherwise
        """
        return 0 <= point.x < self.x_size and 0 <= point.y < self.y_size

    def _valid_neighbours(self, location: Point):
        """
        Yield adjacent neighbour points:
        We can move L, R, U, D by one, but only to locations that are no more than one higher than current elevation

        :param location: Current location we are moving from
        :return Yields valid neighbours we can move to from current location
        """
        current_elevation = self.elevation_at_point(location)

        for neighbour in location.neighbours():
            if self._point_in_grid(neighbour) and self.elevation_at_point(neighbour) <= current_elevation + 1:
                yield neighbour

    def get_path(self, start: Point) -> list[Point] | None:
        """
        Given a starting point, determine the best path to reach the goal specified by 'E'

        :param start: Starting point to seek path from towards the end
        :return list[Point] | None - List of points comprising the path, or None if no valid path from this start point
        """
        points_to_assess = deque()  # Points we want to get value and neighbours of
        points_to_assess.append(start)  # First point to assess is start

        curr_point = None
        points_came_from = {start: None}

        while points_to_assess:  # They should only ever be valid points
            curr_point = points_to_assess.popleft()

            if curr_point == self.goal:  # We've reached the end
                break

            for neighbour in self._valid_neighbours(curr_point):
                if neighbour not in points_came_from:  # We will need to assess this point
                    points_to_assess.append(neighbour)
                    points_came_from[neighbour] = curr_point

        if curr_point != self.goal:
            return None  # No valid path from this point

        # Recover the path
        curr_point = self.goal
        path = []
        while curr_point != start:
            path.append(curr_point)
            curr_point = points_came_from[curr_point]

        return path

    def __repr__(self) -> str:
        """
        Custom string representation of the Grid, for debugging purposes

        :return: Formatted string representing the state of the Grid
        """
        return "\n".join("".join(map(str, row)) for row in self.array)


def main():
    """
    Input is a grid of elevations, where 'a' is lowest, and z is tallest
    We need to navigate the grid, from Start to End
    We can move to any adjacent L, R, U, D location, if that location's elevation is no greater than curr elevation + 1

    Part 1:
    What is the fewest steps required to move from your current position to the goal?
    - Find the shortest path from Start (S) to End (E)
    - Use a Breadth-First-Search (BFS)

    Part 2:
    What is the shortest number of steps (path), given all starting locations `a` to the goal?
    - Find the shortest path from all lowest points (given as "a")
    - Apply the BFS for each start location
    - Report the shortest path
    - Many starting locations have no valid paths, which needs to be handled

    NOTE: A faster search algorithm than BFS could have been used (e.g., informed A* search), but not necessary...
    """
    with open("day12-input.txt", mode="rt") as input_file:
        data = input_file.read().splitlines()

    grid = Grid(data)

    # Part 1:
    path = grid.get_path(grid.start)
    part1_length = len(path)

    print(f"What is the fewest steps required to move from your current position to the location that should get the "
          f"best signal?"
          f"\nAnswer: {part1_length}")

    # Part 2:
    start_points = grid.all_lowest_elevation_points()
    part2_length = part1_length  # We know of at least one solution that must be improved upon, the solution from Part 1
    for start in start_points:
        path = grid.get_path(start)
        if path:
            part2_length = min(part2_length, len(path))

    print(f"What is the fewest steps required to move starting from any square with elevation a to the location that "
          f"should get the best signal?"
          f"\nAnswer: {part2_length}")


if __name__ == "__main__":
    main()
