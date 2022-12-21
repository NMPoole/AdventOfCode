#######################################################################################################################
# Advent of Code 2022 - Day 21
#######################################################################################################################

from __future__ import annotations
import operator


OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv
}


def compute(monkeys: dict, monkey_name: str) -> int | None:
    """
    Compute the resulting yelled value for a given monkey

    :param monkeys: Dictionary of monkey names to their corresponding operations
    :param monkey_name: Name of the monkey being computed
    :return: int | None - What the monkey yells as a result of compute, None if cannot compute yet
    """
    yell = monkeys[monkey_name]

    # Base Case: Monkey has what it needs and can simply yell its number
    if yell is None or isinstance(yell, int):
        return yell

    # Recursive Step: Monkey needs to wait on the result of other monkeys yelling first
    m1, op, m2 = yell
    s1 = compute(monkeys, m1)
    s2 = compute(monkeys, m2)

    if s1 and s2:
        return OPS[op](s1, s2)
    else:
        return None


def solve(monkeys: dict, monkey_name: str, target: int) -> int:
    """
    Find the number 'humn' must yell to pass root's equality test

    :param monkeys: Dictionary of monkey names to their corresponding operations
    :param monkey_name: Name of the monkey being computed
    :param target: Used to force operators to match on both sides of root's equality check
    :return: int - Number we ('humn') must yell to pass root's equality test
    """
    yell = monkeys[monkey_name]

    # Base Case: Monkey has what it needs and can simply yell their number, or 'humn' simply yells target
    if isinstance(yell, int):
        return yell
    if yell is None:
        return target

    # Recursive Step(s):
    m1, op, m2 = yell
    s1 = compute(monkeys, m1)
    s2 = compute(monkeys, m2)

    if s1 is None:  # x op s2 = target
        if op == '+':
            return solve(monkeys, m1, target - s2)
        if op == '-':
            return solve(monkeys, m1, target + s2)
        if op == '*':
            return solve(monkeys, m1, target // s2)
        if op == '/':
            return solve(monkeys, m1, target * s2)

    elif s2 is None:  # s1 op x = target
        if op == '+':
            return solve(monkeys, m2, target - s1)
        if op == '-':
            return solve(monkeys, m2, -(target - s1))
        if op == '*':
            return solve(monkeys, m2, target // s1)
        if op == '/':
            return solve(monkeys, m2, s1 // target)


def main() -> None:
    """
    Advent of Code 2022 - Day 21 Solution:
    """
    monkeys = {}

    with open('day21-input.txt') as input_file:
        for line in input_file.readlines():
            line = line.strip().split(' ')
            key = line[0][:-1]
            if len(line) == 2:
                monkeys[key] = int(line[1])
            else:
                monkeys[key] = line[1:]

    # Part 1:
    part1_sol = compute(monkeys, 'root')
    print(f"What number will the monkey named root yell?"
          f"\nAnswer: {part1_sol}")

    # Part 2:
    monkeys['humn'] = None  # This is the number we have to yell, so its provided number is irrelevant
    monkeys['root'][1] = '-'  # Equality check the same as n - m == 0, so req. n = m on both sides of root's op

    part2_sol = solve(monkeys, 'root', 0)
    print(f"What number do you yell to pass root's equality test?"
          f"\nAnswer: {part2_sol}")


if __name__ == "__main__":
    main()
