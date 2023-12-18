#######################################################################################################################
# Advent of Code 2023 - Day 3
#######################################################################################################################
from re import finditer
from math import prod

if __name__ == '__main__':
    board = open('day3-input.txt').readlines()  # Read data from input file.

    chars = {
        (r, c): [] for r in range(140) for c in range(140) if board[r][c] not in '01234566789.'
    }

    for r, row in enumerate(board):
        for n in finditer(r'\d+', row):
            edge = {
                (r, c) for r in (r - 1, r, r + 1) for c in range(n.start() - 1, n.end() + 1)
            }

            for o in edge & chars.keys():
                chars[o].append(int(n.group()))

    part1_sol = sum(sum(p) for p in chars.values())
    print(f"What is the sum of all of the part numbers in the engine schematic?"
          f"\nAnswer: {part1_sol}")

    part2_sol = sum(prod(p) for p in chars.values() if len(p) == 2)
    print(f"What is the sum of all of the gear ratios in your engine schematic?"
          f"\nAnswer: {part2_sol}")
