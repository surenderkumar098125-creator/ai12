from typing import Dict, Any

class AntiCheat:
    @staticmethod
    def validate_session(session) -> bool:
        # basic existence/ownership checks should be performed by service
        return True

    @staticmethod
    def validate_score(game_id: str, score: int, duration: float) -> bool:
        # reject obviously impossible scores (heuristic)
        if score < 0:
            return False
        if duration <= 0 and score > 0:
            return False
        if score > 10000000:
            return False
        return True

    @staticmethod
    def detect_duplicate(session_id: str, user_id: int) -> bool:
        # placeholder: check DB for existing completed session with same id
        return False

    @staticmethod
    def flag_suspicious(result: Dict[str, Any]):
        # add audit log entry in production
        return
