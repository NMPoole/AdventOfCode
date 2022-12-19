#######################################################################################################################
# Advent of Code 2022 - Day 17
#######################################################################################################################

from __future__ import annotations
from dataclasses import dataclass
import itertools

SHAPES = {  # Tetris shapes the rocks resemble
    "HLINE": {(0, 0), (1, 0), (2, 0), (3, 0)},
    "PLUS": {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    "BACKWARDS_L": {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    "I": {(0, 0), (0, 1), (0, 2), (0, 3)},
    "SQUARE": {(0, 0), (1, 0), (0, 1), (1, 1)}
}

MOVE = {  # Directions of movement of Tetris rocks
    "<": (-1, 0),
    ">": (1, 0),
    "V": (0, -1)
}


@dataclass(frozen=True)
class Point:
    """
    Point with x,y coordinates that knows how to add a vector to create a new Point.
    """
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        """
        Add other point/vector to this point, returning new point

        :return Point - New point having added other to this
        """
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        """
        Point simply represented as a string of their co-ordinates

        :return: String - Formatted string representing a point
        """
        return f"P({self.x},{self.y})"


class Shape:
    """
    Stores the points that make up this shape.
    Has a factory method to create Shape instances based on shape type.

    - Shape:
        - Has a set of all the Points it occupies.
        - Factory methods to create each shape.
        - Point coordinates are created with the appropriate starting position (offset).
        - Factory method to create a shape for a set of points (e.g. when we move a shape)
        - Is hashable, so we can store it in sets.
    """

    def __init__(self, points: set[Point], at_rest:bool = False) -> None:
        """
        Initialises a Shape object

        :param points: Points comprising this shape
        :param at_rest: Whether this shape is at rest
        """
        self.points: set[Point] = points  # The points that make up this shape
        self.at_rest = at_rest

    @classmethod
    def create_shape_by_type(cls, shape_type: str, origin: Point) -> Shape:
        """
        Factory method to create an instance of our shape
        The shape points are offset by the supplied origin

        :param shape_type: Type of shape from within SHAPES
        :param origin: Origin considered by this shape (i.e., canonical centre)
        :return: Shape - Newly created shape object of given type relative to origin
        """
        return cls({(Point(*coords) + origin) for coords in SHAPES[shape_type]})

    @classmethod
    def create_shape_from_points(cls, points: set[Point], at_rest:bool = False) -> Shape:
        """
        Factory method to create an instance of our shape
        The shape points are offset by the supplied origin

        :param points: Sets of points comprising this shape
        :param at_rest: Whether this shape is at rest
        :return: Shape - Newly created shape object comprised of points
        """
        return cls(points, at_rest)

    def __eq__(self, other: object) -> bool:
        """
        Overwrite equality method for Shapes - equal if they have all same points

        :param other: Shape to compare equality to this Shape
        :return: bool - True if all points the same, False otherwise
        """
        if isinstance(other, Shape):
            if self.points == other.points:
                return True
        else:
            return NotImplemented

    def __hash__(self) -> int:
        """
        Overwrite hash method

        :return: int - New hash
        """
        return hash(repr(self))

    def __repr__(self) -> str:
        """
        Represent a Shape by displaying if at rest, and the points comprising the shape

        :return: str - Formatted string, as described
        """
        return f"Shape(at_rest={self.at_rest}, points={self.points}"


class Tower:
    """
    Tower:
        - Use itertools.cycle to infinitely iterate through the input jet pattern - We can always generate the next jet
        - Use itertools.cycle to infinitely iterate through the shapes in order - We can always generate the next shape
        - Stores all points for all at rest shapes (set)
        - Stores the current top of all the settled points
        - Can determine origin for new shapes, using current top
        - Simulates dropping a shape
            - Creates the new shape at the appropriate origin
            - Calls move with next jet
            - Calls move with down - If we can't move down, settles the shape by adding current shape to settled points
    """
    WIDTH = 7
    LEFT_WALL_X = 0
    RIGHT_WALL_X = LEFT_WALL_X + 7 + 1  # Right wall at x=8
    OFFSET_X = 2 + 1  # Objects start with left edge at x=3
    OFFSET_Y = 3 + 1  # New rocks have a gap of 3 above top of highest settled rock
    FLOOR_Y = 0

    # Printing characters
    FALLING = "@"
    AT_REST = "#"
    EMPTY = "."
    WALL = "|"
    FLOOR = "-"

    def __init__(self, jet_pattern: str) -> None:
        """
        Initialises a Tower object

        :param jet_pattern: The jet pattern for this tower
        """
        self.current_shape = None
        self._jet_pattern = itertools.cycle(enumerate(jet_pattern))  # Infinite cycle
        self._shape_generator = itertools.cycle(enumerate(SHAPES))  # Infinite cycle
        self.top = Tower.FLOOR_Y  # Keep track of top of blocks
        self._all_at_rest_shapes: set[Shape] = set()
        self._all_at_rest_points: set[Point] = set()  # Tracking this for speed

        self.repeat_identified = False
        self._cache: dict[tuple, tuple] = {}  # K=(rock_idx, jet_idx, rock_formation): V=(height, shape_ct)
        self._repeat: tuple = (0, 0)  # height_diff, shape_diff

    def _current_origin(self) -> Point:
        """
        Rocks are dropped 2 from the left edge, and 3 above the current tallest settled rock

        :return: Point determined to be the origin
        """
        return Point(Tower.LEFT_WALL_X + Tower.OFFSET_X, self.top + Tower.OFFSET_Y)

    def _next_shape(self) -> str:
        """
        Get the next shape from the generator

        :return: str - Next shape as string representation
        """
        return next(self._shape_generator)

    def _next_jet(self) -> str:
        """
        Get the next jet blast from the generator

        :return: str - Next jet blast
        """
        return next(self._jet_pattern)

    def _check_cache(self, shape_index: int, jet_index: int, formation: str) -> tuple:
        """
        Checking against cache of results
        """
        key = (shape_index, jet_index, formation)
        shape_ct = len(self._all_at_rest_shapes)
        
        if key in self._cache:  # Found a repeat
            last_height, last_shape_count = self._cache[key]
            return True, self.top, last_height, shape_ct, last_shape_count
        else:
            self._cache[key] = (self.top, shape_ct)

        return False, self.top, 0, shape_ct, 0

    def drop_shape(self) -> None:
        """
        Simulate dropping a shape in thw tower
        """
        shape_index, next_shape_type = self._next_shape()
        self.current_shape = Shape.create_shape_by_type(next_shape_type, self._current_origin())

        while True:
            jet_index, jet = self._next_jet()
            self._move_shape(jet)

            if not self._move_shape("V"):  # Failed to move down
                self.top = max(self.top, max(point.y for point in self.current_shape.points))
                settled_shape = Shape.create_shape_from_points(self.current_shape.points, True)
                self._settle_shape(settled_shape)

                if not self.repeat_identified:
                    cache_response = self._check_cache(shape_index, jet_index, self.get_recent_formation())

                    if cache_response[0]:  # Cache hit
                        self.repeat_identified = True
                        self._repeat = (cache_response[1] - cache_response[2],  # Current top - last top
                                        cache_response[3] - cache_response[4])  # Current shape ct - last shape ct

                break

    def calculate_height(self, shape_drops: int) -> tuple[int, int]:
        """
        Calculate the additional height given n shape drops

        We know that x shapes (shape repeat) create a height delta (height repeat) of y
        x - current_shape_ct -> required_drops
        required_drops // shape_repeat -> whole repeats required
        required_drops % shape_repeat -> remaining drops required
        required_drops * height_repeat -> height delta

        :return: tuple - new_height (int), remaining drops (int)
        """
        remaining_drops = shape_drops - len(self._all_at_rest_shapes)
        repeats_req = remaining_drops // self._repeat[1]  # full repeats
        remaining_drops %= self._repeat[1]  # remaining individual drops

        height_delta = self._repeat[0] * repeats_req  # height created by these repeats
        new_height = self.top + height_delta

        return new_height, remaining_drops

    def _settle_shape(self, shape: Shape) -> None:
        """
        Add this shape to the settled sets
        """
        self._all_at_rest_shapes.add(shape)
        self._all_at_rest_points.update(shape.points)

    def _move_shape(self, direction) -> bool:
        """
        Move a shape in the direction indicated. Return False if we can't move.
        """
        # Test against boundaries:
        if direction == "<":
            shape_left_x = min(point.x for point in self.current_shape.points)
            if shape_left_x == Tower.LEFT_WALL_X + 1:
                return False  # Can't move left

        if direction == ">":
            shape_right_x = max(point.x for point in self.current_shape.points)
            if shape_right_x == Tower.RIGHT_WALL_X - 1:
                return False  # Can't move right

        if direction == "V":
            shape_bottom = min(point.y for point in self.current_shape.points)
            if shape_bottom == Tower.FLOOR_Y + 1:
                return False  # Can't move down

        # Move phase - test for collision
        candidate_points = {(point + Point(*MOVE[direction])) for point in self.current_shape.points}
        if self._all_at_rest_points & candidate_points:  # If the candidate would intersect
            return False  # Then this is not a valid position
        else:  # We can move there. Update our current shape position, by constructing a new shape at the new position
            self.current_shape = Shape.create_shape_from_points(candidate_points)
        return True

    def get_recent_formation(self) -> str:
        """
        Covert last (top) 20 rows into a str representation
        """
        rows = []
        min_y = max(0, self.top - 20)  # we want the last 20 lines
        for y in range(min_y, self.top + 1):
            line = ""
            for x in range(Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X):
                if Point(x, y) in self._all_at_rest_points:
                    line += Tower.AT_REST
                elif Point(x, y) in self.current_shape.points:
                    line += Tower.FALLING
                else:
                    line += Tower.EMPTY

            rows.append(line)

        return "\n".join(rows[::-1])

    def __str__(self) -> str:
        """
        String representation for the tower

        :return: str - Formatted string for the tower
        """
        rows = []
        top_for_vis = max(self.top, max(point.y for point in self.current_shape.points))

        for y in range(Tower.FLOOR_Y, top_for_vis + 1):
            line = f"{y:3d} "
            if y == Tower.FLOOR_Y:
                line += "+" + (Tower.FLOOR * Tower.WIDTH) + "+"
            else:
                for x in range(Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X + 1):
                    if x in (Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X):
                        line += Tower.WALL
                    elif Point(x, y) in self._all_at_rest_points:
                        line += Tower.AT_REST
                    elif Point(x, y) in self.current_shape.points:
                        line += Tower.FALLING
                    else:
                        line += Tower.EMPTY

            rows.append(line)

        return f"{repr(self)}:\n" + "\n".join(rows[::-1])

    def __repr__(self) -> str:
        """
        Tower represented by its height and rested shapes

        :return: str - Formatted string, as described
        """
        return f"Tower(height={self.top}, rested={len(self._all_at_rest_shapes)})"


def main():
    """
    Rocks are falling and they resemble tetris pieces! They always fall in this order: -, +, backwards L, |, ■.

    Chamber is 7 units wide and rocks start to fall from:
    - Left edge 2 units from left wall
    - Bottom edge 3 units above highest rock in the room, or the floor

    Input is horizontal movement of the falling objects, as a result of jets of gasses from the sides. E.g:
    >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>

    This pattern also repeats indefinitely

    Rocks are pushed 1 unit, then fall one unit
    The rock comes to rest in the fall step AFTER it reaches its lowest point
    Then another rock starts to fall

    Part 1 Solution:
    How many units tall will the tower of rocks be after 2022 rocks have stopped falling?
    - To move a shape:
        - Check if we can move left, right or down based on bounds; return if we can't.
        - If bounds are okay, generate candidate points from current shape.
        - Check if candidate intersects with settled.  If so, we can't move there.
        - Otherwise, update current shape to be new shape from candidate points.
    - Finally, call tower.drop_shape 2022 times.

    Part 2 Solution:
    How tall will the tower be after 1000000000000 rocks have stopped?
    Part 1 achieves 1M drops / minute, o running Part 1 for this many drops would take 2 years!
    Look for a repeat of:
    - Same dropped rock (Enumerate the rocks)
    - Same index in the jets (Enumerate the jet data)
    - Identical rock formation - lets build a str (which is hashable) from the last 20 rows
    We will store these three values in a cache, implemented as a dict:
    - Key = rock_index, jet_index, rock_formation
    - Value = (current height, current shape count)
    Implement check_cache() method:
    - Check if the current key is in the cache
    - If it is, return (True, height, last_height, shape count, last shape count)
    - if not, update the cache
    - Modify drop_shape():
        - When our shape is settled, check the cache
        - If we get a cache hit, update a property for repeats_found
        - Store the two crucial values of our repeat cycle: height delta, and shape count delta
    - Add calculate_height(drops) method:
        - Determine how many drops are still required
        - Determine how many repeat cycles we need, by dividing by the shape count delta
        Also determine if there is a remainder, so we can manually drop the remaining shapes
        - Determine the height increase, based on this number of repeats. Add this to current height
        - Finally, return the calculated height, and the shape drop remainder
    - Back in main():
        - Drop shapes until we find our first repeat. Store the initial height at this point
        - Call calculate_height to determine the calculated height after n drops
        - Manually drop shapes for any remainder. Get the new height
        - The final height = calculated height + new height - initial height
    """
    with open("day17-input.txt", mode="rt") as f:
        data = f.read()

    # Part 1:
    tower = Tower(jet_pattern=data)
    for _ in range(2022):
        tower.drop_shape()

    print(f"How many units tall will the tower of rocks be after 2022 rocks have stopped falling?"
          f"\nAnswer: {repr(tower)}")

    # Part 2
    tower = Tower(jet_pattern=data)  # Recreate the initial tower
    while not tower.repeat_identified:  # Drop until we identify the first repeat
        tower.drop_shape()
    height_at_repeat_start = tower.top  # The height achieved before first repeat

    # Calculate the new height, but we're NOT modifying the actual tower height
    new_height, remaining_drops = tower.calculate_height(1000000000000)

    # If drops was not an exact multiple of drop repeat, then we'll need to top up with the remaining drops
    # However, we're continuing the drops with our tower at the point where the repeat was identified
    for _ in range(remaining_drops):
        tower.drop_shape()
    height_after_top_up = tower.top  # But this number does NOT include the calculated height delta
    # So, get the diff between the height now, and the height when we stopped dropping
    final_height = new_height + height_after_top_up - height_at_repeat_start

    print(f"How tall will the tower be after 1000000000000 rocks have stopped?"
          f"\nAnswer: {final_height}")


if __name__ == "__main__":
    main()
