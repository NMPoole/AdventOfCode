#######################################################################################################################
# Advent of Code 2023 - Day 6
#######################################################################################################################
def common(times, distances):
    n = 1
    for time, distance in zip(times, distances):
        margin = 0
        for hold in range(time):
            if hold * (time - hold) > distance:
                margin += 1
        n *= margin

    return n


if __name__ == '__main__':
    input_data = open('day6-input.txt').readlines()

    part1_times, part1_distances = [list(map(int, line.split(":")[1].split())) for line in input_data]
    part1_sol = common(part1_times, part1_distances)
    print(f"What do you get if you multiply these numbers together?"
          f"\nAnswer: {part1_sol}")

    part2_times, part2_distances = [list(map(int, ["".join(line.split(":")[1].split())])) for line in input_data]
    part2_sol = common(part2_times, part2_distances)
    print(f"How many ways can you beat the record in this one much longer race?"
          f"\nAnswer: {part2_sol}")
