from utils.core.game_utils import check_answer

def play_answer_checker(problem: str, user_answer: str):
    """Main logic for Answer Checker route."""
    return check_answer(problem, user_answer)
