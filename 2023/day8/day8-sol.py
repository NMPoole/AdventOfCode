#######################################################################################################################
# Advent of Code 2023 - Day 8
#######################################################################################################################
import math


def parse_input(file_name: str):
    input_data = [x for x in open(file_name).read().strip().split('\n\n')]
    instructions = list(input_data[0])

    connections = {}
    for labeled_node in input_data[1].split("\n"):
        a = labeled_node.split(" ")[0]
        b = labeled_node.split("(")[1].split(",")[0]
        c = labeled_node.split(" ")[3].split(")")[0]
        connections[a] = (b, c)

    return instructions, connections


def calc_part1(inst, conn):
    pos = 'AAA'
    idx = 0
    while pos != 'ZZZ':
        d = inst[idx % len(inst)]
        pos = conn[pos][0 if d == 'L' else 1]
        idx += 1

    return idx


def calc_part2(inst, conn):
    def solvesteps(start):
        pos = start
        idx = 0
        while not pos.endswith('Z'):
            d = inst[idx % len(inst)]
            pos = conn[pos][0 if d == 'L' else 1]
            idx += 1
        return idx

    ret = 1
    for start in connections:
        if start.endswith('A'):
            ret = math.lcm(ret, solvesteps(start))

    return ret

if __name__ == "__main__":
    instructions, connections = parse_input("day8-input.txt")

    # Part 1:
    part1_sol = calc_part1(instructions, connections)
    print(f"How many steps are required to reach ZZZ?"
          f"\nAnswer: {part1_sol}")

    # Part 2:
    part2_sol = calc_part2(instructions, connections)
    print(f"How many steps does it take before you're only on nodes that end with Z?"
          f"\nAnswer: {part2_sol}")