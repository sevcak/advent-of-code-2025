import argparse

DAY = "11"

PuzzleAnswer = int
Filename = str
PuzzleParams = Filename

Graph = dict[str, list[str]]


def read_input(input_filename: Filename) -> Graph:
    graph: Graph = {}

    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            from_node_name, to_node_names = line.split(":")
            to_node_names = to_node_names.strip().split()

            if from_node_name not in graph:
                graph[from_node_name] = []

            for to_node_name in to_node_names:
                graph[from_node_name].append(to_node_name)


    return graph


def count_paths(graph: Graph, src: str, dest: str, thru: list[str]) -> int:
    memo: dict[tuple[str, int], int] = {}

    def _count_paths_rec(u: str, mask: int) -> int:
        if (u, mask) in memo:
            return memo[(u, mask)]

        new_mask = mask
        for idx, v in enumerate(thru):
            if u == v:
                new_mask |= (1 << idx)

        if u == dest:
            return 1 if new_mask == (1 << len(thru)) - 1 else 0

        total_paths = 0
        for v in graph.get(u, []):
            total_paths += _count_paths_rec(v, new_mask)

        memo[(u, mask)] = total_paths

        return total_paths

    return _count_paths_rec(src, 0)



def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    graph = read_input(input_filename)

    return count_paths(graph, "svr", "out", ["fft", "dac"])


def run_tests() -> None:
    test_pairs: list[tuple[PuzzleParams, PuzzleAnswer]] = [
        (f"d{DAY}_test_02.txt", 2),
        (f"d{DAY}_input.txt", 545394698933400)
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
