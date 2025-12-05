import argparse

DAY = "05"

PuzzleAnswer = int
Filename = str


class Interval:
    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Interval):
            return NotImplemented

        return self.low == other.low and self.high == other.high

    def get_size(self) -> int:
        return self.high - self.low + 1

    def intersects(self, interval: "Interval") -> bool:
        return self.low <= interval.high and interval.low <= self.high


def read_input(input_filename: str) -> list[Interval]:
    intervals: list[Interval] = []

    with open(input_filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue

            if "-" in line:
                low, high = map(int, line.split("-"))
                interval = Interval(low, high)
                intervals.append(interval)

    return intervals


def merge_intervals(intervals: list[Interval]) -> list[Interval]:
    if len(intervals) == 0:
        return []

    merged: list[Interval] = []

    sorted_intervals = sorted(intervals, key=lambda interval: interval.low)
    current_interval = sorted_intervals[0]
    for i in range(1, len(sorted_intervals)):
        next_interval = sorted_intervals[i]
        if current_interval.intersects(next_interval):
            current_interval.high = max(current_interval.high,
                                        next_interval.high)
        else:
            merged.append(current_interval)
            current_interval = next_interval
    merged.append(current_interval)

    return merged


def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    intervals = read_input(input_filename)
    merged = merge_intervals(intervals)

    fresh_id_count = 0

    for interval in merged:
        fresh_id_count += interval.get_size()

    return fresh_id_count


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 14),
        (f"d{DAY}_input.txt", 348820208020395)
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
