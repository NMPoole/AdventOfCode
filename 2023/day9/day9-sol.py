#######################################################################################################################
# Advent of Code 2023 - Day 8
#######################################################################################################################

def calc_part1(lines):
    total = 0
    for line in lines:
        report = [[int(x) for x in line.split()]]
        while len([n for n in report[-1] if n == 0]) < len(report[-1]):
            report.append([report[-1][i + 1] - report[-1][i] for i in range(len(report[-1]) - 1)])
        for i in range(len(report) - 2, -1, -1):
            report[i].append(report[i][-1] + report[i + 1][-1])
        total += report[0][-1]

    return total


def calc_part2(lines):
    total = 0
    for line in lines:
        report = [[int(x) for x in line.split()]]
        while len([n for n in report[-1] if n == 0]) < len(report[-1]):
            report.append([report[-1][i + 1] - report[-1][i] for i in range(len(report[-1]) - 1)])
        for i in range(len(report) - 2, -1, -1):
            report[i] = [report[i][0] - report[i + 1][0]] + report[i]
        total += report[0][0]

    return total


if __name__ == "__main__":
    input_lines = open("day9-input.txt").readlines()

    part1_sol = calc_part1(input_lines)
    print(f"What is the sum of these extrapolated values?"
          f"\nAnswer: {part1_sol}")

    part2_sol = calc_part2(input_lines)
    print(f"What is the sum of these extrapolated values?"
          f"\nAnswer: {part2_sol}")

