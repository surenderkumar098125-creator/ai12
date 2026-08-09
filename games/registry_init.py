from games.registry import GAME_REGISTRY
from games.action.reaction_test import ReactionTest
from games.skill.tap_speed import TapSpeed
from games.classic.rps import RockPaperScissors
from games.classic.tictactoe import TicTacToe
from games.fun.guess_number import GuessNumber
from games.puzzle._2048 import Game2048

# register games
GAME_REGISTRY.register(ReactionTest)
GAME_REGISTRY.register(TapSpeed)
GAME_REGISTRY.register(RockPaperScissors)
GAME_REGISTRY.register(TicTacToe)
GAME_REGISTRY.register(GuessNumber)
GAME_REGISTRY.register(Game2048)
