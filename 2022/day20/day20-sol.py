#######################################################################################################################
# Advent of Code 2022 - Day 20
#######################################################################################################################

from collections import deque


DECR_KEY = 811589153


def solve(data: list[str], is_part2: bool = False) -> int:
    """
    Mix the numbers given in data having applied a decryption key, and sum the co-ordinates given by the 1000th, 2000th,
    and 3000th numbers after the final position of '0' within the list

    :param data: List of numbers as strings which are to be mixed
    :param is_part2: Whether this method is executing for Part 2 or not
    :return: int - Sum of three calculated co-ordinates via mixing decryption
    """
    # Multiply each number by the decryption key before - this will produce the actual list of numbers to mix
    # There is no decryption key in part 1, so multiply by idempotent 1 in this case
    data = deque([*map(lambda n: int(n) * (DECR_KEY if is_part2 else 1), data)])

    current_value = 0
    length = len(data)
    indexes = deque(range(0, length))

    # In part 2, need to mix the list of numbers ten times
    for _ in range(10 if is_part2 else 1):
        # Number mixing order does not change; numbers moved in the order they appeared in the original, pre-mixed list
        for idx in range(length):
            position = indexes.index(idx)

            # Mix list of numbers and list of indexes tracking numbers equally...
            # ...so we can find next number according to the original ordering of the list
            for deq in [data, indexes]:
                deq.rotate(position * -1)
                local_value = deq.popleft()

                if deq == data:
                    current_value = local_value

                deq.rotate(current_value * -1)
                deq.appendleft(local_value)

    zero = data.index(0)  # Position of the 0 after mixing

    # Co-ordinates are the 1000th, 2000th, and 3000th numbers after the 0 in the mixed list of numbers
    a, b, c = (data[(zero + 1000) % (len(data))],
               data[(zero + 2000) % (len(data))],
               data[(zero + 3000) % (len(data))])

    return sum([a,b,c]) # Question requires the sum of the three numbers that form the grove coordinates


def main() -> None:
    """
    Read the input from file, then execute Parts 1 and 2
    """
    # Read input from file:
    with open("day20-input.txt") as f:
        data = f.read().splitlines()

    # Part 1:
    part1_sol = solve(data)
    print(f"Mix your encrypted file exactly once."
          f"\nWhat is the sum of the three numbers that form the grove coordinates?"
          f"\nAnswer: {part1_sol}")

    # Part 2:
    part2_sol = solve(data, is_part2=True)
    print(f"Apply the decryption key and mix your encrypted file ten times."
          f"\nWhat is the sum of the three numbers that form the grove coordinates?"
          f"\nAnswer: {part2_sol}")


if __name__ == "__main__":
    main()
