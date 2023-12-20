#######################################################################################################################
# Advent of Code 2023 - Day 7
#######################################################################################################################
import collections


def calc_hand(curr_hand, is_part1):
    if is_part1:
        curr_hand = curr_hand.replace('J', 'X')

    h2 = ['J23456789TXQKA'.index(i) for i in curr_hand]
    ts = []
    for rank in '23456789TQKA':
        c = collections.Counter(curr_hand.replace('J', rank))
        p = tuple(sorted(c.values()))
        t = [(1,1,1,1,1),(1,1,1,2),(1,2,2),(1,1,3),(2,3),(1,4),(5,)].index(p)
        ts.append(t)

    return max(ts), *h2


if __name__ == "__main__":
    hands_data = [line.split() for line in (open("day7-input.txt").readlines())]

    # Part 1:
    hands = sorted(
        (calc_hand(curr_hand, True), int(curr_bid))
        for curr_hand, curr_bid in hands_data
    )
    part1_t = 0
    for i, (_, bid) in enumerate(hands):
        part1_t += i * bid + bid

    print(f"What are the total winnings?"
          f"\nAnswer: {part1_t}")

    # Part 2:
    hands = sorted(
        (calc_hand(curr_hand, False), int(curr_bid))
        for curr_hand, curr_bid in hands_data
    )
    part2_t = 0
    for i, (_, bid) in enumerate(hands):
        part2_t += i * bid + bid

    print(f"Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?"
          f"\nAnswer: {part2_t}")