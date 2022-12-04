#######################################################################################################################
# Advent of Code 2022 - Day 2
#######################################################################################################################

shape_score_map = {  # Scores attained based on shape played
    "X": 1, "A": 1,
    "Y": 2, "B": 2,
    "Z": 3, "C": 3
}

outcome_map = {  # Scores attained based on round outcome: what they play, what we play -> outcome score
    ("A", "X"): 3, ("B", "Y"): 3, ("C", "Z"): 3,
    ("A", "Y"): 6, ("B", "Z"): 6, ("C", "X"): 6,
    ("A", "Z"): 0, ("B", "X"): 0, ("C", "Y"): 0,
}

# Inverse of the outcome map such that: what they play, outcome score -> what we play
inv_outcome_map = {(k[0], v): k[1] for k, v in outcome_map.items()}

strategy = {  # (Part 2) Scores based on round outcome, where: X -> loss, Y -> draw, Z -> win
    "X": 0,
    "Y": 3,
    "Z": 6
}

part1_total_score = 0
part2_total_score = 0

with open("day2-input.txt") as rounds:  # Load the rounds of the game
    for curr_round in rounds:
        # Getting what they play and what we play (part 1) / desired outcome (part 2)
        they_play, response = curr_round.strip().split(" ")
        # Adding shape score and outcome score, respectively
        part1_total_score += shape_score_map[response] + outcome_map[(they_play, response)]
        part2_total_score += shape_score_map[inv_outcome_map[(they_play, strategy[response])]] + strategy[response]

print(f"What would your total score be if everything goes exactly according to your strategy guide?"
      f"\nAnswer: {part1_total_score}")

print(f"Following the Elf's instructions for the second column, what would your total score be if everything goes "
      f"exactly according to your strategy guide?"
      f"\nAnswer: {part2_total_score}")


