import argparse
import heapq
from math import prod

DAY = "08"

PuzzleAnswer = int
Filename = str
PuzzleParams = tuple[Filename, int]

Position = tuple[int, int, int]
Vertex = Position
Edge = tuple[int, int, int]


def read_input(input_filename: str) -> list[Position]:
    positions: list[Position] = []

    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            x, y, z = map(int, line.split(","))
            positions.append((x, y, z))

    return positions


def euclidean_distance_squared(v1: Position, v2: Position) -> int:
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    dx = x1 - x2
    dy = y1 - y2
    dz = z1 - z2
    return dx ** 2 + dy ** 2 + dz ** 2


def get_weighted_edges(vertices: list[Vertex], limit: int) -> list[Edge]:
    # Use a bounded max-heap to keep at most «limit» items
    weighted_edges_heap: list[Edge] = []

    for i, v1 in enumerate(vertices):
        for j in range(i + 1, len(vertices)):
            v2 = vertices[j]

            weight = euclidean_distance_squared(v1, v2)

            if len(weighted_edges_heap) < limit:
                heapq.heappush(weighted_edges_heap, (-weight, i, j))
            else:
                max_weight, _, _ = weighted_edges_heap[0]
                if weight < -max_weight:
                    heapq.heapreplace(weighted_edges_heap, (-weight, i, j))

    return [(-weight, i, j) for (weight, i, j) in weighted_edges_heap]


def solve(input_filename: Filename = f"d{DAY}_input.txt",
          connection_limit: int = 1000) -> PuzzleAnswer:
    box_positions = read_input(input_filename)
    connections = get_weighted_edges(box_positions, connection_limit)
    connections.sort()

    uf_parents = list(range(len(box_positions)))
    uf_sizes = [1] * len(box_positions)

    def find(x: int) -> int:
        while x != uf_parents[x]:
            uf_parents[x] = uf_parents[uf_parents[x]]
            x = uf_parents[x]

        return x

    def union(x: int, y: int) -> None:
        x_root = find(x)
        y_root = find(y)

        if x_root == y_root:
            return

        if uf_sizes[x_root] < uf_sizes[y_root]:
            x_root, y_root = y_root, x_root

        uf_parents[y_root] = x_root
        uf_sizes[x_root] += uf_sizes[y_root]

    for i in range(min(connection_limit, len(connections))):
        _, v1_idx, v2_idx = connections[i]
        union(v1_idx, v2_idx)

    circuit_sizes: list[int] = []
    for i in range(len(box_positions)):
        if i == find(i):
            circuit_sizes.append(uf_sizes[i])

    return prod(heapq.nlargest(3, circuit_sizes))


def run_tests() -> None:
    test_pairs: list[tuple[PuzzleParams, PuzzleAnswer]] = [
        ((f"d{DAY}_test_01.txt", 10), 40),
        ((f"d{DAY}_input.txt", 1000), 131580)
    ]

    for parameters, expected_answer in test_pairs:
        input_filename, connection_limit = parameters
        solution_answer = solve(input_filename, connection_limit)
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
