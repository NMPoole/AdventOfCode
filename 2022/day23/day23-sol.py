#######################################################################################################################
# Advent of Code 2022 - Day 23
#######################################################################################################################

from copy import copy


def read_input(input_file_str: str) -> set[tuple[int, int]]:
    """
    Read elf positions in grid of ground tiles from a given input file

    :param input_file_str: Location to input file as string
    :return: set[tuple[int, int]] - Set of elf positions read/parsed from file
    """
    elves = set()

    with open(input_file_str) as input_file:
        for i, line in enumerate(input_file.readlines()):
            line = line.strip()
            for j, c in enumerate(line):
                if c == '#':
                    elves.add((j, i))

    return elves


def get_tiles_around(elf_x: int, elf_y: int) -> list[tuple[int, int]]:
    """
    Given the position of an elf, return the set of adjacent tiles around the elf

    :param elf_x: Current x co-ordinate of elf
    :param elf_y: Current y co-ordinate of elf
    :return: list[tuple[int, int]] - List of tile co-ordinates around the elf
    """
    tiles_around = [
        (elf_x, elf_y + 1),  # N
        (elf_x + 1, elf_y + 1),  # NE
        (elf_x + 1, elf_y),  # E
        (elf_x + 1, elf_y - 1),  # SE
        (elf_x, elf_y - 1),  # S
        (elf_x - 1, elf_y - 1),  # SW
        (elf_x - 1, elf_y),  # W
        (elf_x - 1, elf_y + 1),  # NW
    ]

    return tiles_around


def get_proposals(elves: set[tuple[int, int]], directions: list[tuple[int, int]]) -> dict:
    """
    Get the proposed new positions for each elf to move to according to the given rules of 'unstable diffusion'

    :param elves: Set of current elf co-ordinates
    :param directions: Ordered list of directions for each elf to consider moving in
    :return: dict - Mapping of elf co-ordinates to their corresponding proposals - either a new pos, or None
    """
    proposals = {}

    for curr_elf_x, curr_elf_y in elves:

        tiles_around = get_tiles_around(curr_elf_x, curr_elf_y)

        for adj_x, adj_y in tiles_around:
            if (adj_x, adj_y) in elves:  # Already an elf at the proposed position
                for dir_x, dir_y in directions:
                    propose_move = True

                    for adj_x, adj_y in tiles_around:
                        if (dir_x == 0 and adj_y - curr_elf_y == dir_y) or (dir_y == 0 and adj_x - curr_elf_x == dir_x):
                            if (adj_x, adj_y) in elves:
                                propose_move = False
                                break

                    if propose_move:
                        if (curr_elf_x + dir_x, curr_elf_y + dir_y) in proposals:
                            proposals[(curr_elf_x + dir_x, curr_elf_y + dir_y)] = None
                        else:
                            proposals[(curr_elf_x + dir_x, curr_elf_y + dir_y)] = (curr_elf_x, curr_elf_y)
                        break
                break  # An elf can move only in one direction!

    return proposals


def simulate_rounds(elves: set[tuple[int, int]], is_part1: bool = False) -> tuple[int, int]:
    """
    Simulate the rounds of moving by the elves via their unstable diffusion rules

    :param elves: Set of elf co-ordinates at the beginning
    :param is_part1: Whether simulating rounds for Part 1 or Part 2 of the question
    :return: tuple[int, int] - Total number of empty ground tiles, and round number
    """
    # Ordered directions to consider by elves
    directions = [
        (0, -1),
        (0, +1),
        (-1, 0),
        (+1, 0),
    ]

    min_x, min_y, max_x, max_y = None, None, None, None
    diffusion_round = 0
    proposals = True

    while proposals:
        # Start round by getting elf proposals for movements
        diffusion_round += 1
        proposals = get_proposals(elves, directions)

        # Moving elves according to proposals
        for (proposed_x, proposed_y), elf in proposals.items():
            if elf:
                elves.remove(elf)
                elves.add((proposed_x, proposed_y))

        # Smallest rectangle containing the elves
        min_x = min([x for x, y in elves])
        max_x = max([x for x, y in elves])
        min_y = min([y for x, y in elves])
        max_y = max([y for x, y in elves])

        # Rotate considered directions
        directions = directions[1:] + directions[:1]

        # No need to proceed past 10 rounds for part 1
        if is_part1 and diffusion_round == 10:
            break

    empty_ground_tiles = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)  # Total num tiles in rect - elves in it
    return empty_ground_tiles, diffusion_round


if __name__ == "__main__":
    """
    Advent of Code 2022 - Day 23 Solution:
    """
    # Read input data:
    elves_start = read_input("day23-input.txt")

    # Part 1:
    part1_sol, _ = simulate_rounds(copy(elves_start), is_part1=True)  # Copy elves so parts don't interfere
    print(f"Simulate the Elves' process and find the smallest rectangle that contains the Elves after 10 rounds."
          f"\nHow many empty ground tiles does that rectangle contain?"
          f"\nAnswer: {part1_sol}")

    # Part 2:
    _, part2_sol = simulate_rounds(elves_start)
    print(f"Figure out where the Elves need to go."
          f"\nWhat is the number of the first round where no Elf moves?"
          f"\nAnswer: {part2_sol}")

