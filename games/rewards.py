def calculate_reward_basic(score: int, difficulty: str) -> dict:
    # simple reward mapping
    base = max(1, score // 10)
    mult = {"easy":1, "normal":1.2, "hard":1.5, "extreme":2}.get(difficulty,1)
    coins = int(base * mult)
    xp = int(coins * 0.5)
    gems = int(coins / 100)
    return {"coins": coins, "xp": xp, "gems": gems}
