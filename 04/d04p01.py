import argparse

DAY = "04"

PuzzleAnswer = int
Filename = str

Position = tuple[int, int]

NEIGHBOR_OFFSETS = [(-1, -1), (0, -1), (1, -1),
                    (-1, 0), (1, 0),
                    (-1, 1), (0, 1), (1, 1)]

ROLL = '@'


class RollGrid:
    def __init__(self, roll_positions: set[Position]):
        self.roll_positions = roll_positions

    @classmethod
    def init_from_file(cls, filename: str) -> "RollGrid":
        roll_positions: set[Position] = set()

        with open(filename, "r", encoding="utf-8") as file:
            for y, line in enumerate(file):
                for x, ch in enumerate(line):
                    if ch == ROLL:
                        roll_positions.add((x, y))

        return cls(roll_positions)

    def get_accessible_roll_count(self) -> int:
        accessible_rolls = 0

        for x, y in self.roll_positions:
            adjacent_rolls = 0
            for dx, dy in NEIGHBOR_OFFSETS:
                nx, ny = x + dx, y + dy
                if (nx, ny) in self.roll_positions:
                    adjacent_rolls += 1

            if adjacent_rolls < 4:
                accessible_rolls += 1

        return accessible_rolls


def solve(input_filename: Filename = "d03_input.txt") -> PuzzleAnswer:
    grid = RollGrid.init_from_file(input_filename)

    return grid.get_accessible_roll_count()


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 13),
        (f"d{DAY}_input.txt", 1372)
    ]

    for input_filename, expected_answer in test_pairs:
        solution_answer = solve(input_filename)
        assert solution_answer == expected_answer, (
            f"Test for intput {input_filename} failed.\n"
            f"Expected: {expected_answer}.\n"
            f"Got:      {solution_answer}."
        )


def main() -> None:
    print("Running tests...")
    run_tests()
    print("Tests ran successfuly!\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", help="puzzle input file")
    args = parser.parse_args()

    if args.filename:
        print(f"Solving the puzzle with input {args.filename}...")
        answer = solve(args.filename)
        print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
