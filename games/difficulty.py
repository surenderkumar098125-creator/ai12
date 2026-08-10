DIFFICULTY_LEVELS = ["easy", "normal", "hard", "extreme"]

def normalize(d: str) -> str:
    d = (d or "").lower()
    return d if d in DIFFICULTY_LEVELS else "normal"
