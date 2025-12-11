from typing import Generator, NamedTuple
import argparse
import re
from fractions import Fraction
import math


DAY = "10"

PuzzleAnswer = int
Filename = str
PuzzleParams = Filename


class LinearSystemResult(NamedTuple):
    aug_matrix: list[list[Fraction]]
    pivot_cols: list[int]
    free_cols: list[int]
    is_consistent: bool


def read_input(input_filename: Filename) -> Generator[tuple[str, list[list[int]], list[int]]]:
    # Pattern splitting input like
    #   «[.##.] (3) (1,3) (2) {3,5,4,7}»
    # into three groups:
    #   «.##.», «(3) (1,3) (2)», «3, 5, 4, 7».
    line_pattern = re.compile(r"^\[(.+?)\]\s(.+?)\s+\{(.+?)\}$")
    # Pattern extract groups of numbers from input like
    #   «(3) (1, 3) (2)»
    # into
    #   «3», «1, 3», «2».
    button_pattern = re.compile(r"\((.*?)\)")

    with open(input_filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            triple_match = line_pattern.match(line)

            assert triple_match is not None

            target = triple_match.group(1).strip()

            buttons_str = triple_match.group(2).strip()
            buttons: list[list[int]] = []
            for button_match in button_pattern.findall(buttons_str):
                button_values = [int(b.strip())
                                 for b in button_match.split(',')
                                 if b.strip() != ""]
                buttons.append(button_values)

            joltages_str = triple_match.group(3).strip()
            joltages = [int(j.strip())
                        for j in joltages_str.split(',')
                        if j.strip() != ""]

            yield target, buttons, joltages


def solve_linear_system(matrix: list[list[int]], target: list[int]) -> LinearSystemResult:
    var_count, eq_count = len(matrix[0]), len(matrix)
    assert len(target) == eq_count

    # Build augmented matrix A|x
    aug_mat = []
    for row_i, row in enumerate(matrix):
        aug_row = [Fraction(x) for x in row + [target[row_i]]]
        aug_mat.append(aug_row)

    pivot_row_i = 0
    pivot_cols = []
    is_pivot_col = [False] * var_count

    # Perform Gaussian Elimination
    for col_i in range(var_count):
        if pivot_row_i >= eq_count:
            break

        # Find pivot row
        row_i = pivot_row_i
        while row_i < eq_count and aug_mat[row_i][col_i] == 0:
            row_i += 1
        if row_i == eq_count:
            continue

        # Swap rows
        aug_mat[pivot_row_i], aug_mat[row_i] = \
            aug_mat[row_i], aug_mat[pivot_row_i]

        # Normalize pivot row
        invert_factor = 1 / aug_mat[pivot_row_i][col_i]
        for col_j in range(col_i, var_count + 1):
            aug_mat[pivot_row_i][col_j] *= invert_factor

        # Eliminate other row entries
        for row_i in range(eq_count):
            if row_i != pivot_row_i:
                factor = aug_mat[row_i][col_i]
                if factor != 0:
                    for col_j in range(col_i, var_count + 1):
                        aug_mat[row_i][col_j] -= factor * aug_mat[pivot_row_i][col_j]

        is_pivot_col[col_i] = True
        pivot_cols.append(col_i)
        pivot_row_i += 1

    # Check consistency
    is_consistent = True
    for row_i in range(pivot_row_i, eq_count):
        if aug_mat[row_i][-1] != 0:
            is_consistent = False
            break

    free_cols = [col_i for col_i in range(var_count)
                 if not is_pivot_col[col_i]]

    return LinearSystemResult(aug_mat, pivot_cols, free_cols, is_consistent)


def find_min_int_solution(system: LinearSystemResult, free_bounds: list[int]) -> int:
    aug_mat, pivot_cols, free_cols, _ = system

    base_cost = sum(aug_mat[row_i][-1]
                    for row_i in range(len(pivot_cols)))
    cost_coeffs = []
    for free_col_i in free_cols:
        sum_pivot_coeffs = sum(aug_mat[row_i][free_col_i]
                               for row_i in range(len(pivot_cols)))
        cost_coeffs.append(1 - sum_pivot_coeffs)

    constraints = []
    for row_i in range(len(pivot_cols)):
        coeffs = [aug_mat[row_i][free_col_i]
                  for free_col_i in free_cols]
        constraints.append((aug_mat[row_i][-1], coeffs))

    min_total = float("inf")

    def search(idx: int, current_cost: Fraction, current_vals: list[int]) -> None:
        nonlocal min_total

        # No free variables left
        if idx == len(free_cols):
            all_int = True

            for const, coeffs in constraints:
                val = const
                for cur_val_i, cur_val in enumerate(current_vals):
                    val -= coeffs[cur_val_i] * cur_val
                if val.denominator != 1 or val < 0:
                    all_int = False
                    break

            if all_int:
                min_total = min(min_total, current_cost)

            return

        # Calculate current free variable's bounds
        low = 0
        high = free_bounds[idx]
        for const, coeffs in constraints:
            residue = const
            for col_i in range(idx):
                residue -= coeffs[col_i] * current_vals[col_i]

            min_future = Fraction(0)
            for col_i in range(idx + 1, len(free_cols)):
                coeff = coeffs[col_i]
                if coeff < 0:
                    min_future += coeff * free_bounds[col_i]

            rhs = residue - min_future
            coeff = coeffs[idx]

            if coeff > 0:
                limit = math.floor(rhs / coeff)
                if limit < high:
                    high = limit
            elif coeff < 0:
                limit = math.ceil(rhs / coeff)
                if limit > low:
                    low = limit
            elif rhs < 0:
                return

        if low > high:
            return

        cc = cost_coeffs[idx]
        rng = range(low, high + 1) if cc >= 0 else range(high, low - 1, -1)

        for val in rng:
            new_cost = current_cost + cc * val

            if new_cost >= min_total:
                future_can_reduce = any(c < 0 for c in cost_coeffs[idx+1:])

                if not future_can_reduce:
                    break

            current_vals.append(val)
            search(idx + 1, new_cost, current_vals)
            current_vals.pop()

    search(0, base_cost, [])

    return int(min_total) if min_total != float("inf") else 0


def minimum_presses(target: list[int], buttons: list[list[int]]) -> int:
    w, h = len(buttons), len(target)

    buttons_matrix = [[0] * w for _ in range(h)]
    for col_idx, button in enumerate(buttons):
        for row_idx in button:
            buttons_matrix[row_idx][col_idx] = 1

    system_solution = solve_linear_system(buttons_matrix, target)
    if not system_solution.is_consistent:
        return 0

    free_variable_bounds = []
    for free_col in system_solution.free_cols:
        affected_indices = buttons[free_col]
        if len(affected_indices) == 0:
            free_variable_bounds.append(0)
        else:
            limit = min(target[i] for i in affected_indices)
            free_variable_bounds.append(limit)

    return find_min_int_solution(system_solution, free_variable_bounds)


def solve(input_filename: Filename = f"d{DAY}_input.txt") -> PuzzleAnswer:
    total_min_presses = 0

    for _, buttons, target in read_input(input_filename):
        total_min_presses += minimum_presses(target, buttons)

    return total_min_presses

def run_tests() -> None:
    test_pairs: list[tuple[PuzzleParams, PuzzleAnswer]] = [
        (f"d{DAY}_test_02.txt", 11),
        (f"d{DAY}_test_01.txt", 33)
        # (f"d{DAY}_input.txt", 375)
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
