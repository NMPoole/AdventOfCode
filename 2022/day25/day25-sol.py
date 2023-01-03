#######################################################################################################################
# Advent of Code 2022 - Day 25
#######################################################################################################################

snafu_to_dec = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

int_to_snafu = {v: k for k, v in snafu_to_dec.items()}


def main():
    """
    Determine the sum of the fuel requirements of all hot air balloons
    Numbers in the snafu system; it's base-5: '2' = 2, '1' = 1, '0' = 0, '-' = -1, '=' = -2
    So, 1=-0-2

    Part 1 Solution:
    Add up all the snafu numbers, and represent the total in snafu format.
    Solution:
    - Add snafu numbers column by column, from right to left, just like any other base.
    - For column addition: convert to decimal, add up, and determine any carry to the left column.
      - We need to carry-over, if the current column adds up to < -2, or > 2.
        If current col > 2: add one carry-over unit and subtract 5 in the current column.
        If current col < -2: subtract one carry-over unit and add 5 in the current column.
      - Convert the current col back to snafu and store it.

    Part 2 Solution:
    - There is no part 2!
    """
    # Read Input:
    with open("day25-input.txt", mode="rt") as f:
        data = f.read().splitlines()

    # Part 1:
    part1_sol = add_snafu(data)
    print(f"The Elves are starting to get cold."
          f"\nWhat SNAFU number do you supply to Bob's console?"
          f"\nAnswer: '{part1_sol}'")


def add_snafu(nums: list[str]) -> str:
    """
    Add up snafu digits with column carry, just like any other base system
    All the input digits are in snafu format, so are passed as str
    Add up decimal values, calculate the carries, and convert the current column to snafu
    """
    max_cols = max(len(num) for num in nums)  # The longest digit in our input

    snafu_total_digits = []
    carry = 0
    for col in range(max_cols):  # Add up ALL numbers from right to left
        sum_col = carry  # Carry this number from previous column
        for num in nums:
            if col < len(num):  # We need to include this number in the column addition
                # Get the appropriate snafu digit from this number, convert to dec for addition
                sum_col += snafu_to_dec[num[len(num) - 1 - col]]

        carry = 0  # Reset carry
        while sum_col > 2:
            # Every unit carried is worth 5 from the column before
            carry += 1
            sum_col -= 5

        while sum_col < -2:  # Since snafu digits can be negative, we need to handle this
            carry -= 1
            sum_col += 5

        snafu_total_digits.append(int_to_snafu[sum_col])

    return ''.join(snafu_total_digits[::-1])


if __name__ == "__main__":
    main()
