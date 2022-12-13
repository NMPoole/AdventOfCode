#######################################################################################################################
# Advent of Code 2022 - Day 13
#######################################################################################################################

from __future__ import annotations
from ast import literal_eval  # Reading packet data made easy!


class Packet:
    """
    Packet is made up of a value which is either a list or an int - lists can contain other lists
    """

    def __init__(self, value: list | int) -> None:
        """
        Instantiate packet with a value that is either an int or a list

        :param value: Value to add to this packet
        """
        self.value = value

    def __lt__(self, other: Packet) -> bool:
        """
        Define the functionality of the less than (<) operator on Packets

        :param other: Packet to compare to this
        :return: bool - True if ordering conditions met between packets, False otherwise
        """
        # Base Case: Both are ints
        if isinstance(self.value, int) and isinstance(other.value, int):
            if self.value < other.value:
                return True
            if self.value > other.value:
                return False

        # Case: One val is int and one list
        if isinstance(self.value, int) and isinstance(other.value, list):
            new_item = Packet([self.value])  # Convert this int to list
            return new_item < other
        if isinstance(self.value, list) and isinstance(other.value, int):
            new_item = Packet([other.value])  # Convert other int to list
            return self < new_item

        # Case: Both vals are lists
        if isinstance(self.value, list) and isinstance(other.value, list):
            # Take each item and compare it - zip will stop when it reaches the end of either list
            compare_count = 0
            for val in zip(self.value, other.value):
                compare_count += 1
                if val[0] == val[1]:
                    continue  # If the same, continue to next item

                return Packet(val[0]) < Packet(val[1])

            # If here, then iterator terminated before finding a difference, so smaller list 'wins'
            return len(self.value) < len(other.value)

    def __repr__(self) -> str:
        """
        Packet is represented as a string simply by its value

        :return: Formatted string, as described
        """
        return str(self.value)


class Pair:
    """
    Contains two Packets: left and right
    """

    def __init__(self, left: Packet, right: Packet) -> None:
        """
        Initialise object for a pair of Packets

        :param left: First packet in pair
        :param right: Second packet in pair
        """
        self.left = left
        self.right = right

    def __repr__(self):
        """
        pair is represented as a string by simply showing its left and right values

        :return: Formatted string, as described
        """
        return f"Pair (l = '{self.left}', r = '{self.right}')"


def parse_packets_pairs(data: str) -> list[Pair]:
    """
    Parse packet data from string into list of Packet Pairs

    :param data: String containing all packet data to be parsed
    :return: list[Pair] - Parsed list of packet pairs
    """
    pairs: list[Pair] = []
    blocks = data.split("\n\n")  # Split into blocks (i.e., packet pairs)

    for block in blocks:
        lines = block.splitlines()

        left = Packet(literal_eval(lines[0]))
        right = Packet(literal_eval(lines[1]))
        pair = Pair(left, right)

        pairs.append(pair)

    return pairs


def parse_packets_all(data: str) -> list[Packet]:
    """
    Parse packet data into a list of all Packets

    :param data: String containing all packet data to be parsed
    :return: list[Packet] - Parsed list of packets
    """
    lines = data.splitlines()
    return [Packet(literal_eval(line)) for line in lines if line]


def main():
    """
    Input contains blocks, where each block is a pair.
    Each 'packet' in the pair is a list or an int. Lists can contain other lists.
    So clearly, recursion is going to be involved.

    Part 1 Solution:
    How many pairs are in the right order?
    - Read in each 'packet' using ast.literal_eval - this will automatically store as list or int
    - Create a Packet class that stores this item, and which implements __lt__ so that we can compare according to rules
      - The __lt__() method compares self with other
      - It is recursive:
        The base case is when we're comparing int values
        Otherwise, we're either converting an int on one side to list and comparing, or iterating a list and comparing
    - Finally, for each pair, compare and count how many times L < R

    Part 2 Solution:
    Ignore pairs and get all the packets
    Add two special 'divider' packets
    Then put all the packets in the right order, find the (1-indexed) index locations of the two divider packets
    Return the product of these two indexes
    - Our Item class is already sortable since we implemented __lt__().
    - So, read in all items, sort, and find the dividers.
    """
    with open("day13-input.txt", mode="rt") as f:
        data = f.read()

    # Part 1:
    pairs = parse_packets_pairs(data)

    right_order = []
    for i, pair in enumerate(pairs, start=1):
        if pair.left < pair.right:
            right_order.append(i)  # Only need ordering of packet indices, don't need to actually order packets

    part1_sol = sum(right_order)
    print(f"Determine which pairs of packets are already in the right order."
          f"\nWhat is the sum of the indices of those pairs?"
          f"\nAnswer: {part1_sol}")

    # Part 2
    all_packets = parse_packets_all(data)

    div_two, div_six = Packet([[2]]), Packet([[6]])  # Add divider packets, as required
    all_packets.append(div_two)
    all_packets.append(div_six)

    sorted_items = sorted(all_packets)  # Can sort all packets as the __lt__ operator is defined

    # Retrieve 1-indexed positions of the divider packets:
    loc_div_two = sorted_items.index(div_two) + 1
    loc_div_six = sorted_items.index(div_six) + 1

    part2_sol = loc_div_two * loc_div_six
    print(f"Organize all of the packets into the correct order."
          f"\nWhat is the decoder key for the distress signal?"
          f"\nAnswer: {part2_sol}")


if __name__ == '__main__':
    main()
