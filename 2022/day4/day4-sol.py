#######################################################################################################################
# Advent of Code 2022 - Day 4
#######################################################################################################################
from collections import Counter


def pair_to_set(pair_str: str) -> set:
    """
    Convert string from 'N-M' format into a set of ints from N to M, inclusive

    :param pair_str: String in 'N-M' format to convert
    :return: set - Set of ints from N to M, inclusive
    """
    start, end = map(int, pair_str.split("-"))
    return set(range(start, end + 1))


def sets_fully_overlap(set1: set, set2: set) -> bool:
    """
    Check if two sets fully overlap (i.e., both sets are equal or one is a superset of the other)

    :param set1: First set to check overlap for
    :param set2: Second set to check overlap for
    :return: True if sets fully overlap, False otherwise
    """
    return set1.issuperset(set2) or set1.issubset(set2)  # Sets fully overlap if set1 in set2 or set2 in set1


def sets_overlap(set1: set, set2: set) -> bool:
    """
    Check if two sets overlap (i.e., both sets have at least one member in common)

    :param set1: First set to check overlap for
    :param set2: Second set to check overlap for
    :return: True if sets overlap, False otherwise
    """
    return bool(set1 & set2)


def part1_solution(input_string: str) -> int:
    """
    Part 1 Solution: Count the amount of sets that fully overlap in the assignments of each pair of elves

    :param input_string: Input string containing elf pair assignments
    :return: int - Count of assignments that fully overlap
    """
    counter = Counter()  # Counter of True and False occurrences based on whether the sets fully overlap

    for pair in input_string.splitlines():
        sec1, sec2 = map(pair_to_set, pair.split(","))  # Map 'A-B,C-D' formats to int sets {A,...,B} and {C,...,D}
        counter[sets_fully_overlap(sec1, sec2)] += 1  # Count amount of fully overlapping sets (i.e., assignments)

    return counter[True]


def part2_solution(input_string: str) -> int:
    """
    Part 2 Solution: Count the amount of sets that overlap in the assignments of each pair of elves

    :param input_string: Input string containing elf pair assignments
    :return: int - Count of assignments that overlap
    """
    counter = Counter()  # Counter of True and False occurrences based on whether the sets overlap

    for pair in input_string.splitlines():
        sec1, sec2 = map(pair_to_set, pair.split(","))  # Map 'A-B,C-D' formats to int sets {A,...,B} and {C,...,D}
        counter[sets_overlap(sec1, sec2)] += 1  # Count amount of partially overlapping sets (i.e., assignments)

    return counter[True]


if __name__ == "__main__":
    with open('day4-input.txt') as file:  # Reading data from file
        data = file.read()

    # Part 1:
    part1_sol = part1_solution(data)
    print(f"In how many assignment pairs does one range fully contain the other?"
          f"\nAnswer: {part1_sol}")

    # Part 2:
    part2_sol = part2_solution(data)
    print(f"In how many assignment pairs do the ranges overlap?"
          f"\nAnswer: {part2_sol}")
