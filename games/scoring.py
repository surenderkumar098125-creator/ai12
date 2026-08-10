def calculate_score_basic(state: dict) -> int:
    # default scoring: score value in state
    return int(state.get("score", 0))
