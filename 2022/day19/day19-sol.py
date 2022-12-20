#######################################################################################################################
# Advent of Code 2022 - Day 19
#######################################################################################################################

import math


class Blueprint:
    """
    Blueprint Class:
    """

    def __init__(self, blueprint: str) -> None:
        """
        Initialise a blueprint by passing in a blueprint config string to be parsed

        :param blueprint: Blueprint as string to parse info from
        """
        bp_id, robots = blueprint[10:-1].split(": ")

        self.id = int(bp_id)
        self.robots = {}

        for i, robot in enumerate(reversed(robots.split(". "))):
            typ, costs = robot[5:].split(" robot costs ")
            self.robots[typ] = {resource: int(cnt) for cnt, resource in
                                (cost.split(" ") for cost in costs.split(" and "))}

        self.maxes = {t: max(res.get(t, 0) for res in self.robots.values()) for t in self.robots.keys()}

    def __str__(self) -> str:
        """
        Represent a blueprint by its ID and its robots dict of build costs

        :return: str - Formatted string, as described
        """
        return f'Blueprint {self.id}: {self.robots}'

    def calc_max_geodes(self, minutes: int) -> int:
        """
        Find out the maximum number of geodes that can be recovered in the given amount of time (in minutes)
        Uses Depth-First-Search with short circuits to improve execution time

        :param minutes: Number of minutes available to farm geodes
        :return: int - Max number of geodes that can be farmed in the given amount of minutes
        """
        resources = {t: 0 for t in self.robots}
        robots = {t: int(t == "ore") for t in self.robots}

        q = [(minutes, resources, robots, None)]
        max_geodes = 0

        while len(q):
            time, resources, robots, last = q.pop()

            # We reached the end, consider the candidate for the max
            if time == 0:
                max_geodes = max(max_geodes, resources["geode"])
                continue

            # This path can never beat our current maximum geode count
            if max_geodes - resources["geode"] >= (time * (2 * robots["geode"] + time - 1)) // 2:
                continue

            time -= 1
            wait = False

            for robot_type, res_cost in self.robots.items():

                # If already generate enough resources for this type, don't need to create another robot to generate more
                if robot_type != "geode" and (robots[robot_type] * time) + resources[robot_type] > self.maxes[robot_type] * time:
                    continue

                # Don't create one of these if we could have created one last time
                if (last is None or last == robot_type) and all(v <= resources[t] - robots[t] for t, v in res_cost.items()):
                    continue

                # Don't have enough resources to create a robot if other robots did something, we could get enough resources, though
                if any(resources[t] < v for t, v in res_cost.items()):
                    wait = wait or all(robots[t] > 0 for t in res_cost.keys())
                    continue

                next_resources = {t: v + robots[t] - res_cost.get(t, 0) for t, v in resources.items()}
                next_robots = {t: v + int(t == robot_type) for t, v in robots.items()}

                q.append((time, next_resources, next_robots, robot_type))

            if wait:
                next_resources = {t: v + robots[t] for t, v in resources.items()}
                q.append((time, next_resources, robots, None))

        return max_geodes


def main() -> None:
    """
    Read the input regarding blueprint configurations from file, then execute Parts 1 and 2 using Depth-First-Search
    """
    # Read input from file:
    with open("day19-input.txt") as input_file:
        blueprints = [Blueprint(line.rstrip()) for line in input_file.readlines()]

    # Part 1:
    quality_levels = [bp.id * bp.calc_max_geodes(24) for bp in blueprints]
    sum_quality_levels = sum(quality_levels)
    print(f'Determine the quality level of each blueprint using the largest number of geodes it could produce in 24 minutes.'
          f'\nWhat do you get if you add up the quality level of all of the blueprints in your list?'
          f'\nAnswer: {sum_quality_levels}')

    # Part 2:
    geodes = [bp.calc_max_geodes(32) for bp in blueprints[:3]]
    geodes_prod = math.prod(geodes)
    print(f"Don't worry about quality levels; "
          f"instead, just determine the largest number of geodes you could open using each of the first three blueprints."
          f"\nWhat do you get if you multiply these numbers together?"
          f"\nAnswer: {geodes_prod}")


if __name__ == '__main__':
    main()
