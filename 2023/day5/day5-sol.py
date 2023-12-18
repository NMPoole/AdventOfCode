#######################################################################################################################
# Advent of Code 2023 - Day 5
#######################################################################################################################

def solve(groups, seed_interpreter):
    seed_ranges = seed_interpreter(list(map(int, groups[0].split()[1:])))

    for group in groups[1:]:
        step_mapping = [tuple(map(int, line.split())) for line in group.splitlines()[1:]]
        new_ranges = []

        for start, r_len in seed_ranges:
            while r_len != 0:
                found_match = False
                best_dist = r_len

                for dst, src, length in step_mapping:
                    if src <= start < src + length:
                        # Found a match
                        off = start - src
                        rem_length = min(length - off, r_len)
                        new_ranges.append((dst+off, rem_length))
                        start += rem_length
                        r_len -= rem_length
                        found_match = True
                        break
                    else:
                        if start < src:
                            best_dist = min(src - start, best_dist)

                if not found_match:
                    handling_len = min(best_dist, r_len)
                    new_ranges.append((start, handling_len))
                    start += handling_len
                    r_len -= handling_len

        seed_ranges = new_ranges

    return min(start for start, length in seed_ranges)


def calc_part1(groups):
    return solve(groups, lambda nums : [(n, 1) for n in nums])


def calc_part2(groups):
    return solve(groups, lambda nums : list(zip(nums[::2], nums[1::2])))


if __name__ == '__main__':
    input_groups = open('day5-input.txt').read().split('\n\n')

    part1_sol = calc_part1(input_groups)
    print(f"What is the lowest location number that corresponds to any of the initial seed numbers?"
          f"\nAnswer: {part1_sol}")

    part2_sol = calc_part2(input_groups)
    print(f"What is the lowest location number that corresponds to any of the initial seed numbers?"
          f"\nAnswer: {part2_sol}", )