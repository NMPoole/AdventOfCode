#######################################################################################################################
# Advent of Code 2022 - Day 10
#######################################################################################################################

class CathodeRayTube:
    """
    Object-oriented approach to the Cathode Ray Tube computer implementation:
    """

    def __init__(self):
        """
        Initialise CRT Computer:
        """
        self.cycle = 0  # Current CPU clock cycle
        self.x = 1  # Current register, X, value, which starts at 1
        self.signal = 0  # Current signal strength
        self.screen = []  # Current screen output

        self.crt_width = 40  # Width of the CRT display

        self.lit_pixel = '#'  # Character used to represent a lit pixel
        self.dark_pixel = '.'  # Character used to represent a dark pixel

    def calc_signal_strength(self) -> int:
        """
        Calculate the signal strength at the current state of this CRT computer
        Signal strength is X * cycles, but we only consider the signal strength every 40 cycles starting at the 20th

        :return: int - Calculated signal strength at current state, as defined
        """
        if (self.cycle - 20) % self.crt_width == 0:
            return self.cycle * self.x
        else:
            return 0

    def noop(self) -> None:
        """
        Implementation of a 'noop' operation:

        noop takes one cycle to complete
        It has no other effect
        """
        self.screen.append("") if self.cycle % self.crt_width == 0 else None  # New screen row every 40 cycles
        # If sprite positioned s.t. 1 of its 3 pixels is the pixel being drawn, the screen produces a lit pixel, else dark
        self.screen[-1] += self.lit_pixel if self.x - 1 <= self.cycle % self.crt_width <= self.x + 1 else self.dark_pixel

        self.cycle += 1
        self.signal += self.calc_signal_strength()  # Determine signal strength to add for current cycle

    def addx(self, val) -> None:
        """
        Implementation of a 'addx' operation:

        'addx V' takes two cycles to complete
        After two cycles, the X register is increased by the value V (V can be negative)
        """
        for _ in range(2):
            self.noop()

        self.x += val

    def execute(self, file_str: str) -> None:
        """
        Execute/simulate a set of instructions read from a file in this CRT computer

        :param file_str: String path to input file location to read instructions from
        """
        with open(file_str) as input_file:
            for instruction in input_file:
                cmd = instruction.rstrip().split()

                if cmd[0] == "noop":
                    self.noop()
                elif cmd[0] == "addx":
                    self.addx(int(cmd[1]))

    def show(self) -> str:
        """
        Gets representation of the CRT screen/display as formatted string

        :return: string - CRT display at current state
        """
        return "\n".join(self.screen)


def main():
    crt = CathodeRayTube()
    crt.execute("day10-input.txt")

    print(f"Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles."
          f"\nWhat is the sum of these six signal strengths?"
          f"\nAnswer: {crt.signal}")

    print(f"Render the image given by your program."
          f"\nWhat eight capital letters appear on your CRT?"
          f"\nAnswer: \n{crt.show()}")


if __name__ == "__main__":
    main()
