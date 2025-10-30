import re
from typing import Tuple, Optional

# Supported operator aliases
_op_alias = {
    '+': '+', '-': '-',
    '*': '*', 'x': '*', 'X': '*', '×': '*',
    '/': '/', '÷': '/'
}

def _normalize_operator(op_raw: str) -> Optional[str]:
    return _op_alias.get(op_raw.strip())

def parse_problem(problem: str) -> Tuple[Optional[int], Optional[str], Optional[int]]:
    """Parse simple integer math problems like '3 + 4' or '12 ÷ 5'."""
    s = problem.strip()
    match = re.search(r'(\d+)\s*([+\-*/xX×÷])\s*(\d+)', s)
    if not match:
        return None, None, None
    a = int(match.group(1))
    op = _normalize_operator(match.group(2))
    b = int(match.group(3))
    return a, op, b

def compute(a: int, op: str, b: int) -> int:
    """Perform integer math only. Division returns quotient (integer)."""
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a // b  # integer quotient only
    raise ValueError("Unsupported operator")

def format_division_remainder(a: int, b: int) -> str:
    """Return formatted quotient and remainder, e.g., '2 r 1'."""
    q, r = divmod(a, b)
    return f"{q} r {r}"
