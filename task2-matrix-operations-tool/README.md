# Task 2 — Matrix Operations Tool

An interactive command-line tool for performing common matrix operations,
built on NumPy. Enter matrices row by row and get nicely boxed,
structured output.

## Setup

```bash
pip install numpy
```

(Or `pip install -r requirements.txt` if you're installing across the
whole repo — see the root README.)

## Run it

```bash
python matrix_operations_tool.py
```

## Menu options

| Key | Operation |
|---|---|
| 1 | Addition (A + B) |
| 2 | Subtraction (A - B) |
| 3 | Matrix multiplication (A × B) |
| 4 | Element-wise multiplication (A ∘ B) |
| 5 | Transpose (Aᵗ) |
| 6 | Determinant — det(A), square matrices only |
| 7 | Inverse — A⁻¹, square + non-singular only |
| 8 | Eigenvalues & eigenvectors — square matrices only |
| 9 | Rank |
| T | Trace — tr(A), square matrices only |
| D | Quick demo with pre-loaded 3×3 sample matrices |
| Q | Quit |

## Entering a matrix

When prompted, type each row as space-separated numbers and press Enter.
Type `done` once all rows are entered:

```
Row 1: 1 2 3
Row 2: 4 5 6
Row 3: 7 8 9
Row 4: done
```

The tool validates that every row has the same number of columns, and
re-prompts on invalid input (non-numeric values or mismatched row
lengths).

## Example session

```
Enter option: 6
Row 1: 1 2
Row 2: 3 4
Row 3: done

  +----------------------------------------------------------+
  |  Matrix A (entered)                                      |
  +----------------------------------------------------------+
  |  /    1    2  \
  |  \    3    4  /
  |  Shape: 2x2
  +----------------------------------------------------------+

  +----------------------------------------------------------+
  |  det(A)  [2x2]                                           |
  +----------------------------------------------------------+
  |   -2
  +----------------------------------------------------------+
```

## Error handling

- **Addition/subtraction/element-wise multiplication** require matching
  shapes; mismatches print a clear error instead of crashing.
- **Matrix multiplication** requires the columns of A to equal the rows
  of B; mismatches are reported with a clear message.
- **Determinant, inverse, eigenvalues, and trace** require a square
  matrix; the tool checks this before calling NumPy and explains why it
  can't proceed if not.
- **Inverse** additionally checks that the matrix isn't singular
  (determinant ≈ 0) before attempting `np.linalg.inv`.
