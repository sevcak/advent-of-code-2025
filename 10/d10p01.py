import argparse
from typing import Generator
import re

DAY = "10"

PuzzleAnswer = int
Filename = str
PuzzleParams = Filename

INFINITY = 10 ** 20

def read_input(input_filename: Filename) -> Generator[tuple[str, list[list[int]], list[int]]]:
    # Pattern splitting input like
    #   «[.##.] (3) (1,3) (2) {3,5,4,7}»
    # into three groups:
    #   «.##.», «(3) (1,3) (2)», «3, 5, 4, 7».
    line_pattern = re.compile(r"^\[(.+?)\]\s(.+?)\s+\{(.+?)\}$")
    # Pattern extract groups of numbers from input like
    #   «(3) (1, 3) (2)»
    # into
    #   «3», «1, 3», «2».
    button_pattern = re.compile(r"\((.*?)\)")

    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            triple_match = line_pattern.match(line)

            target = triple_match.group(1).strip()

            buttons_str = triple_match.group(2).strip()
            buttons: list[list[int]] = []
            for button_match in button_pattern.findall(buttons_str):
                button_values = [int(b.strip())
                                 for b in button_match.split(',')
                                 if b.strip() != ""]
                buttons.append(button_values)

            joltages_str = triple_match.group(3).strip()
            joltages = [int(j.strip())
                        for j in joltages_str.split(',')
                        if j.strip() != ""]

            yield target, buttons, joltages


def minimum_presses(target: str, buttons: list[int]) -> int:
    min_presses = INFINITY
    start = "." * len(target)

    min_presses = min_presses_rec(target, start,
                                  buttons,
                                  min_presses, 0,
                                  {})

    return min_presses


def min_presses_rec(target: str, current: str,
                    buttons: list[int],
                    min_presses: int, presses: int,
                    result_presses: dict[str, int]) -> int:
    if current in result_presses and result_presses[current] <= presses:
        return INFINITY

    result_presses[current] = presses

    if current == target:
        return presses
    if presses >= min_presses:
        return presses

    for switch_indices in buttons:
        symbols = list(current)
        for idx in switch_indices:
            symbols[idx] = "#" if symbols[idx] != "#" else "."
        new_state = "".join(symbols)

        min_presses = min(min_presses, min_presses_rec(target, new_state,
                                                       buttons,
                                                       min_presses, presses + 1,
                                                       result_presses))

    return min_presses


def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    total_min_presses = 0

    for target, buttons, _ in read_input(input_filename):
        total_min_presses += minimum_presses(target, buttons)

    return total_min_presses

def run_tests() -> None:
    test_pairs: list[tuple[PuzzleParams, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 7),
        (f"d{DAY}_input.txt", 375)
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
