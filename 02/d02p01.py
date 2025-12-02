import argparse
import re

PuzzleAnswer = int
Filename = str


def invalid_id_sum_in_range(start_id: int, end_id: int) -> int:
    invalid_id_sum = 0

    double_pattern = re.compile(r'^(\d+)\1$')
    for current_id in range(start_id, end_id + 1):
        id_str = str(current_id)
        if double_pattern.fullmatch(id_str):
            invalid_id_sum += current_id

    return invalid_id_sum


# No regex version
def iisir_alt(start_id: int, end_id: int) -> int:
    invalid_id_sum = 0

    for current_id in range(start_id, end_id + 1):
        id_str = str(current_id)

        if is_double(id_str):
            invalid_id_sum += current_id

    return invalid_id_sum


def is_double(id_str: str) -> bool:
    digit_count = len(id_str)
    if digit_count % 2 != 0:
        return False

    boundary = digit_count // 2
    return id_str[:boundary] == id_str[boundary:]


def solve(input_filename: str = "d02_input.txt") -> PuzzleAnswer:
    invalid_id_sum = 0

    id_ranges: list[str] = []
    with open(input_filename, "r", encoding="utf-8") as file:
        id_ranges = file.read().split(',')

    for id_range in id_ranges:
        boundary_id_strs = id_range.split('-')
        start_id = int(boundary_id_strs[0])
        end_id = int(boundary_id_strs[1])

        # invalid_id_sum += invalid_id_sum_in_range(start_id, end_id)
        invalid_id_sum += iisir_alt(start_id, end_id)


    return invalid_id_sum


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        ("d02_test_01.txt", 1227775554),
        ("d02_input.txt", 38437576669)
    ]

    for input_filename, expected_answer in test_pairs:
        solution_answer = solve(input_filename)
        assert solution_answer == expected_answer, (
            f"Test for intput {input_filename} failed.\n"
            f"Expected: {expected_answer}.\n"
            f"Got: {solution_answer}."
        )


def main() -> None:
    print("Running tests...")
    run_tests()
    print("Tests ran successfuly!\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", help="puzzle input file")
    args = parser.parse_args()

    answer = solve(args.filename)

    print(answer)


if __name__ == "__main__":
    main()
