import argparse

PuzzleAnswer = int
Filename = str

def maximum_joltage(bank: list[int], battery_count: int = 12) -> int:
    to_pick = min(len(bank), battery_count)

    digits: list[int] = []

    for i, digit in enumerate(bank):
        remaining = len(bank) - i

        # Try to slide the new digit as much to the left as possible, without:
        # 1) Missing out on picking as much batteries as we can («to_pick»)
        # 2) Decreasing our maximum possible result (We can't slide left digits lower than «digits[-1]»)
        while len(digits) > 0 and digit > digits[-1] and len(digits) - 1 + remaining >= to_pick:
            digits.pop()

        if len(digits) < to_pick:
            digits.append(digit)

    max_joltage = 0

    for digit in digits[:to_pick]:
        max_joltage = (max_joltage * 10) + digit

    return max_joltage


def solve(input_filename: Filename = "d03_input.txt") -> PuzzleAnswer:
    total_maximum_joltage = 0

    with open(input_filename, "r", encoding="utf-8") as file:
        for line in file:
            bank = [int(c) for c in line if c != '\n']
            total_maximum_joltage += maximum_joltage(bank, 12)

    return total_maximum_joltage


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        ("d03_test_01.txt", 3121910778619),
        ("d03_input.txt", 167384358365132)
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
