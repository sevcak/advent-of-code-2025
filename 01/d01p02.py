import argparse


Direction = str
LEFT = "L"
RIGHT = "R"


class Dial:
    def __init__(self, length: int = 100, starting_position: int = 50):
        self.length = length
        self.position = starting_position

    def turn(self, direction: Direction, distance: int) -> int:
        start_position = self.position
        zero_crossings, distance_remaining = divmod(distance, self.length)

        if distance_remaining == 0:
            return zero_crossings

        index_distance = -distance_remaining if direction == LEFT else distance_remaining
        self.position = (self.position + index_distance) % self.length

        if self.position == 0:
            zero_crossings += 1
            return zero_crossings

        if start_position != 0:
            if direction == LEFT and self.position > start_position:
                zero_crossings += 1
            elif direction == RIGHT and self.position < start_position:
                zero_crossings += 1

        return zero_crossings


def solve(input_filename: str = "d01_input.txt") -> int:
    password = 0

    dial = Dial(100, 50)

    with open(input_filename, "r", encoding="utf-8") as file:
        for line in file:
            turn_direction = line[0]
            turn_distance = int(line[1:])

            password += dial.turn(turn_direction, turn_distance)

    return password


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", help="puzzle input file")
    args = parser.parse_args()

    answer = solve(args.filename)

    print(answer)


if __name__ == "__main__":
    main()
