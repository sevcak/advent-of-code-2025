import argparse
import heapq

DAY = "08"

PuzzleAnswer = int
Filename = str
PuzzleParams = Filename

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


def get_weighted_edges(vertices: list[Vertex],
                       limit: int | None = None) -> list[Edge]:
    # Use a bounded max-heap to keep at most «limit» items
    weighted_edges: list[Edge] = []

    for i, v1 in enumerate(vertices):
        for j in range(i + 1, len(vertices)):
            v2 = vertices[j]

            weight = euclidean_distance_squared(v1, v2)

            if limit is None:
                weighted_edges.append((weight, i, j))
            else:
                if len(weighted_edges) < limit:
                    heapq.heappush(weighted_edges, (-weight, i, j))
                else:
                    max_weight, _, _ = weighted_edges[0]
                    if weight < -max_weight:
                        heapq.heapreplace(weighted_edges, (-weight, i, j))

    if limit is None:
        return weighted_edges

    return [(-weight, i, j) for (weight, i, j) in weighted_edges]


def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    box_positions = read_input(input_filename)

    connections = get_weighted_edges(box_positions)
    connections.sort()

    uf_parents = list(range(len(box_positions)))
    uf_sizes = [1] * len(box_positions)
    uf_components = len(box_positions)

    def find(x: int) -> int:
        while x != uf_parents[x]:
            uf_parents[x] = uf_parents[uf_parents[x]]
            x = uf_parents[x]

        return x

    def union(x: int, y: int) -> bool:
        nonlocal uf_components

        x_root = find(x)
        y_root = find(y)

        if x_root == y_root:
            return False

        if uf_sizes[x_root] < uf_sizes[y_root]:
            x_root, y_root = y_root, x_root

        uf_parents[y_root] = x_root
        uf_sizes[x_root] += uf_sizes[y_root]
        uf_components -= 1
        return True

    for _, v1_idx, v2_idx in connections:
        merged = union(v1_idx, v2_idx)

        if merged and uf_components == 1:
            x1, _, _ = box_positions[v1_idx]
            x2, _, _ = box_positions[v2_idx]
            return x1 * x2

    assert False


def run_tests() -> None:
    test_pairs: list[tuple[PuzzleParams, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 25272),
        (f"d{DAY}_input.txt", 6844224)
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
