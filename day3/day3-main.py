#######################################################################################################################
# Advent of Code 2022 - Day 3
#######################################################################################################################

with open('./day3/day3-input.txt') as file:  # Reading data from file
    rucksacks = file.read().splitlines()

a_to_Z = [chr(i) for i in range(97, 97 + 26)]  # List of chars from a to z, inclusive
a_to_Z.extend([chr(i) for i in range(65, 65 + 26)])  # Extend list of chars from a to z to include A to Z, inclusive

# Part 1:
priorities_sum = 0
for curr_rucksack in rucksacks:
    num_items = len(curr_rucksack)

    first_comp, second_comp = curr_rucksack[:num_items // 2], curr_rucksack[num_items // 2:]
    first_comp_set, second_comp_set = set(first_comp), set(second_comp)  # Don't care for num of items, just existence

    intersect_item = first_comp_set.intersection(second_comp_set).pop()
    intersect_item_priority = a_to_Z.index(intersect_item) + 1
    priorities_sum += intersect_item_priority

print(f"Find the item type that appears in both compartments of each rucksack."
      f"\nWhat is the sum of the priorities of those item types?"
      f"\nAnswer: {priorities_sum}")

# Part 2:
priorities_sum = 0
num_rucksacks = len(rucksacks)
for i in range(0, num_rucksacks, 3):  # Looping over every set of three Elf rucksacks
    first_elf_items, second_elf_items, third_elf_items = rucksacks[i], rucksacks[i + 1], rucksacks[i + 2]
    first_elf_item_set, second_elf_item_set, third_elf_item_set = set(first_elf_items), set(second_elf_items), set(third_elf_items)

    intersect_item = first_elf_item_set.intersection(second_elf_item_set).intersection(third_elf_item_set).pop()
    intersect_item_priority = a_to_Z.index(intersect_item) + 1
    priorities_sum += intersect_item_priority

print(f"Find the item type that corresponds to the badges of each three-Elf group."
      f"\nWhat is the sum of the priorities of those item types?"
      f"\nAnswer: {priorities_sum}")
