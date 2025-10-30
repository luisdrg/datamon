import random

def start_number_guesser():
    """Start Number Guesser game."""
    return random.randint(9, 100)

def check_guess(secret_number: int, guess: int) -> str:
    """Compare user guess to secret number."""
    if guess < secret_number:
        return "Too low!"
    elif guess > secret_number:
        return "Too high!"
    return "Correct!"
