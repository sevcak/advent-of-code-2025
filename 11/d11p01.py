import argparse

DAY = "11"

PuzzleAnswer = int
Filename = str
PuzzleParams = Filename


class GraphNode:
    def __init__(self, value: str):
        self.value = value
        self.succs: list[GraphNode] = []
        self.visited = False
        self.paths_to_dest = 0

    def clear_flags(self) -> None:
        self.visited = False
        self.paths_to_dest = 0

Graph = dict[str, GraphNode]


def read_input(input_filename: Filename) -> Graph:
    graph: dict[str, GraphNode] = {}

    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            from_node_name, to_node_names = line.split(":")
            to_node_names = to_node_names.strip().split(" ")

            if from_node_name not in graph:
                graph[from_node_name] = GraphNode(from_node_name)
            pred_node = graph[from_node_name]

            for to_node_name in to_node_names:
                if to_node_name not in graph:
                    graph[to_node_name] = GraphNode(to_node_name)
                succ_node = graph[to_node_name]

                pred_node.succs.append(succ_node)

    return graph


def count_paths_to_dest(src_node: GraphNode, dest_node: GraphNode) -> int:
    if src_node.visited:
        return src_node.paths_to_dest

    src_node.visited = True

    if src_node == dest_node:
        src_node.paths_to_dest = 1

        src_node.visited = True

        return 1

    path_count = 0
    for succ_node in src_node.succs:
        path_count += count_paths_to_dest(succ_node, dest_node)

    src_node.paths_to_dest = path_count
    return path_count


def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    graph = read_input(input_filename)

    return count_paths_to_dest(graph["you"], graph["out"])


def run_tests() -> None:
    test_pairs: list[tuple[PuzzleParams, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 5),
        (f"d{DAY}_input.txt", 708)
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
