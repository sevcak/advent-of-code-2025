import argparse
import itertools

DAY = "09"

PuzzleAnswer = int
Filename = str
PuzzleParams = Filename

Position = tuple[int, int]

def read_input(input_filename: str) -> list[Position]:
    red_tiles: list[Position] = []

    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            x, y = map(int, line.split(","))

            red_tiles.append((x, y))

    return red_tiles


def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    red_tiles = read_input(input_filename)

    # Form the wall segments, with the last one looping back to the first
    walls = list(zip(red_tiles, red_tiles[1:] + red_tiles[:1]))

    candidates = []
    for p1, p2 in itertools.combinations(red_tiles, 2):
        x1, y1 = p1
        x2, y2 = p2

        width = abs(x1 - x2) + 1
        height = abs(y1 - y2) + 1
        area = width * height

        candidates.append((area, p1, p2))

    # Sort descendingly by area so we can exit early upon finding
    # the first valid rectangle, since it'll be the largest one
    candidates.sort(key=lambda x: x[0], reverse=True)

    for area, (x1, y1), (x2, y2) in candidates:
        # Compute the rectagle's bounding box
        rect_min_x = min(x1, x2)
        rect_max_x = max(x1, x2)
        rect_min_y = min(y1, y2)
        rect_max_y = max(y1, y2)

        is_valid = True
        for line_start, line_end in walls:
            line_start_x, line_start_y = line_start
            line_end_x, line_end_y = line_end

            left_of_rect = max(line_start_x, line_end_x) <= rect_min_x
            right_of_rect = min(line_start_x, line_end_x) >= rect_max_x
            above_rect = max(line_start_y, line_end_y) <= rect_min_y
            below_rect = min(line_start_y, line_end_y) >= rect_max_y

            # If the wall is not strictly on one side,
            # it intersects (or is inside) the rectabgle
            if not (left_of_rect or right_of_rect or above_rect or below_rect):
                is_valid = False
                break

        if is_valid:
            return area

    return 0

def run_tests() -> None:
    test_pairs: list[tuple[PuzzleParams, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 24),
        (f"d{DAY}_input.txt", 1343576598)
    ]

    for parameters, expected_answer in test_pairs:
        input_filename = parameters
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
