#######################################################################################################################
# Advent of Code 2022 - Day 5
#######################################################################################################################

from copy import deepcopy
import re


def main():
    """
    We have stacks of crates. First block of input data shows stack configuration, e.g.
                [D]
            [N] [C]
            [Z] [M] [P]
             1   2   3
    We have instructions for rearranging crates.  E.g. 'move 3 from 1 to 3'

    Part 1:
    Our CrateMover 9000 moves one crate at the time, from the end of one stack to the end of another.
    What crates will be at the top of each stack, after following the instructions?
    - Solution:
      - Split the instructions into two blocks: crate config, and instructions.
        - For config, first reverse the order, count how many stacks, and then parse with regex.
      - Process each instruction, popping off the end of the source stack as many times as required, and appending to
        the target stack.

    Part 2:
    Our CrateMover 9001 moves multiple crates at a time, and puts them in the new stack in the same order that they
    were lifted. What crates will be at the top of each stack, after following the instructions?
    - Solution:
      - The same, except now we can slice n items off the end of the source stack, rather than popping one at a time.
      - Because we're now adding a list (slice) to the target stack, we need to use extend, not append.
    """
    with open("./day5-input.txt", mode="rt") as input_file:
        stack_data, instructions = input_file.read().split("\n\n")

    stacks = process_stack_data(stack_data.splitlines())
    movements = read_instructions(instructions.splitlines())

    # Part 1:
    part1_stack = deepcopy(stacks)  # Make a copy - need to reset the stack for Part 2
    for how_many, from_where, to_where in movements:
        for _ in range(how_many):  # Pop items off the end, for how_many times
            part1_stack[to_where].append(part1_stack[from_where].pop())

    stack_message = "".join(a_stack[-1] for a_stack in part1_stack)
    print(f"After the rearrangement procedure completes, what crate ends up on top of each stack?"
          f"\nAnswer: {stack_message}")

    # Part 2:
    for how_many, from_where, to_where in movements:
        stacks[to_where].extend(stacks[from_where][-how_many:])  # Slice items off the end and move to the target stack
        stacks[from_where][-how_many:] = []  # ...And then delete the items

    stack_message = "".join(a_stack[-1] for a_stack in stacks)
    print(f"Before the rearrangement process finishes, update your simulation so that the Elves know where they should "
          f"stand to be ready to unload the final supplies."
          f"\nAfter the rearrangement procedure completes, what crate ends up on top of each stack?"
          f"\nAnswer: {stack_message}")


def process_stack_data(stack_data: list[str]) -> list[list]:
    """
    Data looks like...
            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

    Return: [['Z', 'N'], ['M', 'C', 'D'], ['P']]
    """
    stack_width = 4
    p = re.compile(r"[A-Z]")
    stack_data = stack_data[::-1]  # Reverse it, so we've got the stack numbers at the top

    num_stacks = len(stack_data[0].split())

    stacks = []
    for stack_num in range(num_stacks):
        stacks.append([])

    # Proces the stacks
    for stack_row in stack_data[1:]:  # Starting at the row of crates
        for stack_num in range(num_stacks):
            match = p.search(stack_row[stack_num * stack_width:(stack_num + 1) * stack_width])
            if match:
                stacks[stack_num].append(match.group())

    return stacks


def read_instructions(instructions: list[str]) -> list[tuple[int, int, int]]:
    """
    Instructions look like: 'move 3 from 8 to 6'

    Return: [(3, 8, 6), ...]
    """
    p = re.compile(r"move (\d+) from (\d+) to (\d+)")

    movements = []
    for line in instructions:
        how_many, from_where, to_where = list(map(int, p.findall(line)[0]))
        from_where -= 1  # Needs to be 0-indexed
        to_where -= 1  # Needs to be 0-indexed
        movements.append((how_many, from_where, to_where))

    return movements


if __name__ == "__main__":
    main()
