#######################################################################################################################
# Advent of Code 2023 - Day 2
#######################################################################################################################
import numpy as np


def parse(games):
    """
    Returns the history of games as a 3-D array (game, color, round).
    """
    COLORS = {"red": 0, "green": 1, "blue": 2}  # Map color to index.
    MAX_PLAY = 10  # HACK: a hard-coded limit of MAX_PLAY rounds per game.

    cubes = np.zeros((len(games), len(COLORS), MAX_PLAY), int)
    for g, game in enumerate(games):
        _, plays = game.split(":")
        for p, play in enumerate(plays.split(";")):
            for pair in play.split(","):
                count, color = pair.split()
                cubes[g, COLORS[color], p] = count

    return cubes


def calc_part1(cubes):
    # The bag is loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes.
    limit = np.array([12, 13, 14])
    valid = np.all(cubes.max(2) <= limit, 1)
    return np.sum(np.argwhere(valid) + 1)


def calc_part2(cubes):
    return cubes.max(2).prod(1).sum()


if __name__ == "__main__":
    input_data = parse(open('day2-input.txt').readlines())  # Read data from input file.

    part1_sol = calc_part1(input_data)
    print(f'What is the sum of the IDs of those games?'
          f'\nAnswer: {part1_sol}')

    part2_sol = calc_part2(input_data)
    print(f'What is the sum of the power of these sets?'
          f'\nAnswer: {part2_sol}')