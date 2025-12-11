import argparse

Direction = str
LEFT = "L"
RIGHT = "R"

class Dial:
    def __init__(self, length: int = 100, starting_position: int = 50):
        self.length = length
        self.position = starting_position

    def turn(self, direction: Direction, distance: int) -> None:
        index_distance = -distance if direction == LEFT else distance

        self.position = (self.position + index_distance) % self.length

def solve(input_filename: str = "d01_input.txt") -> int:
    password = 0

    dial = Dial(100, 50)

    with open(input_filename, "r", encoding="utf-8") as file:
        for line in file:
            turn_direction = line[0]
            turn_distance = int(line[1:])
            dial.turn(turn_direction, turn_distance)

            if dial.position == 0:
                password += 1

    return password


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", help="puzzle input file")
    args = parser.parse_args()

    answer = solve(args.filename)

    print(answer)

if __name__ == "__main__":
    main()
