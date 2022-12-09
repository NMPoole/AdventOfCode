#######################################################################################################################
# Advent of Code 2022 - Day 9
#######################################################################################################################
from typing import List


def get_directions() -> List[tuple[str, int]]:
    """
    Read the set of directions for the rope head to follow from file
    These directions are given in the format: '<U|D|L|R> <num_steps>'
        , where <U|D|L|R> is the direction of movement (e.g., 'R' = right)
        , and <num_steps> is the number of steps made in said direction

    :return: List[tuple[str, int]] - Directions as list of tuples with direction and num steps - e.g., '('U', 2)'
    """
    lines = open("day9-input.txt", 'r').read().splitlines()
    directions = [(line.split()[0], int(line.split()[1])) for line in lines]
    return directions


def sign(x: int) -> int:
    """
    Utility function to get the sign of a number

    :param x: Number to get sign for
    :return: Sign of the number, with 1 being positive, and -1 being negative
    """
    return 1 if x >= 0 else -1


def is_adjacent(pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
    """
    Calculate whether two positions are adjacent in 2D space
    The positions can be horizontally, vertically, or diagonally adjacent and must be separated by exactly 1 space

    :param pos1: First position to check adjacency of
    :param pos2: Second position to check adjacency of
    :return: bool - True if positions considered adjacent, False otherwise
    """
    if abs(pos1[0] - pos2[0]) == 1 and pos1[1] == pos2[1]:  # Horizontally adjacent
        return True
    elif pos1[0] == pos2[0] and abs(pos1[0] - pos2[0]) == 1:  # Vertically adjacent
        return True
    elif abs(pos1[0] - pos2[0]) == 1 and abs(pos1[1] - pos2[1]) == 1:  # Diagonally adjacent
        return True
    else:  # Not adjacent
        return False


def update_rope_knot_pos(head_pos: tuple[int, int], tail_pos: tuple[int, int]) -> None:
    """
    Updates the position of the tail (i.e., trailing knot) which directly follows head (i.e., leading knot)

    :param head_pos: Current position of the head knot
    :param tail_pos: Current position of the tail knot
    """
    # Guard Condition: Head and tail are at same position or are adjacent, so do nothing
    if head_pos == tail_pos or is_adjacent(head_pos, tail_pos):
        return

    head_x, head_y = head_pos
    tail_x, tail_y = tail_pos

    if abs(head_x - tail_x) == 2 and head_y == tail_y:  # Move tail horizontally
        tail_pos[0], tail_pos[1] = tail_x + sign(head_x - tail_x), tail_y

    elif head_x == tail_x and abs(head_y - tail_y) == 2:  # Move tail vertically
        tail_pos[0], tail_pos[1] = tail_x, tail_y + sign(head_y - tail_y)

    elif abs(head_x - tail_x) == 1 and abs(head_y - tail_y) == 2:  # Move tail diagonally - case 1
        tail_pos[0], tail_pos[1] = head_x, tail_y + sign(head_y - tail_y)

    elif abs(head_x - tail_x) == 2 and abs(head_y - tail_y) == 1:  # Move tail diagonally - case 2
        tail_pos[0], tail_pos[1] = tail_x + sign(head_x - tail_x), head_y

    elif abs(head_x - tail_x) == 2 and abs(head_y - tail_y) == 2:  # Move tail diagonally - case 3
        tail_pos[0], tail_pos[1] = tail_x + sign(head_x - tail_x), tail_y + sign(head_y - tail_y)


def move_rope_with_n_knots(num_knots: int) -> int:
    """
    Parts 1 and 2 Solution - Generic function for n knots in the rope:
    Moves are processed iteratively with each movement propagated down all the knots in the rope
    Each knot acts as the head for the next knot along the rope

    :param num_knots: Number of nots in the rope
    :return: int - Number of positions traced by the rope tail at least once
    """
    direction_map = {'U': [0, 1], 'D': [0, -1], 'R': [1, 0], 'L': [-1, 0]}
    directions_to_follow = get_directions()  # Read directions from input file

    # Maps knots (0..num_knots-1) to curr pos as (x, y) with knot 0 considered as the head
    knot_positions = {i: [0, 0] for i in range(num_knots)}
    positions_traced_by_tail = set()

    for curr_dir, num_moves in directions_to_follow:
        x, y = direction_map[curr_dir]

        for _ in range(num_moves):
            # Move rope head
            head_pos = knot_positions[0]
            head_pos[0], head_pos[1] = head_pos[0] + x, head_pos[1] + y
            knot_positions[0] = head_pos

            # Move all knots following the head
            for knot_num in range(1, num_knots):
                prev_knot_pos = knot_positions[knot_num - 1]
                curr_knot_pos = knot_positions[knot_num]
                update_rope_knot_pos(prev_knot_pos, curr_knot_pos)
                knot_positions[knot_num] = curr_knot_pos

            # Add tail position to positions traced
            tail_pos = knot_positions[num_knots - 1]
            positions_traced_by_tail.add((tail_pos[0], tail_pos[1]))

    return len(positions_traced_by_tail)


if __name__ == "__main__":
    part1_sol = move_rope_with_n_knots(num_knots=2)
    print(f"Simulate your complete hypothetical series of motions."
          f"\nHow many positions does the tail of the rope visit at least once?"
          f"\nAnswer: {part1_sol}")

    part2_sol = move_rope_with_n_knots(num_knots=10)
    print(f"Simulate your complete series of motions on a larger rope with ten knots."
          f"\nHow many positions does the tail of the rope visit at least once?"
          f"\nAnswer: {part2_sol}")
