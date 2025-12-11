import argparse

PuzzleAnswer = int
Filename = str


def get_suffix_max(nums: list[int]) -> list[int]:
    suffix_max = [0] * len(nums)
    suffix_max[-1] = nums[-1]
    for i in range(len(nums) - 2, -1, -1):
        suffix_max[i] = max(suffix_max[i + 1], nums[i])

    return suffix_max


def maximum_joltage(bank: list[int]) -> int:
    suffix_max = get_suffix_max(bank)
    max_joltage = 0

    for i in range(len(bank) - 1):
        max_joltage_starting_at_i = (bank[i] * 10) + suffix_max[i + 1]
        max_joltage = max(max_joltage, max_joltage_starting_at_i)

    return max_joltage


def solve(input_filename: Filename = "d03_input.txt") -> PuzzleAnswer:
    total_maximum_joltage = 0

    with open(input_filename, "r", encoding="utf-8") as file:
        for line in file:
            bank = [int(c) for c in line if c != '\n']
            total_maximum_joltage += maximum_joltage(bank)

    return total_maximum_joltage


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        ("d03_test_01.txt", 357),
        ("d03_input.txt", 16927)
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
