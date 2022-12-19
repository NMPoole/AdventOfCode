#######################################################################################################################
# Advent of Code 2022 - Day 18
#######################################################################################################################

from __future__ import annotations
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Cube:
    """
    Cube with three dimensions and knows how to return Cube locations at adjacent faces
    """
    x: int
    y: int
    z: int

    # To generate deltas only for faces, we need two of three dimensions to be 0
    ADJ_DELTAS = [(dx, dy, dz) for dx in range(-1, 1 + 1)
                  for dy in range(-1, 1 + 1)
                  for dz in range(-1, 1 + 1)
                  if (dx, dy, dz).count(0) == 2]

    def adjacent(self) -> set[Cube]:
        """
        Return set of adjacent cubes to this cube

        :return: set[Cube] - Set of adjacent cubes
        """
        return {Cube(self.x + dx, self.y + dy, self.z + dz) for dx, dy, dz in Cube.ADJ_DELTAS}


@dataclass
class Droplet:
    """
    Droplet is a volume of 1x1x1 cubes
    """
    ADJACENT_FACES = 6
    filled_cubes: set[Cube]

    def __post_init__(self) -> None:
        """
        Post Initialisation:
        """
        self.all_surface_area: int = 0  # Surface area, internal + external

        # Store max bounds, so we can tell if we've followed a path beyond the perimeter
        self._min_x = self._min_y = self._min_z = 0
        self._max_x = self._max_y = self._max_z = 0

        self._calculate_values()

    def __repr__(self) -> str:
        """
        Represent a droplet by its filled cubes

        :return: str - Formatted string, as described
        """
        return f"Droplet(filled_cubes={len(self.filled_cubes)}"

    def _calculate_values(self) -> None:
        """
        Determine:
            - Total surface area of all filled positions
            - Outer boundaries (min/max x/y/z values) for the droplet
        """
        for filled_cube in self.filled_cubes:
            self.all_surface_area += Droplet.ADJACENT_FACES - len(self.filled_cubes & filled_cube.adjacent())

            self._min_x = min(filled_cube.x, self._min_x)
            self._min_y = min(filled_cube.y, self._min_y)
            self._min_z = min(filled_cube.z, self._min_z)
            self._max_x = max(filled_cube.x, self._max_x)
            self._max_y = max(filled_cube.y, self._max_y)
            self._max_z = max(filled_cube.z, self._max_z)

    def get_external_surface_area(self) -> int:
        """
        Determine surface area of all cubes that can reach the outside
        """
        cubes_to_outside = set()  # Cache cubes we have already identified a path to outside for
        no_path_to_outside = set()  # Store all internal empty
        surfaces_to_outside = 0

        # Loop through the cubes and find any that can reach outside
        for cube in self.filled_cubes:
            for adjacent in cube.adjacent():
                if self._has_path_to_outside(adjacent, cubes_to_outside, no_path_to_outside):
                    cubes_to_outside.add(adjacent)
                    surfaces_to_outside += 1
                else:
                    no_path_to_outside.add(adjacent)

        return surfaces_to_outside

    def _has_path_to_outside(self, cube: Cube, cubes_to_outside: set[Cube], no_path_to_outside: set[Cube]) -> bool:
        """
        Perform Breadth-First-Search to flood fill from this empty cube

        :param cube: Current cube
        :param cubes_to_outside: To cache cubes we've seen before, that we know have a path
        :param no_path_to_outside: To cache cubes we've seen before, that are internal
        :return: bool - True if cube has path to outside, False otherwise
        """
        frontier = deque([cube])
        explored = {cube}

        while frontier:
            current_cube = frontier.popleft()  # FIFO for BFS

            # Check caches:
            if current_cube in cubes_to_outside:
                return True  # We've got out from here before
            if current_cube in no_path_to_outside:
                continue  # This cube doesn't have a path, so no point checking its neighbours

            if current_cube in self.filled_cubes:
                continue  # This path is blocked

            # Check if we've followed a path out of the bounds
            if current_cube.x > self._max_x or current_cube.y > self._max_y or current_cube.z > self._max_z:
                return True
            if current_cube.x < self._min_x or current_cube.y < self._min_y or current_cube.z < self._min_z:
                return True

            # We want to look at all neighbours of this empty space
            for neighbour in current_cube.adjacent():
                if neighbour not in explored:
                    frontier.append(neighbour)
                    explored.add(neighbour)

        return False


def parse_cubes(data: list[str]) -> set[Cube]:
    """
    Parse cubes from input data

    :param data: Data to parse
    :return: set[Cube] - Set of cubes parsed from input data
    """
    cubes = set()
    for line in data:
        coords = tuple(map(int, line.split(",")))
        cubes.add(Cube(*coords))

    return cubes


def main():
    """
    We are examining surface area of a lava droplet. The droplet is made up of many 1x1x1 cubes.
    The input is a list of these cubes.

    Part 1 Solution:
    Count total exposed surface area
    - Cube class knows how to find location of all six adjacent cubes.
    - Droplet class stores cubes.
    - Each cube has a surface area of 6 - (intersection of cube adjacent with all cubes)

    Part 2 Solution:
    What is the exterior surface area of your scanned lava droplet?
    We're told steam wants to expand diagonally.
    - We now need to ignore internal pockets that are sealed to the outside.
    - We need to know if a empty location is interior and if it has a path to the outside.
    - Assume all cubes in our list are connected.
    - Find all adjacent cubes. These are either:
      - These are either:
        - Part of internal pockets. If we flood fill a pocket, it will have a boundary.
        - Part of path to the outside. If we flood fill, we will reach a cube beyond all the droplet bounds.
    - To solve:
      - For each filled cube, get its adjacent
      - BFS for each adjacent, if adjacent is empty space.
      - If the BFS only leads to filled cubes, then all paths are blocked, so cube is internal.
      - If the BFS leads to cubes that our outside our bounds, then this cube has a path out.
      - Store all cubes that have a path out or are internal, and use these to cache the BFS.
      - Only increment the surface area count every time we find an adjacent location that has a path out.
    """
    with open("day18-input.txt", mode="rt") as input_file:
        data = input_file.read().splitlines()

    droplet = Droplet(parse_cubes(data))

    # Part 1:
    print(f"What is the surface area of your scanned lava droplet?"
          f"\nAnswer: {droplet.all_surface_area}")

    # Part 2:
    external_faces = droplet.get_external_surface_area()
    print(f"What is the exterior surface area of your scanned lava droplet?"
          f"\nAnswer: {external_faces}")


if __name__ == "__main__":
    main()
