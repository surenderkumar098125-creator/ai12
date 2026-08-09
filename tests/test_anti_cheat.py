import pytest
from games.anti_cheat import AntiCheat

def test_validate_score():
    assert AntiCheat.validate_score('rps', 100, 10)
    assert not AntiCheat.validate_score('rps', -10, 10)
