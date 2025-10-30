from typing import Tuple
from utils.core.math_utils import parse_problem, compute, format_division_remainder

def parse_user_answer(ans: str):
    """
    Accepts only integer answers.
    Division problems must use 'Q r R' format.
    """
    ans = ans.strip()
    # Handle quotient + remainder input
    if 'r' in ans.lower():
        parts = ans.lower().split('r')
        try:
            q = int(parts[0].strip())
            r = int(parts[1].strip())
            return ('remainder', (q, r))
        except Exception:
            return ('invalid', None)
    # Handle single integer input
    try:
        return ('int', int(ans))
    except ValueError:
        return ('invalid', None)

def check_answer(problem: str, user_answer: str) -> Tuple[bool, str]:
    """
    Datamon-style integer-only answer checking.
    Division => quotient and remainder (no decimals allowed).
    """
    a, op, b = parse_problem(problem)
    if a is None or op is None or b is None:
        return False, "Invalid problem format (try: 12 ÷ 5)"
    if op == '/' and b == 0:
        return False, "EEE (division by zero)"

    # Division: quotient + remainder only
    if op == '/':
        q, r = divmod(a, b)
        correct_display = f"{q} r {r}"

        mode, parsed = parse_user_answer(user_answer)
        if mode != 'remainder':
            return False, f"Division requires 'Q r R' format (e.g., {correct_display})"
        return parsed == (q, r), correct_display

    # All other ops: integer math
    correct_val = compute(a, op, b)
    mode, parsed = parse_user_answer(user_answer)

    if mode == 'int':
        return parsed == correct_val, str(correct_val)
    else:
        return False, str(correct_val)
