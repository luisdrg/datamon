from typing import Optional
from config import supabase

def register_user(email: str, password: str, name: str):
    if supabase is None:
        raise RuntimeError("Supabase not configured.")
    # Supabase supports user_metadata for extra fields like name
    return supabase.auth.sign_up({
        "email": email,
        "password": password,
        "options": {"data": {"name": name}}
    })

def login_user(email: str, password: str):
    if supabase is None:
        raise RuntimeError("Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY in .env")
    return supabase.auth.sign_in_with_password({"email": email, "password": password})

def save_score(user_id: str, score: int):
    if supabase is None:
        # Allow running without Supabase (local demo)
        print("[WARN] Supabase not configured; skipping save_score.")
        return None
    return supabase.table("scores").insert({
        "user_id": user_id,
        "game": "Answer Checker",
        "score": score
    }).execute()
