#######################################################################################################################
# Advent of Code 2022 - Day 6
#######################################################################################################################
from collections import Counter

PACKET_MARKER_SIZE = 4  # Part 1: Number of distinct chars defining the start-of-packet marker
MSG_MARKER_SIZE = 14  # Part 2: Number of distinct chars defining the start-of-message marker


def main():
    """
    Part 1:
    Read the input stream. Report how many characters have been read when the last four chars are all different.
    - Solution:
      - Let distinct_char_size = 4
      - Process the data stream one char at a time and track the slice of the last distinct_char_size chars
      - Perform count of all chars in distinct_char_size. If they are all 1, then we have our goal

    Part 2:
    How many characters need to be processed before the first start-of-message marker is detected?
    Solution:
    - This is exactly the same as part 1, except distinct_char_size = 14
    """
    with open("day6-input.txt", mode="rt") as input_file:
        data = input_file.read()

    distinct_chars, curr_position = process_stream(data, PACKET_MARKER_SIZE)
    print(f"How many characters need to be processed before the first start-of-packet marker is detected?"
          f"\nAnswer: '{distinct_chars}' at {curr_position}")

    distinct_chars, curr_position = process_stream(data, MSG_MARKER_SIZE)
    print(f"How many characters need to be processed before the first start-of-message marker is detected?"
          f"\nAnswer: '{distinct_chars}' at {curr_position}")


def process_stream(data: str, distinct_char_size: int) -> tuple:
    """
    Process a string of data. Report char position when the last distinct_char_size chars are all different.

    Returns: Tuple - (distinct_chars, position) - meaning distinct_chars is the marker read just before position
    """
    last_size_chars = ""
    curr_position = 0

    for i, char in enumerate(data[distinct_char_size:]):
        # Start distinct_char_size chars in, get prev distinct_char_size chars, and advance one char each loop as window
        # E.g., distinct_char_size = 4, start at char 5, get prev 4 chars ('pqff'), then slide window a char each loop
        curr_position = i + distinct_char_size
        last_size_chars = data[curr_position - distinct_char_size:curr_position]

        # Count chars in last distinct_char_size chars and check for uniqueness
        char_counts = Counter(last_size_chars)
        if all(count == 1 for count in char_counts.values()):
            break

    return last_size_chars, curr_position


if __name__ == "__main__":
    main()
