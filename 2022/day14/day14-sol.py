#######################################################################################################################
# Advent of Code 2022 - Day 14
#######################################################################################################################

ROCK = "#"
SAND = "o"
SAND_ORIGIN = (500, 0)  # Co-ordinate where sand enters the cave


def parse_cave_lines(input_file_str: str) -> dict:
    """
    Parse the cave lines from file

    :param input_file_str: Location of file to read cave lines from
    :return: dict - Mapping of co-ordinates comprising the grid, which are all rock lines presently (dict to be ext)
    """
    cave = {}

    for line in open(input_file_str).readlines():
        coords = line.split(" -> ")

        for from_coord, to_coord in zip(coords[0::], coords[1::]):
            from_x, from_y = (int(n) for n in from_coord.split(","))
            to_x, to_y = (int(n) for n in to_coord.split(","))

            for x in range(min(from_x, to_x), max(from_x, to_x) + 1):
                cave[x, from_y] = ROCK

            for y in range(min(from_y, to_y), max(from_y, to_y) + 1):
                cave[from_x, y] = ROCK

    return cave


def cave_bottom(cave: dict) -> int:
    """
    Gets the bottom y co-ordinate of the cave

    :param cave: The cave dict containing rock co-ordinates
    :return: int - Yhe bottom y co-ordinate of the cave
    """
    bottom_y = max(y for (_, y), val in cave.items() if val == ROCK)
    return bottom_y


def drop_sand(cave: dict) -> bool:
    """
    Simulates the dropping of a sand grain in the cave

    :param cave: The case to drop the sand through
    :return: bool - True if sand rests anywhere but the sand origin, False otherwise (i.e., no rest or at origin)
    """
    x = SAND_ORIGIN[0]

    cave_bottom_y = cave_bottom(cave)
    for y in range(cave_bottom_y):
        if (x, y + 1) not in cave:  # Move Down?
            pass
        elif (x - 1, y + 1) not in cave:  # Move Diagonal-Left Down?
            x -= 1
        elif (x + 1, y + 1) not in cave:  # Move Diagonal-Right Down?
            x += 1
        else:  # Sand comes to rest
            cave[(x, y)] = SAND
            return (x, y) != SAND_ORIGIN

    return False


def add_cave_floor(cave: dict) -> None:
    """
    Adds a bottom to the cave floor at "two plus the highest y coordinate"

    :param cave: Cave to add floor to
    """
    bottom_y = cave_bottom(cave)
    for x in range(-10 * bottom_y, 10 * bottom_y):  # Safe-ish guess at cave width that causes it to fill to sand origin
        cave[x, bottom_y + 2] = ROCK


def simulate(has_abyss: bool, cave: dict) -> dict:
    """
    Simulate the falling of sand within the cave

    :param has_abyss: Whether the bottom of the cave is an abyss, or the cave floor
    :param cave: Cave dict to simulate sand falling through
    :return: State of the cave after sand falling simulated (i.e., sand falling into abyss now, or cave is full)
    """
    if not has_abyss:
        add_cave_floor(cave)

    while drop_sand(cave):
        pass  # Just needs to simulate falling sand and cave state is mutated

    return cave


def main():
    cave = parse_cave_lines("day14-input.txt")

    part1_cave = simulate(True, cave).values()  # Simulate with abyss
    part1_sol = sum(1 for cave_tile in part1_cave if cave_tile == SAND)
    print(f"Using your scan, simulate the falling sand."
          f"\nHow many units of sand come to rest before sand starts flowing into the abyss below?"
          f"\nAnswer: {part1_sol}")

    part2_cave = simulate(False, cave).values()  # Simulate with cave floor
    part2_sol = sum(1 for cave_tile in part2_cave if cave_tile == SAND)
    print(f"Using your scan, simulate the falling sand until the source of the sand becomes blocked."
          f"\nHow many units of sand come to rest?"
          f"\nAnswer: {part2_sol}")


if __name__ == "__main__":
    main()
