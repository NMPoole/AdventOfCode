#######################################################################################################################
# Advent of Code 2023 - Day 1
#######################################################################################################################
def calc_part1(data: list) -> int:
    """
    Part 1 Solution: Simply find first and last digits characters in each line, form a two-digit number, and add to total.
    """
    lines_num_chars = []
    for line in data:
        line_num_chars = []
        for char in line:
            if '0' <= char <= '9':
                line_num_chars.append(int(char))
        lines_num_chars.append(line_num_chars)

    total = 0
    for result in lines_num_chars:
        total += (10 * result[0])  # Will be a single two-digit number, so add 10x first digit in line and add last digit.
        total += result[-1]

    return total


def calc_part2(data: list) -> int:
    """
    Part 2 Solution: Dirty solution - inject digit into word and use Part 1 solution.
    """
    new_data = []
    for line in data:
        line = line.replace('one', 'o1ne')
        line = line.replace('two', 't2wo')
        line = line.replace('three', 't3hree')
        line = line.replace('four', 'f4our')
        line = line.replace('five', 'f5ive')
        line = line.replace('six', 's6ix')
        line = line.replace('seven', 's7even')
        line = line.replace('eight', 'e8ight')
        line = line.replace('nine', 'n9ine')
        line = line.replace('zero', 'z0ero')
        new_data.append(line)
    return calc_part1(new_data)


if __name__ == "__main__":
    input_data = open('day1-input.txt').readlines()  # Read data from input file.

    part1_sol = calc_part1(input_data)
    print(f'What is the sum of all of the calibration values?'
          f'\nAnswer: {part1_sol}')

    part2_sol = calc_part2(input_data)
    print(f'What is the sum of all of the calibration values?'
          f'\nAnswer: {part2_sol}')