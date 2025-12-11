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

    def is_accessible(self, position: Position) -> bool:
        x, y = position

        adjacent_rolls = 0
        for dx, dy in NEIGHBOR_OFFSETS:
            if (x + dx, y + dy) in self.roll_positions:
                adjacent_rolls += 1

                if adjacent_rolls >= 4:
                    return False

        return True

    def get_accessible_roll_count(self) -> int:
        count = 0

        for position in self.roll_positions:
            if self.is_accessible(position):
                count += 1

        return count

    def get_accessible_roll_positions(self) -> list[Position]:
        return [pos for pos in self.roll_positions if self.is_accessible(pos)]

    def remove_accessible_rolls_step(self) -> int:
        accessible = self.get_accessible_roll_positions()

        for position in accessible:
            self.roll_positions.remove(position)

        return len(accessible)

    def remove_accessible_rolls_full(self) -> int:
        total_removed = 0

        last_removed = self.remove_accessible_rolls_step()
        while last_removed > 0:
            total_removed += last_removed
            last_removed = self.remove_accessible_rolls_step()

        return total_removed


def solve(input_filename: Filename = "d03_input.txt") -> PuzzleAnswer:
    grid = RollGrid.init_from_file(input_filename)

    return grid.remove_accessible_rolls_full()


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 43),
        (f"d{DAY}_input.txt", 7922)
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
