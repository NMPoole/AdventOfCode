#######################################################################################################################
# Advent of Code 2022 - Day 1
#######################################################################################################################

data = open('./day1/day1-input.txt', 'r')  # Read data from input file

elves_calories = data.read().strip().split('\n\n')  # Elves calorie data separated by blank lines
calories = []

# For each elf, total their calorie counts (which are separated on new lines) and add to ordered list
for elf in elves_calories:
    meals = elf.split('\n')
    meals = [eval(i) for i in meals]
    calories.append(sum(meals))

# Elf with most calories is simply max total in the list
part1 = max(calories)
print(f'Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?'
      f'\nAnswer: {part1}', )

# Total calories of top 3 Elves is simply total of 3 largest items (done via sort first)
calories = sorted(calories, reverse=True)
part2 = sum(calories[0:3:1])
print(f'Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?'
      f'\nAnswer: {part2}')
