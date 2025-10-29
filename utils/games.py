import re
from typing import Tuple, Optional

_op_alias = {
    '+': '+',
    '-': '-',
    '*': '*',
    'x': '*', 'X': '*', '×': '*',
    '/': '/',
    '÷': '/'
}

def _normalize_operator(op_raw: str) -> Optional[str]:
    return _op_alias.get(op_raw.strip())

def parse_problem(problem: str) -> Tuple[Optional[int], Optional[str], Optional[int]]:
    """Parse problems like '3 + 4', '12 x 5', '10 ÷ 3'.
    Returns (a, op, b) as ints and normalized operator, or (None, None, None) if invalid.
    """
    s = problem.strip()
    # Allow formats with spaces or without, handle unicode ops
    # Try to split by known operators while preserving operator
    match = re.search(r'(\d+)\s*([+\-*/xX×÷])\s*(\d+)', s)
    if not match:
        return None, None, None
    a = int(match.group(1))
    op = _normalize_operator(match.group(2))
    b = int(match.group(3))
    if op is None:
        return None, None, None
    return a, op, b

def compute(a: int, op: str, b: int):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b
    raise ValueError("Unsupported operator")

def format_division_remainder(a: int, b: int) -> str:
    q = a // b
    r = a % b
    return f"{q} r {r}"

def parse_user_answer(ans: str):
    ans = ans.strip()
    # Support remainder format like "7 r 1" or "7 R 1"
    if 'r' in ans.lower():
        parts = re.split(r'\s*[rR]\s*', ans)
        if len(parts) == 2 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
            q = int(parts[0].strip())
            r = int(parts[1].strip())
            return ('remainder', (q, r))
        return ('invalid', None)
    # Otherwise, try float
    try:
        return ('float', float(ans))
    except ValueError:
        return ('invalid', None)

def check_answer(problem: str, user_answer: str):
    """Return (is_correct: bool, correct_display: str).
    - Accepts user answers as float or 'Q r R' for division.
    - Displays correct value as a decimal or remainder form when appropriate.
    """
    a, op, b = parse_problem(problem)
    if a is None:
        return False, "Invalid problem format. Try like: 12 ÷ 5"
    try:
        correct_val = compute(a, op, b)
    except ZeroDivisionError:
        return False, "EEE (division by zero)"
    except Exception:
        return False, "EEE (invalid computation)"

    mode, parsed = parse_user_answer(user_answer)

    # If division and not an exact integer, support remainder checking
    if op == '/' and b != 0 and a % b != 0:
        correct_rem = (a // b, a % b)
        correct_display = f"{correct_rem[0]} r {correct_rem[1]}"

        if mode == 'remainder':
            is_correct = (parsed == correct_rem)
            return is_correct, correct_display
        elif mode == 'float':
            # Accept numeric if it matches the exact decimal value
            is_correct = abs(parsed - correct_val) < 1e-9
            return is_correct, correct_display
        else:
            return False, correct_display
    else:
        # Non-division or exact division: numeric compare
        correct_display = str(int(correct_val)) if float(correct_val).is_integer() else str(correct_val)
        if mode == 'float':
            is_correct = abs(parsed - correct_val) < 1e-9
            return is_correct, correct_display
        elif mode == 'remainder':
            # If user supplied remainder for an exact division, it's wrong unless r == 0 and q matches
            q_expected = int(correct_val)
            is_correct = (parsed == (q_expected, 0))
            return is_correct, correct_display
        else:
            return False, correct_display
