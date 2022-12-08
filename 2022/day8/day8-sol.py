#######################################################################################################################
# Advent of Code 2022 - Day 8
#######################################################################################################################

def parse(input_str: str) -> tuple[int, int, dict]:
    """
    Parsing the grid of trees from the input string as a dictionary where co-ordinates (x, y) gives the corresponding
    tree's height

    :param input_str: String representing the grid of
    :return: tuple[int, int, dict] - width of the grid, height of the grid, and the grid
    """
    grid = {}
    i, j = -1, -1

    for i, line in enumerate(input_str.splitlines()):
        for j, height in enumerate(line):
            grid[i, j] = int(height)

    return i, j, grid


def directions(i: int, j: int, width: int, height: int):
    """
    Yield line of co-ordinates along each of the cardinal directions (N, E, S, W) from a given tree at (i, j) to edge

    :param i: Current location along width (i.e., x co-ordinate)
    :param j: Current location along height (i.e., y co-ordinate)
    :param width: The width of the grid
    :param height: The height of the grid
    :return: tuple[int, int] - Yields line of co-ordinates along one of cardinal directions
    """
    yield [(x, j) for x in range(i + 1, width + 1)]  # Right/East of tree
    yield [(x, j) for x in range(i - 1, -1, -1)]  # Left/West of tree
    yield [(i, x) for x in range(j + 1, height + 1)]  # Down/South of tree
    yield [(i, x) for x in range(j - 1, -1, -1)]  # Up/North of tree


def visible(i: int, j: int, width: int, height: int, grid: dict) -> bool:
    """
    Check along each cardinal direction (from tree to N, E, S, W edges) and check visibility

    :param i: Current location along width (i.e., x co-ordinate)
    :param j: Current location along height (i.e., y co-ordinate)
    :param width: The width of the grid
    :param height: The height of the grid
    :param grid: The grid of trees (height map)
    :return: bool - True if tree is visible from the edges, False otherwise
    """
    tree_height = grid[i, j]

    for line in directions(i, j, width, height):
        for tree in line:
            if grid[tree] >= tree_height:
                break
        else:
            return True

    return False


def scenic_score(i: int, j: int, width: int, height: int, grid: dict) -> int:
    """
    Calculate a given tree's scenic score by multiplying together its viewing distance in each of the four directions

    To measure the viewing distance from a given tree, look up, down, left, and right from that tree;
    stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration

    :param i: Current location along width (i.e., x co-ordinate)
    :param j: Current location along height (i.e., y co-ordinate)
    :param width: The width of the grid
    :param height: The height of the grid
    :param grid: The grid of trees (height map)
    :return: int - Scenic score for the given tree
    """
    tree_height = grid[i, j]
    score = 1  # Multiplicative identity

    for line in directions(i, j, width, height):
        distance = 0
        for tree in line:
            distance += 1
            if grid[tree] >= tree_height:
                break
        score *= distance

    return score


def part_one(width: int, height: int, grid: dict) -> int:
    """
    Part 1 Solution: The sum of all trees that are visible within the grid

    :param width: The width of the grid
    :param height: The height of the grid
    :param grid: The grid of trees (height map)
    :return: int - Sum of visible trees
    """
    return sum(visible(i, j, width, height, grid) for (i, j) in grid)


def part_two(width: int, height: int, grid: dict) -> int:
    """
    Part 2 Solution: The max scenic score of all trees within the grid

    :param width: The width of the grid
    :param height: The height of the grid
    :param grid: The grid of trees (height map)
    :return: int - Max scenic score
    """
    return max(scenic_score(i, j, width, height, grid) for (i, j) in grid)


if __name__ == "__main__":
    grid_width, grid_height, grid_dict = parse(open("day8-input.txt").read().strip())

    part1_sol = part_one(grid_width, grid_height, grid_dict)
    print(f"Consider your map; how many trees are visible from outside the grid?"
          f"\nAnswer: {part1_sol}")

    part2_sol = part_two(grid_width, grid_height, grid_dict)
    print(f"Consider each tree on your map. What is the highest scenic score possible for any tree?"
          f"\nAnswer: {part2_sol}")
