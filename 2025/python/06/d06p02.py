import argparse
from collections import deque
from math import prod

DAY = "06"

PuzzleAnswer = int
Filename = str


def get_last_line(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return deque(f, maxlen=1)[0]


def read_input(input_filename: str) -> tuple[list[str], list[list[int]]]:
    operators_line = get_last_line(input_filename)

    operators: list[str] = []
    operand_columns: list[list[int]] = []

    # Load the operators and precompute the counts of expected operands
    # in each column
    column_width = 0
    for ch in operators_line:
        if ch == " ":
            column_width += 1
        else:
            operators.append(ch)
            if column_width > 0:
                operand_columns.append([0] * column_width)
                column_width = 0
    # This is always true for the last operator column in a valid input file
    # if len(operand_columns) < len(operators):
    operand_columns.append([0] * (column_width + 1))

    # Load the operands for each column
    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            col_idx = 0
            subcol_idx = 0
            for ch in line:
                if ch in operators:
                    break

                if subcol_idx == len(operand_columns[col_idx]):
                    col_idx += 1
                    subcol_idx = 0
                else:
                    if ch != " ":
                        digit = int(ch)

                        operand_columns[col_idx][subcol_idx] = \
                            (operand_columns[col_idx][subcol_idx] * 10) + digit

                    subcol_idx += 1

    return operators, operand_columns


def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    grand_total = 0

    operator_columns, operand_columns = read_input(input_filename)

    for column_idx, operator in enumerate(operator_columns):
        operands = operand_columns[column_idx]
        if operator == "+":
            grand_total += sum(operands)
        else:
            assert operator == "*"
            grand_total += prod(operands)

    return grand_total


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 3263827),
        (f"d{DAY}_input.txt", 11136895955912)
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
