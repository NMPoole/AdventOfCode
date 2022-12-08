#######################################################################################################################
# Advent of Code 2022 - Day 3
#######################################################################################################################
from typing import List


def part1_solution(rucksacks: List[str], a_to_Z: List[str]) -> int:
    """
    Part 1 Solution: Find the intersecting item found in both compartments of each elf's backpack, and total the
    associated priorities of said items

    :param rucksacks: List of strings, with each string representing the items within an elf's backpack
    :param a_to_Z: List of characters from a..zA..Z used for calculating item priorities
    :return: int - Sum of intersecting item priorities
    """
    priorities_sum = 0

    for curr_rucksack in rucksacks:
        num_items = len(curr_rucksack)

        first_comp, second_comp = curr_rucksack[:num_items // 2], curr_rucksack[num_items // 2:]
        first_comp_set, second_comp_set = set(first_comp), set(second_comp)  # Don't care for num items, just existence

        intersect_item = first_comp_set.intersection(second_comp_set).pop()
        intersect_item_priority = a_to_Z.index(intersect_item) + 1
        priorities_sum += intersect_item_priority

    return priorities_sum


def part2_solution(rucksacks: List[str], a_to_Z: List[str]) -> int:
    """
    Part 2 Solution: Find the intersecting item amongst the backpack contents in each group of three elves - this item
    is the badge. Total the priorities of these badge items

    :param rucksacks: List of strings, with each string representing the items within an elf's backpack
    :param a_to_Z: List of characters from a..zA..Z used for calculating item priorities
    :return: int - Sum of intersecting item priorities
    """
    priorities_sum = 0
    num_rucksacks = len(rucksacks)

    for i in range(0, num_rucksacks, 3):  # Looping over every set of three Elf rucksacks
        first_elf_items, second_elf_items, third_elf_items = rucksacks[i], rucksacks[i + 1], rucksacks[i + 2]
        first_elf_item_set, second_elf_item_set, third_elf_item_set = set(first_elf_items), set(second_elf_items), set(third_elf_items)

        intersect_item = first_elf_item_set.intersection(second_elf_item_set).intersection(third_elf_item_set).pop()
        intersect_item_priority = a_to_Z.index(intersect_item) + 1
        priorities_sum += intersect_item_priority

    return priorities_sum


if __name__ == "__main__":
    with open('day3-input.txt') as file:  # Reading data from file
        elves_rucksacks = file.read().splitlines()

    a_to_Z_list = [chr(i) for i in range(97, 97 + 26)]  # List of chars from a to z, inclusive
    a_to_Z_list.extend([chr(i) for i in range(65, 65 + 26)])  # Extend list of chars from a to z to include A to Z, inclusive

    part1_sol = part1_solution(elves_rucksacks, a_to_Z_list)
    print(f"Find the item type that appears in both compartments of each rucksack."
          f"\nWhat is the sum of the priorities of those item types?"
          f"\nAnswer: {part1_sol}")

    part2_sol = part2_solution(elves_rucksacks, a_to_Z_list)
    print(f"Find the item type that corresponds to the badges of each three-Elf group."
          f"\nWhat is the sum of the priorities of those item types?"
          f"\nAnswer: {part2_sol}")
