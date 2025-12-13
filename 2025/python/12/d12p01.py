import argparse

DAY = "12"

PuzzleAnswer = int
Filename = str
PuzzleParams = Filename

Coordinates = tuple[int, int]

class Area:
    def __init__(self, width: int, height: int, shape_counts: list[int]) -> None:
        self.width = width
        self.height = height
        self.shape_counts = shape_counts


class Shape:
    def __init__(self, shape_lines: list[str]) -> None:
        self.coords: list[Coordinates] = []
        for y, line in enumerate(shape_lines):
            for x, char in enumerate(line):
                if char == "#":
                    self.coords.append((x, y))

    def get_dihedral_variants(self) -> list[list[Coordinates]]:
        variants: list[list[Coordinates]] = []

        current_coords = self.coords
        for _ in range(4):
            current_coords = Shape.normalize_coords(current_coords)
            variants.append(current_coords)

            reflected = [(-x, y) for x, y in current_coords]
            reflected = Shape.normalize_coords(reflected)
            variants.append(reflected)

            rotated = [(-y, x) for x, y in current_coords]
            current_coords = rotated

        unique_variants: list[list[Coordinates]] = []
        seen_variants: set[frozenset[Coordinates]] = set()
        for variant in variants:
            variant_set = frozenset(variant)
            if variant_set not in seen_variants:
                seen_variants.add(variant_set)
                unique_variants.append(variant)

        return unique_variants

    def get_bounding_box_size(self) -> int:
        if len(self.coords) == 0:
            return 0

        max_x = max(x for x, _ in self.coords)
        max_y = max(y for _, y in self.coords)

        return (max_x + 1) * (max_y + 1)

    @staticmethod
    def normalize_coords(coords: list[Coordinates]) -> list[Coordinates]:
        min_x = min(x for x, _ in coords)
        min_y = min(y for _, y in coords)

        return [(x - min_x, y - min_y) for x, y in coords]

    @staticmethod
    def offset_coords(coords: list[Coordinates], offset_x: int, offset_y: int) -> list[Coordinates]:
        return [(x + offset_x, y + offset_y) for x, y in coords]


class Node:
    def __init__(self) -> None:
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.header: HeaderNode | None = None


class HeaderNode(Node):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.length: int = 0
        self.name = name
        self.header = self


class DancingLinksMatrix:
    """Dirty implementation attempt of Donald Knuth's Algorithm X using Dancing Links.
    See chapter 7.2.2.1 of The Art of Computer Programming, Volume 4B.
    """

    def __init__(self, shapes: list[Shape], area: Area) -> None:
        self.shapes = shapes
        self.area = area

        self.root: HeaderNode = HeaderNode("root")

        self.shape_headers: list[HeaderNode] = []
        for shape_i, shape_count in enumerate(area.shape_counts):
            for count_i in range(shape_count):
                header = HeaderNode(f"s{shape_i}_{count_i}")

                header.left = self.root.left
                header.right = self.root
                if self.root.left:
                    self.root.left.right = header
                self.root.left = header

                self.shape_headers.append(header)

        self.area_headers: list[list[HeaderNode]] = []
        for y in range(area.height):
            row: list[HeaderNode] = []
            for x in range(area.width):
                header = HeaderNode(f"a{x}_{y}")
                row.append(header)
            self.area_headers.append(row)

    def add_row(self, headers: list[HeaderNode]) -> None:
        first_node: Node | None = None
        last_node: Node | None = None

        for header in headers:
            new_node = Node()
            new_node.header = header

            # Link vertically
            new_node.up = header.up
            new_node.down = header
            new_node.header = header
            header.up.down = new_node
            header.up = new_node
            header.length += 1

            # Link horizontally
            if first_node is None:
                first_node = new_node
                last_node = new_node
                new_node.right = new_node
                new_node.left = new_node
            else:
                new_node.left = last_node
                new_node.right = first_node
                last_node.right = new_node
                first_node.left = new_node
                last_node = new_node


    def generate_rows(self) -> None:
        shape_start_index = 0

        for shape_type_i, shape_count in enumerate(self.area.shape_counts):
            shape = self.shapes[shape_type_i]
            shape_variants = shape.get_dihedral_variants()

            for shape_instance_j in range(shape_count):
                for variant in shape_variants:
                    for dy in range(self.area.height):
                        for dx in range(self.area.width):
                            placed_coords = Shape.offset_coords(variant, dx, dy)

                            if all(0 <= px < self.area.width and 0 <= py < self.area.height
                                for px, py in placed_coords):
                                headers: list[HeaderNode] = []
                                shape_header = self.shape_headers[shape_start_index + shape_instance_j]
                                headers.append(shape_header)
                                for px, py in placed_coords:
                                    area_header = self.area_headers[py][px]
                                    headers.append(area_header)

                                self.add_row(headers)

            shape_start_index += shape_count

    def cover(self, header: HeaderNode) -> None:
        header.right.left = header.left
        header.left.right = header.right

        row_node = header.down
        while row_node != header:
            col_node = row_node.right
            while col_node != row_node:
                col_node.down.up = col_node.up
                col_node.up.down = col_node.down

                col_node.header.length -= 1

                col_node = col_node.right

            row_node = row_node.down

    def uncover(self, header: HeaderNode) -> None:
        row_node = header.up
        while row_node != header:
            col_node = row_node.left
            while col_node != row_node:
                col_node.up.down = col_node
                col_node.down.up = col_node

                col_node.header.length += 1

                col_node = col_node.left

            row_node = row_node.up

        header.right.left = header
        header.left.right = header


    def search(self) -> bool:
        if self.root.right == self.root:
            return True

        smallest_column_header = self.root.right
        header_node = self.root.right
        while header_node != self.root:
            if header_node.length < smallest_column_header.length:
                smallest_column_header = header_node

            header_node = header_node.right

        self.cover(smallest_column_header)

        row_node = smallest_column_header.down
        while row_node != smallest_column_header:
            col_node = row_node.right
            while col_node != row_node:
                self.cover(col_node.header)

                col_node = col_node.right

            if self.search():
                return True

            col_node = row_node.left
            while col_node != row_node:
                self.uncover(col_node.header)

                col_node = col_node.left

            row_node = row_node.down

        self.uncover(smallest_column_header)

        return False


def read_input(input_filename: Filename) -> tuple[list[Shape], list[Area]]:
    shape_lines: list[str] = []
    shapes: list[Shape] = []
    areas: list[Area] = []

    def flush_shape():
        nonlocal shape_lines
        if shape_lines:
            shapes.append(Shape(shape_lines))
            shape_lines = []

    with open(input_filename, "r") as input_file:
        for line in input_file:
            line = line.strip()

            if not line:
                flush_shape()
                continue

            if "x" in line and ":" in line:
                flush_shape()

                area_size_str, shape_counts_str = line.split(":")
                area_width, area_height = map(int, area_size_str.split("x"))
                shape_counts = list(map(int, shape_counts_str.strip().split()))

                area = Area(area_width, area_height, shape_counts)
                areas.append(area)
            elif line.endswith(":") and line[:-1].isdigit():
                flush_shape()
            elif line[0] == "#" or line[0] == ".":
                shape_lines.append(line)

    flush_shape() # Catch the final shape if file ends with one

    return shapes, areas



def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    shapes, areas = read_input(input_filename)

    fitting_area_count = 0

    for area_i, area in enumerate(areas):
        area_cells = area.width * area.height
        total_shape_cells = sum(shape_count * len(shapes[i].coords)
                                for i, shape_count in enumerate(area.shape_counts))
        total_shape_bounding_box_cells = sum(shape_count * shapes[i].get_bounding_box_size()
                                             for i, shape_count in enumerate(area.shape_counts))

        if area_cells >= total_shape_bounding_box_cells:
            print(f"Area {area.width}x{area.height} with shape counts {area.shape_counts} trivially fits.")
            fitting_area_count += 1
        elif area_cells >= total_shape_cells:
            dl_matrix = DancingLinksMatrix(shapes, area)
            dl_matrix.generate_rows()

            if dl_matrix.search():
                print(f"Area {area.width}x{area.height} with shape counts {area.shape_counts} fits.")
                fitting_area_count += 1

        print(f"Processed area {area_i + 1}/{len(areas)}.")

    return fitting_area_count


def run_tests() -> None:
    test_pairs: list[tuple[PuzzleParams, PuzzleAnswer]] = [
        (f"d{DAY}_test_01.txt", 2),
        (f"d{DAY}_input.txt", 472)
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
