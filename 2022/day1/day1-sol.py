#######################################################################################################################
# Advent of Code 2022 - Day 1
#######################################################################################################################
from typing import List


def part1_solution(input_str: str) -> tuple[int, List[int]]:
    """
    Part 1 Solution: Sum over thr groups of calories for each elf, and then return the max os the calorie sums

    :param input_str: Input string with all the calorie data inside
    :return: tuple[int, List[int]] - Max calorie total across all elves, and the list of calorie totals (for Part 2)
    """
    calories_groups = input_str.split('\n\n')  # Elves calorie data separated by blank lines
    calories_totals = []

    # For each elf, total their calorie counts (which are separated on new lines) and add to list
    for elf in calories_groups:
        meals = elf.split('\n')
        meals = [eval(i) for i in meals]
        calories_totals.append(sum(meals))

    # Elf with most calories is simply max total in the list
    return max(calories_totals), calories_totals


def part2_solution(calories_totals: List[int]) -> int:
    """
    Part 2 Solution: Total calories of top 3 Elves is simply total of 3 largest items (done via sort first)

    :param calories_totals: List of calories totals across all elves
    :return: int - The sum of calorie totals for the top 3 elves
    """
    calories_totals = sorted(calories_totals, reverse=True)
    return sum(calories_totals[0:3:1])


if __name__ == "__main__":
    data = open('day1-input.txt', 'r').read().strip()  # Read data from input file

    part1_sol, calories = part1_solution(data)
    print(f'Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?'
          f'\nAnswer: {part1_sol}')

    part2_sol = part2_solution(calories)
    print(f'Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?'
          f'\nAnswer: {part2_sol}')
