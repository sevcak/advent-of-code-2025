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

    total_splits = 0

    beam_stack = [diagram.start]
    visited = {diagram.start}
    while len(beam_stack) > 0:
        beam_x, beam_y = beam_stack.pop()

        # Travel downwards
        while (diagram.is_inside((beam_x, beam_y + 1))
               and (beam_x, beam_y + 1) not in visited
               and not (beam_x, beam_y + 1) in diagram.splitters):
            beam_y += 1
            visited.add((beam_x, beam_y))

        # Handle split
        if (beam_x, beam_y + 1) in diagram.splitters:
            total_splits += 1

            left_split_pos = (beam_x - 1, beam_y + 1)
            right_split_pos = (beam_x + 1, beam_y + 1)
            for split_pos in [left_split_pos, right_split_pos]:
                if split_pos not in visited:
                    visited.add(split_pos)
                    beam_stack.append(split_pos)

    return total_splits


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 3),
        (f"d{DAY}_test_02.txt", 21),
        (f"d{DAY}_input.txt", 1662)
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
