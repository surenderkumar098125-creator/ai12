"""Autogenerate many playable text+keyboard games programmatically."""
from typing import Callable
from .base import BaseGame
import random

def _make_math_game(i: int):
    class MathGame(BaseGame):
        @classmethod
        def get_id(cls):
            return f"math_quiz_{i}"
        @classmethod
        def get_name(cls):
            return f"Math Speed #{i}"
        @classmethod
        def get_category(cls):
            return "skill"
        async def start(self, **kwargs):
            a = random.randint(1, 10+i)
            b = random.randint(1, 10+i)
            op = random.choice(['+','-','*'])
            question = f"{a} {op} {b}"
            answer = eval(question)
            state = {'q': question, 'answer': answer, 'attempts':0}
            return {'state':state, 'message': f"Solve: {question}"}
        async def handle_input(self, state, user_input):
            state['attempts'] += 1
            try:
                if str(state['answer']) == str(int(user_input)):
                    state['score'] = max(0, 100 - (state['attempts']-1)*10)
                    return {'state':state, 'finished':True, 'message':'Correct!'}
                else:
                    return {'state':state, 'message':'Wrong, try again.'}
            except Exception:
                return {'state':state, 'message':'Send a number.'}
        async def finish(self, state):
            return {'score': state.get('score',0)}
        def calculate_score(self, state):
            return int(state.get('score',0))
        def calculate_reward(self, score, difficulty):
            return {'coins': max(1, score//10), 'xp': max(1, score//20), 'gems':0}
    return MathGame

def _make_memory_game(i: int):
    class MemoryGame(BaseGame):
        @classmethod
        def get_id(cls):
            return f"memory_match_{i}"
        @classmethod
        def get_name(cls):
            return f"Memory Match #{i}"
        @classmethod
        def get_category(cls):
            return "puzzle"
        async def start(self, **kwargs):
            size = 2 + (i % 4)
            seq = [random.randint(1,9) for _ in range(size)]
            state = {'seq': seq, 'pos':0}
            return {'state':state, 'message': f"Remember sequence of {len(seq)} numbers. Send them one by one."}
        async def handle_input(self, state, user_input):
            try:
                val = int(user_input)
            except Exception:
                return {'state':state, 'message':'Send a number.'}
            if state['seq'][state['pos']] == val:
                state['pos'] += 1
                if state['pos'] >= len(state['seq']):
                    state['score'] = 100
                    return {'state':state, 'finished':True, 'message':'Well done!'}
                return {'state':state, 'message':'Correct, next.'}
            else:
                state['score'] = max(0, 10 * state['pos'])
                return {'state':state, 'finished':True, 'message':'Wrong sequence.'}
        async def finish(self, state):
            return {'score': state.get('score',0)}
        def calculate_score(self, state):
            return int(state.get('score',0))
        def calculate_reward(self, score, difficulty):
            return {'coins': max(1, score//10), 'xp': max(1, score//20), 'gems':0}
    return MemoryGame

def _make_word_scramble(i:int):
    WORDS = ['apple','banana','python','telegram','puzzle','rocket','galaxy','dragon','wizard','forest']
    class WordScramble(BaseGame):
        @classmethod
        def get_id(cls):
            return f"word_scramble_{i}"
        @classmethod
        def get_name(cls):
            return f"Word Scramble #{i}"
        @classmethod
        def get_category(cls):
            return "fun"
        async def start(self, **kwargs):
            w = random.choice(WORDS)
            s = ''.join(random.sample(w, len(w)))
            state = {'word':w, 'scramble':s, 'attempts':0}
            return {'state':state, 'message': f"Unscramble: {s}"}
        async def handle_input(self, state, user_input):
            state['attempts'] += 1
            if user_input.strip().lower() == state['word']:
                state['score'] = max(0, 100 - (state['attempts']-1)*10)
                return {'state':state, 'finished':True, 'message':'Correct!'}
            return {'state':state, 'message':'Try again.'}
        async def finish(self, state):
            return {'score':state.get('score',0)}
        def calculate_score(self, state):
            return int(state.get('score',0))
        def calculate_reward(self, score, difficulty):
            return {'coins': max(1, score//10), 'xp': max(1, score//20), 'gems':0}
    return WordScramble

def register_autogen_games(registry):
    # create a blend of math, memory, scramble, trivia variations
    for i in range(6,76):
        if i % 3 == 0:
            registry.register(_make_math_game(i))
        elif i % 3 == 1:
            registry.register(_make_memory_game(i))
        else:
            registry.register(_make_word_scramble(i))
