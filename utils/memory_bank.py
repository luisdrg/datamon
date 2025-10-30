import time
from config import supabase
from utils.core.game_utils import check_answer

def add_to_memory_bank(user_id: str, problem: str):
    print(f"[TODO] Save '{problem}' to memory bank for {user_id}.")

def get_memory_bank_problems(user_id: str):
    print(f"[TODO] Fetch saved problems for {user_id}.")
    return []

def clear_memory_bank(user_id: str):
    print(f"[TODO] Clear memory bank for {user_id}.")

def start_memory_bank_session(user_id: str):
    print(f"[TODO] Start Memory Bank session for {user_id}.")
    return {
        "problems": [],
        "current_index": 0,
        "score": 0,
        "tries": 0,
        "start_time": time.time()
    }

def check_memory_bank_answer(session, user_answer):
    print("[TODO] Check user's Memory Bank answer.")
    return session
