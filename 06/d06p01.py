import argparse
from collections import deque

DAY = "06"

PuzzleAnswer = int
Filename = str


def get_last_line(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return deque(f, maxlen=1)[0]


def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    operations = get_last_line(input_filename).split()
    results = [(0 if op == "+" else 1) for op in operations]

    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            columns = line.split()
            if len(columns) > 0 and columns[0] in operations:
                continue

            operands = map(int, columns)
            for column_idx, operand in enumerate(operands):
                op = operations[column_idx]
                if op == "+":
                    results[column_idx] += operand
                else:
                    assert op == "*"
                    results[column_idx] *= operand

    return sum(results)


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 4277556),
        (f"d{DAY}_input.txt", 6343365546996)
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
