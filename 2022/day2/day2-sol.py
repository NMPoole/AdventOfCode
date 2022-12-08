#######################################################################################################################
# Advent of Code 2022 - Day 2
#######################################################################################################################
from typing import List

# Scores attained based on shape played
SHAPE_SCORE_MAP = {
    "X": 1, "A": 1,
    "Y": 2, "B": 2,
    "Z": 3, "C": 3
}

# Scores attained based on round outcome: what they play, what we play -> outcome score
OUTCOME_MAP = {
    ("A", "X"): 3, ("B", "Y"): 3, ("C", "Z"): 3,
    ("A", "Y"): 6, ("B", "Z"): 6, ("C", "X"): 6,
    ("A", "Z"): 0, ("B", "X"): 0, ("C", "Y"): 0,
}

# Inverse of the outcome map such that: what they play, outcome score -> what we play
INV_OUTCOME_MAP = {(k[0], v): k[1] for k, v in OUTCOME_MAP.items()}

# (Part 2) Scores based on round outcome, where: X -> loss, Y -> draw, Z -> win
STRATEGY = {
    "X": 0,
    "Y": 3,
    "Z": 6
}


def part1_solution(rounds: List[str]) -> int:
    """
    Part 1 Solution: Calculate total of shape and outcomes scores for each round
    The 'letters' of the round are interpreted as what they play vs what we play

    :param rounds: List of strings, with each string representing a round of Rock, Paper, Scissors
    :return: int - Total score attained from the round outcomes as interpreted by part 1
    """
    score = 0

    for curr_round in rounds:
        they_play, we_play = curr_round.strip().split(" ")  # Getting what they play and what we play
        score += SHAPE_SCORE_MAP[we_play] + OUTCOME_MAP[(they_play, we_play)]  # Adding shape score and outcome score

    return score


def part2_solution(rounds: List[str]) -> int:
    """
    Part 2 Solution: Calculate total of shape and outcomes scores for each round
    The 'letters' of the round are interpreted as what they play vs what the round outcome should be

    :param rounds: List of strings, with each string representing a round of Rock, Paper, Scissors
    :return: int - Total score attained from the round outcomes as interpreted by part 2
    """
    score = 0

    for curr_round in rounds:
        they_play, round_outcome = curr_round.strip().split(" ")  # Getting what they play and round outcome
        # Adding shape score and outcome score, respectively
        score += SHAPE_SCORE_MAP[INV_OUTCOME_MAP[(they_play, STRATEGY[round_outcome])]] + STRATEGY[round_outcome]

    return score


def main():
    """
    Advent of Code - Day 2 Solution
    NOTE: 'X' or 'A' = Rock, 'Y' or 'B' = Paper, 'Z' or 'C' = Scissors
    """
    with open("day2-input.txt") as rounds_file:
        rounds = rounds_file.read().split('\n')  # Load the rounds of the game

    part1_sol = part1_solution(rounds)
    print(f"What would your total score be if everything goes exactly according to your strategy guide?"
          f"\nAnswer: {part1_sol}")

    part2_sol = part2_solution(rounds)
    print(f"Following the Elf's instructions for the second column, what would your total score be if everything goes "
          f"exactly according to your strategy guide?"
          f"\nAnswer: {part2_sol}")


if __name__ == "__main__":
    main()
