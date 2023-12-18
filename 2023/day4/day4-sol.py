#######################################################################################################################
# Advent of Code 2023 - Day 4
#######################################################################################################################
def parse_nums_from_string(str_input: str) -> set[int]:
    return { int(x) for x in str_input.split(' ') if x }


def calc_part1(card_lst: list[str]) -> int:
    points_sum = 0

    for card_index, card in enumerate(card_lst):
        winning_number_lst, guessed_number_lst = [parse_nums_from_string(x) for x in card.split(': ')[1].split(' | ')]
        card_winning_count = len(guessed_number_lst.intersection(winning_number_lst))

        points_sum += int(1 * pow(2, card_winning_count - 1))

    return points_sum


def calc_part2(card_lst: list[str]) -> int:
    card_count_lst = [1 for _ in range(len(card_lst))]

    for card_index, card in enumerate(card_lst):
        winning_number_lst, guessed_number_lst = [parse_nums_from_string(x) for x in card.split(': ')[1].split(' | ')]
        card_winning_count = len(guessed_number_lst.intersection(winning_number_lst))

        for x in range(card_index + 1, card_index + card_winning_count + 1):
            card_count_lst[x] += 1 * card_count_lst[card_index]

    return sum(card_count_lst)


if __name__ == '__main__':
    card_list = open('day4-input.txt').readlines()

    part1_sol = calc_part1(card_list)
    print(f'How many points are they worth in total?'
          f'\nAnswer: {part1_sol}')

    part2_sol = calc_part2(card_list)
    print(f'Including the original set of scratchcards, how many total scratchcards do you end up with?'
          f'\nAnswer: {part2_sol}')