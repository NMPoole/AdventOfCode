#######################################################################################################################
# Advent of Code 2022 - Day 16
#######################################################################################################################

import sys
import functools

sys.setrecursionlimit(10000)
STATE = {}


def read_input(file_str: str) -> None:
    """
    Read input about the valve config into state

    :param file_str: Location to input file as string
    """
    with open(file_str, "r") as input_file:
        for line in input_file:
            line = line.strip().split(" ")
            name = line[1]
            rate = int(line[4].split("=")[-1].split(";")[0])
            valves = [word.split(",")[0] for word in line[9:]]

            STATE[name] = {"rate": rate, "valves": valves}


@functools.cache
def part_one(open_valves: frozenset, mins_remaining: int, curr_valve: str) -> int:
    """
    Part 1 Solution:

    :param open_valves: Set of valves that have been opened and are releasing pressure each minute
    :param mins_remaining: Number of minutes remaining in the current function call (used recursively)
    :param curr_valve: Curr valve moved to in this function call (used recursively)
    :return: int - Most pressure that can be released
    """
    if mins_remaining <= 0:  # Base Case: No time left, so cannot open more valves
        return 0

    best = 0
    curr_valve_state = STATE[curr_valve]

    for valve in curr_valve_state["valves"]:
        best = max(best, part_one(open_valves, mins_remaining - 1, valve))

    if curr_valve not in open_valves and curr_valve_state["rate"] > 0 and mins_remaining > 0:
        open_valves = set(open_valves)
        open_valves.add(curr_valve)
        mins_remaining -= 1
        new_sum = mins_remaining * curr_valve_state["rate"]

        for valve in curr_valve_state["valves"]:
            best = max(best, new_sum + part_one(frozenset(open_valves), mins_remaining - 1, valve))

    return best


@functools.cache
def part_two(open_valves: frozenset, mins_remaining: int, curr_valve: str) -> int:
    """
    Part 2 Solution:
    Just do part one, then do it again once done to simulate the elephant (this is a naive solution, but it works)

    :param open_valves: Set of valves that have been opened and are releasing pressure each minute
    :param mins_remaining: Number of minutes remaining in the current function call (used recursively)
    :param curr_valve: Curr valve moved to in this function call (used recursively)
    :return: int - Most pressure that can be released
    """
    # Base Case: No time left, so cannot open more valves - instead, simulate elephant with the same 26 mins as well
    if mins_remaining <= 0:
        return part_one(open_valves, 26, "AA")

    best = 0
    curr_valve_state = STATE[curr_valve]

    for valve in curr_valve_state["valves"]:
        best = max(best, part_two(open_valves, mins_remaining - 1, valve))

    if curr_valve not in open_valves and curr_valve_state["rate"] > 0 and mins_remaining > 0:
        open_valves = set(open_valves)
        open_valves.add(curr_valve)
        mins_remaining -= 1
        new_sum = mins_remaining * curr_valve_state["rate"]

        for valve in curr_valve_state["valves"]:
            best = max(best, new_sum + part_two(frozenset(open_valves), mins_remaining - 1, valve))

    return best


def main():
    read_input("day16-input.txt")

    part1_sol = part_one(frozenset(), 30, 'AA')  # At start, we are in the room with 'AA' valve with 30 minutes to go
    print(f"Work out the steps to release the most pressure in 30 minutes."
          f"\nWhat is the most pressure you can release?"
          f"\nAnswer: {part1_sol}")

    part2_sol = part_two(frozenset(), 26, 'AA')  # At elephant training, in the room with 'AA' valve with 26 mins left
    print(f"With you and an elephant working together for 26 minutes, what is the most pressure you could release?"
          f"\nAnswer: {part2_sol}")


if __name__ == "__main__":
    main()

