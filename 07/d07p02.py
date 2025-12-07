import argparse

DAY = "07"

PuzzleAnswer = int
Filename = str

Position = tuple[int, int]


class ManifoldDiagram:
    def __init__(self) -> None:
        self.splitters: set[Position] = set()
        self.start: Position = (0, 0)
        self.width = 0
        self.height = 0

    def is_inside(self, position: Position) -> bool:
        x, y = position
        return 0 <= x < self.width and 0 <= y <= self.height


def read_input(input_filename: str) -> ManifoldDiagram:
    diagram = ManifoldDiagram()

    with open(input_filename, "r", encoding="utf-8") as f:
        for y, line in enumerate(f):
            diagram.height += 1
            diagram.width = max(diagram.width, len(line))

            for x, ch in enumerate(line):
                if ch == "^":
                    diagram.splitters.add((x, y))
                elif ch == "S":
                    diagram.start = (x, y)

    return diagram


def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    diagram = read_input(input_filename)

    level_beam_stack = [(diagram.start, 1)]
    pos_timelines: dict[Position, int] = {}
    while len(level_beam_stack) > 0:
        # Process the current floor of beams
        pos_timelines = {}
        while len(level_beam_stack) > 0:
            (beam_x, beam_y), beam_timelines = level_beam_stack.pop()

            next_pos = (beam_x, beam_y + 1)

            if next_pos not in diagram.splitters:
                pos_timelines[next_pos] = \
                    pos_timelines.get(next_pos, 0) + beam_timelines
            else:
                split_left_pos = (beam_x - 1, beam_y + 1)
                split_right_pos = (beam_x + 1, beam_y + 1)
                for split_pos in [split_left_pos, split_right_pos]:
                    pos_timelines[split_pos] = \
                        pos_timelines.get(split_pos, 0) + beam_timelines

        # Refill the stack with the next level
        for beam_pos, timelines in pos_timelines.items():
            if diagram.is_inside(beam_pos):
                level_beam_stack.append((beam_pos, timelines))

    total_timelines = 0

    for timelines in pos_timelines.values():
        total_timelines += timelines

    return total_timelines


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 4),
        (f"d{DAY}_test_02.txt", 40),
        (f"d{DAY}_input.txt", 40941112789504)
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
