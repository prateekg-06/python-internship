import sys
import numpy as np

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────

BORDER  = "=" * 58
DIVIDER = "-" * 58

# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def header(title: str) -> None:
    print(f"\n+{BORDER}+")
    print(f"|{'Matrix Operations Tool':^58}|")
    print(f"|{title:^58}|")
    print(f"+{BORDER}+\n")

def section(title: str) -> None:
    print(f"\n  +{DIVIDER}+")
    print(f"  |  {title:<56}|")
    print(f"  +{DIVIDER}+")

def display_matrix(mat: np.ndarray, label: str = "Matrix") -> None:
    section(label)
    rows, cols = mat.shape
    col_w = max(len(f"{v:.4g}") for v in mat.flatten()) + 2
    for i, row in enumerate(mat):
        if rows == 1:
            prefix, suffix = "  |  [", "]"
        elif i == 0:
            prefix, suffix = "  |  /", "\\"
        elif i == rows - 1:
            prefix, suffix = "  |  \\", "/"
        else:
            prefix, suffix = "  |  |", "|"
        inner = "  ".join(f"{v:>{col_w}.4g}" for v in row)
        print(f"{prefix}  {inner}  {suffix}")
    print(f"  |  Shape: {rows}x{cols}")
    print(f"  +{DIVIDER}+")

def display_scalar(value: float, label: str) -> None:
    section(label)
    print(f"  |   {value:.6g}")
    print(f"  +{DIVIDER}+")

def input_matrix(name: str) -> np.ndarray:
    """Prompt the user to enter a matrix row by row."""
    print(f"\n  Enter {name}:")
    print("  (Type each row as space-separated numbers, press Enter after each row.")
    print("   Type 'done' when finished.)\n")
    rows = []
    row_num = 1
    while True:
        raw = input(f"    Row {row_num}: ").strip()
        if raw.lower() == "done":
            if not rows:
                print("  [!]  Please enter at least one row.")
                continue
            break
        try:
            vals = list(map(float, raw.split()))
            if not vals:
                raise ValueError
            if rows and len(vals) != len(rows[0]):
                print(f"  [!]  Expected {len(rows[0])} value(s). Try again.")
                continue
            rows.append(vals)
            row_num += 1
        except ValueError:
            print("  [!]  Invalid input. Enter space-separated numbers.")

    mat = np.array(rows)
    display_matrix(mat, f"{name} (entered)")
    return mat

# ─────────────────────────────────────────────
#  Operations
# ─────────────────────────────────────────────

def op_addition() -> None:
    header("Addition  A + B")
    A = input_matrix("Matrix A")
    B = input_matrix("Matrix B")
    try:
        display_matrix(A + B, "Result  A + B")
    except ValueError:
        print("\n  [X]  Shapes are incompatible for addition.")

def op_subtraction() -> None:
    header("Subtraction  A - B")
    A = input_matrix("Matrix A")
    B = input_matrix("Matrix B")
    try:
        display_matrix(A - B, "Result  A - B")
    except ValueError:
        print("\n  [X]  Shapes are incompatible for subtraction.")

def op_multiplication() -> None:
    header("Multiplication  A x B")
    A = input_matrix("Matrix A")
    B = input_matrix("Matrix B")
    try:
        display_matrix(np.dot(A, B), "Result  A x B")
    except ValueError:
        print("\n  [X]  Incompatible shapes: columns of A must equal rows of B.")

def op_element_mult() -> None:
    header("Element-wise Multiplication  A * B")
    A = input_matrix("Matrix A")
    B = input_matrix("Matrix B")
    try:
        display_matrix(A * B, "Result  A * B")
    except ValueError:
        print("\n  [X]  Shapes must match for element-wise multiplication.")

def op_transpose() -> None:
    header("Transpose  A^T")
    A = input_matrix("Matrix A")
    display_matrix(A.T, "Result  A^T")

def op_determinant() -> None:
    header("Determinant  det(A)")
    A = input_matrix("Matrix A")
    if A.shape[0] != A.shape[1]:
        print("\n  [X]  Determinant requires a square matrix.")
        return
    display_scalar(np.linalg.det(A), f"det(A)  [{A.shape[0]}x{A.shape[1]}]")

def op_inverse() -> None:
    header("Inverse  A^-1")
    A = input_matrix("Matrix A")
    if A.shape[0] != A.shape[1]:
        print("\n  [X]  Inverse requires a square matrix.")
        return
    if abs(np.linalg.det(A)) < 1e-12:
        print("\n  [X]  Matrix is singular (det ~ 0); inverse does not exist.")
        return
    display_matrix(np.linalg.inv(A), "Result  A^-1")

def op_eigenvalues() -> None:
    header("Eigenvalues & Eigenvectors")
    A = input_matrix("Matrix A")
    if A.shape[0] != A.shape[1]:
        print("\n  [X]  Eigenvalues require a square matrix.")
        return
    vals, vecs = np.linalg.eig(A)
    section("Eigenvalues")
    for i, v in enumerate(vals):
        print(f"  |   L{i+1} = {v:.6g}")
    print(f"  +{DIVIDER}+")
    display_matrix(np.real(vecs), "Eigenvectors (columns, real part)")

def op_rank() -> None:
    header("Matrix Rank")
    A = input_matrix("Matrix A")
    display_scalar(np.linalg.matrix_rank(A), f"Rank of A  [{A.shape[0]}x{A.shape[1]}]")

def op_trace() -> None:
    header("Trace  tr(A)")
    A = input_matrix("Matrix A")
    if A.shape[0] != A.shape[1]:
        print("\n  [X]  Trace requires a square matrix.")
        return
    display_scalar(np.trace(A), f"tr(A)  [{A.shape[0]}x{A.shape[1]}]")

def op_demo() -> None:
    """Quick demo with pre-loaded 3x3 matrices."""
    header("Quick Demo  (3x3 sample matrices)")
    D1 = np.array([[1,2,3],[4,5,6],[7,8,9]], dtype=float)
    D2 = np.array([[9,8,7],[6,5,4],[3,2,1]], dtype=float)
    display_matrix(D1, "Sample A")
    display_matrix(D2, "Sample B")
    display_matrix(D1 + D2,        "A + B")
    display_matrix(D1 - D2,        "A - B")
    display_matrix(np.dot(D1, D2), "A x B")
    display_matrix(D1.T,           "A^T")
    display_scalar(np.linalg.det(D1), "det(A)")
    display_scalar(np.linalg.matrix_rank(D1), "rank(A)")

# ─────────────────────────────────────────────
#  Main menu
# ─────────────────────────────────────────────

MENU = [
    ("1", "Addition             (A + B)",   op_addition),
    ("2", "Subtraction          (A - B)",   op_subtraction),
    ("3", "Multiplication       (A x B)",   op_multiplication),
    ("4", "Element-wise Mult    (A * B)",   op_element_mult),
    ("5", "Transpose            (A^T)",     op_transpose),
    ("6", "Determinant          det(A)",    op_determinant),
    ("7", "Inverse              (A^-1)",    op_inverse),
    ("8", "Eigenvalues & Eigenvectors",     op_eigenvalues),
    ("9", "Rank",                           op_rank),
    ("T", "Trace                tr(A)",    op_trace),
    ("D", "Quick Demo",                     op_demo),
    ("Q", "Quit",                           None),
]

def print_menu() -> None:
    print(f"\n+{BORDER}+")
    print(f"|{'  Matrix Operations Tool  ':^58}|")
    print(f"+{BORDER}+")
    for key, label, _ in MENU:
        print(f"|  [{key}]  {label:<52}|")
    print(f"+{BORDER}+")

def main() -> None:
    print(f"\n{'='*60}")
    print(f"  Welcome to the Matrix Operations Tool  (NumPy {np.__version__})")
    print(f"{'='*60}")

    lookup = {k.upper(): fn for k, _, fn in MENU}

    while True:
        print_menu()
        choice = input("\n  Enter option: ").strip().upper()
        if choice == "Q":
            print("\n  Goodbye!\n")
            break
        fn = lookup.get(choice)
        if fn is None:
            print("  [!]  Invalid option. Try again.")
        else:
            fn()
            input("\n  Press Enter to return to menu...")

if __name__ == "__main__":
    main()
