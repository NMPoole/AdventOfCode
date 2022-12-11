#######################################################################################################################
# Advent of Code 2022 - Day 11
#######################################################################################################################

from collections import Counter
import copy
import math
import operator
import re


class Monkey:
    """
    Object-oriented implementation for Monkey behaviour:
    """

    def __init__(self, index: int, items: list, worry_operation: str, test_divisor: int, throw_to: list) -> None:
        """
        Initialise Monkey object

        :param index: Index assigned to this monkey (e.g., 0)
        :param items: Items available for this monkey to inspect (e.g. [79, 98])
        :param worry_operation: Operation to change worry level when monkey inspects item (e.g. old * 19)
        :param test_divisor: Divisor to test worry level divisibility - determines monkey to throw to (e.g. 13)
        :param throw_to: Monkeys to throw to for a True or False test result respectively (e.g. [2, 3])
        """
        self.index = index
        self.items = items
        self.worry_operation = worry_operation
        self.test_divisor = test_divisor
        self.throw_to = throw_to
        self.inspect_count = 0  # Number of times this monkey has performed an inspection

    def add_item(self, item: int) -> None:
        """
        Given an item, represented as a worry level integer, add said item to the end of this monkey's item list

        :param item: Item to add
        """
        self.items.append(item)

    def has_items(self) -> bool:
        """
        Return whether this monkey still has items to inspect

        :return: bool - True if items is non-empty, False otherwise
        """
        return len(self.items) != 0

    def inspect(self, relief: bool = True, lcm: int = None) -> int:
        """
        Inspect the next item in the list, which causes this monkey's worry level to go up, as given by worry_operation
        If relief enabled, then reduce this monkey's worry level by // 3.
        Then, work out which monkey to throw to by dividing by a divisor as a test

        Part 2 Change: Relief is disabled and worry level can get VERY LARGE!
        - We can significantly reduce this number by using the LCM trick.
        """
        self.inspect_count += 1

        # Replace references to 'old' in the operation with the current item being inspected (always the first)
        worry_op = self.worry_operation.replace("old", str(self.items[0]))

        # Apply worry operation
        first_operand, op, second_operand = re.findall(r"(\w+) (.) (\w+)", worry_op)[0]
        ops_dict = {
            "+": operator.add,
            "*": operator.mul
        }
        self.items[0] = ops_dict[op](int(first_operand), int(second_operand))

        # Relief - rule = divide by three and round down
        if relief:
            self.items[0] //= 3

        # Apply LCM trick (in part 2) to prevent worry levels from exploding
        if lcm:
            self.items[0] %= lcm

        # Return monkey to throw to based on the test condition (i.e., is worry level divisible by self.divisor)
        return self.throw_to[0] if self.items[0] % self.test_divisor == 0 else self.throw_to[1]

    def throw_item(self, other) -> None:
        """
        Given a monkey, other, to throw to, remove the current item from this monkey and give it to other

        :param other: Monkey object to throw the currently inspected item to (i.e., first item in self.items)
        """
        other.add_item(self.items.pop(0))

    def __repr__(self) -> str:
        """
        Represent this monkey object with custom string format showing ID, Items, and Inspection Count

        :return: Formatted string as described
        """
        return f"Monkey: (ID={self.index}, Start Items={self.items}, Inspect Count={self.inspect_count})"


def execute_rounds(monkeys: dict[int, Monkey], num_rounds: int, relief: bool = True, lcm: int = None) -> int:
    """
    Execute required number of rounds:
    Iterate over the desired number of rounds
    Each round involves iterating over every monkey, with each monkey inspecting and acting on its items in order

    :param monkeys: Dictionary of monkey indexes to corresponding monkey objects
    :param num_rounds: Number of rounds to execute
    :param relief: Whether relief is applied after a monkey has inspected an item
    :param lcm: Lowest common multiple of all test divisors used across all monkeys (i.e., applying LCM trick)
    :return int - 'Monkey Business' = product of the top two inspection counts
    """
    for _ in range(num_rounds):
        for monkey in monkeys.values():  # Iterate through monkeys in order
            while monkey.has_items():  # Monkey inspects and throws until it has no more items
                to_monkey_index = monkey.inspect(relief=relief, lcm=lcm)
                to_monkey = monkeys[to_monkey_index]
                monkey.throw_item(to_monkey)

    # Get the two monkeys that have inspected the most
    monkey_inspect = Counter({monkey.index: monkey.inspect_count for monkey in monkeys.values()})
    two_most_common = monkey_inspect.most_common(2)
    monkey_business = two_most_common[0][1] * two_most_common[1][1]
    return monkey_business


def parse_input(data: str) -> dict[int, Monkey]:
    """
    Given an input string containing the monkeys configuration data, parse said data into Monkey objects for use

    :param data: String containing monkey configuration data to parse
    :return: dict[int, Monkey] - Dictionary linking monkey indexes to corresponding parsed monkey objects
    """
    monkey_configs = data.split("\n\n")
    monkeys = {}

    for curr_monkey_config in monkey_configs:

        monkey_id, items, worry_op, divisor, to_monkey_true, to_monkey_false = None, None, None, None, None, None

        for line in curr_monkey_config.splitlines():  # Parse config lines for current monkey config
            if line.startswith("Monkey"):
                monkey_id = int(re.findall(r"(\d+)", line)[0])
            if "items:" in line:
                items = list(map(int, re.findall(r"(\d+)", line)))
            if "Operation:" in line:
                worry_op = line.split("=")[-1].strip()
            if "Test:" in line:
                divisor = int(re.findall(r"\d+", line)[0])
            if "true:" in line:
                to_monkey_true = int(re.findall(r"\d+", line)[0])
            if "false:" in line:
                to_monkey_false = int(re.findall(r"\d+", line)[0])

        # Create monkey object using parsed lines
        monkey = Monkey(
            index=monkey_id,
            items=items,
            worry_operation=worry_op,
            test_divisor=divisor,
            throw_to=[to_monkey_true, to_monkey_false]
        )

        # Add current monkey to dict of all monkeys and move on
        monkeys[monkey_id] = monkey

    return monkeys


def main():
    """
    Monkeys have my stuff! They each have a number of my items...
    - The monkeys are throwing my items to each other
    - The input data gives tells us how worried we are about each item
    - The input data specifies the rules for how a monkey inspects each item in order, how our worry score is affected,
        and then which other monkey the item gets thrown to
    - A round = each monkey plays in order with each monkey inspecting and throwing each item, in order

    Part 1 Solution:
    Monkey business = the product of this count from the two monkeys with the greatest count
    Goal is to determine monkey business after 20 rounds
    - Execute 20 rounds - iterating through each monkey, with each inspecting and throwing all its items
    - Determine the final inspect_count for each monkey and return the product of the two largest counts

    Part 2 Solution:
    Item worry level is no longer reduced after inspection
    Goal is to calculate monkey business for 10000 rounds
    - The problem is that with the Part 1 solution, the worry scores get very, very BIG
    - This solution is going to take too long - we need a way to keep the worry scores smaller
    - For this, use: A ≡ B (mod C) - i.e., A is congruent to B mod C meaning A belongs in the same remainder bucket as B
        Numbers are "congruent modulo n" if they have the same remainder after division
            If a ≡ b (mod M) and b = d (mod m), then a ≡ d (mod m)
            If a ≡ b (mod m), then a + c ≡ b + c (mod m)
            If a ≡ b (mod m), then ax ≡ bx (mod mx)
        So, modulo congruence is preserved with addition and multiplication (used in our worry operation)
        And we're not dividing anymore, which would break congruence
        So, we only need to maintain a number which preserves the remainder, not the actual worry score
        So, we can just store % w (mod n), and for n we can use the LCM of all our divisors.

    NOTE: Credit for part 2 solution to 'derailed-dash' for explanation of applying congruence and LCM trick
    - https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2022/d11_monkey_in_the_middle/monkey.py
    """
    with open("day11-input.txt", mode="rt") as f:
        data = f.read()

    monkeys = parse_input(data)

    # Part 1:
    monkey_business = execute_rounds(copy.deepcopy(monkeys), 20)  # Create copy so same parse usable for Parts 1 and 2
    print(f"Figure out which monkeys to chase by counting how many items they inspect over 20 rounds."
          f"\nWhat is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?"
          f"\nAnswer: {monkey_business}")

    # Part 2:
    # Here, the LCM is actually the product of these numbers, since they are all prime - in general, we want to use LCM
    lcm = math.lcm(*[monkey.test_divisor for monkey in monkeys.values()])
    monkey_business = execute_rounds(monkeys, 10000, relief=False, lcm=lcm)
    print(f"Worry levels are no longer divided by three after each item is inspected; "
          f"You'll need to find another way to keep your worry levels manageable."
          f"\nStarting again from the initial state in your puzzle input, "
          f"what is the level of monkey business after 10000 rounds?"
          f"\nAnswer: {monkey_business}")


if __name__ == "__main__":
    main()
