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

    def intersects(self, interval: "Interval") -> bool:
        return self.low <= interval.high and interval.low <= self.high


class IntervalNode:
    def __init__(self, interval: Interval):
        self.interval = interval
        self.max = interval.high
        self.left: IntervalNode | None = None
        self.right: IntervalNode | None = None

    def insert(self, interval: Interval) -> None:
        if self.interval == interval:
            return

        self.max = max(self.max, interval.high)

        if interval.low <= self.interval.low:
            if self.left is None:
                self.left = IntervalNode(interval)
            else:
                self.left.insert(interval)
        else:
            if self.right is None:
                self.right = IntervalNode(interval)
            else:
                self.right.insert(interval)

    def intersect_search(self, interval: Interval) -> "IntervalNode | None":
        node: IntervalNode | None = self
        while node is not None and not node.interval.intersects(interval):
            if node.left is not None and node.left.max >= interval.low:
                node = node.left
            else:
                node = node.right

        return node


class IntervalTree:
    def __init__(self) -> None:
        self.root: IntervalNode | None = None

    def intersect_search(self, interval: Interval) -> IntervalNode | None:
        if self.root is None:
            return None

        return self.root.intersect_search(interval)

    def insert(self, interval: Interval) -> None:
        if self.root is None:
            self.root = IntervalNode(interval)

        self.root.insert(interval)


def read_input(input_filename: str) -> tuple[IntervalTree, list[int]]:
    interval_tree = IntervalTree()
    points: list[int] = []

    with open(input_filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue

            if "-" in line:
                low, high = map(int, line.split("-"))
                interval = Interval(low, high)
                interval_tree.insert(interval)
            else:
                points.append(int(line))

    return (interval_tree, points)


def solve(input_filename: Filename = "d03_input.txt") -> PuzzleAnswer:
    interval_tree, ingredient_ids = read_input(input_filename)

    fresh_id_count = 0

    for ingredient_id in ingredient_ids:
        point_interval = Interval(ingredient_id, ingredient_id)
        if interval_tree.intersect_search(point_interval) is not None:
            fresh_id_count += 1

    return fresh_id_count


def run_tests() -> None:
    test_pairs: list[tuple[Filename, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 3),
        (f"d{DAY}_input.txt", 681)
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
