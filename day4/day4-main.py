#######################################################################################################################
# Advent of Code 2022 - Day 4
#######################################################################################################################
from collections import Counter


def pair_to_set(p):
    start, end = map(int, p.split("-"))  # Parses 'N-M' format to two ints N and M
    return set(range(start, end + 1))  # Create a set of ints from N to M, inclusive


def sets_fully_overlap(set1, set2):
    return set1.issuperset(set2) or set1.issubset(set2)  # Sets fully overlap if set1 in set2 or set2 in set1


def sets_overlap(set1, set2):
    return bool(set1 & set2)  # Partial overlapping just needs to have intersection members between sets


def part1_solution(input_string):
    counter = Counter()  # Counter of True and False occurrences based on whether the sets fully overlap

    for pair in input_string.splitlines():
        sec1, sec2 = map(pair_to_set, pair.split(","))  # Map 'A-B,C-D' formats to int sets {A,...,B} and {C,...,D}
        counter[sets_fully_overlap(sec1, sec2)] += 1  # Count amount of fully overlapping sets (i.e., assignments)

    return counter[True]


def part2_solution(input_string):
    counter = Counter()  # Counter of True and False occurrences based on whether the sets overlap

    for pair in input_string.splitlines():
        sec1, sec2 = map(pair_to_set, pair.split(","))  # Map 'A-B,C-D' formats to int sets {A,...,B} and {C,...,D}
        counter[sets_overlap(sec1, sec2)] += 1  # Count amount of partially overlapping sets (i.e., assignments)

    return counter[True]


with open('./day4/day4-input.txt') as file:  # Reading data from file
    data = file.read()

# Part 1:
print(f"In how many assignment pairs does one range fully contain the other?"
      f"\nAnswer: {part1_solution(data)}")

# Part 2:
print(f"In how many assignment pairs do the ranges overlap?"
      f"\nAnswer: {part2_solution(data)}")
