import random
import string
import math
from copy import deepcopy

alphabet = list(string.ascii_uppercase)

class HumanPlayer():
    @staticmethod
    def parse_cords(raw):
        try:
            if raw[0].isalpha():
                return (int(raw[1:])-1, alphabet.index(raw[0]))
            elif raw[-1].isalpha():
                return (int(raw[:-1])-1, alphabet.index(raw[-1]))
            else:
                return None
        except Exception:
            return None
    
    def get_move(self, state):
        cords = self.parse_cords(input("Your turn!\nInput move: ").upper())
        while cords not in state.possible_moves():
            cords = self.parse_cords(input("Try again (eg. b3): ").upper())

        return cords


class RandomPlayer():
    def __init__(self, char):
        self.char = char

    def get_move(self, state):
        return random.choice(state.possible_moves)
        

class BotPlayer():
    def __init__(self, player, search_depth):
        self.player = player # X or O
        self.other_player = 'O' if player == 'X' else 'X'
        self.search_depth = search_depth
    
    def get_move(self, state):
        return self.minimax(state, True)['move']

    def minimax(self, state, depth, alpha, beta, maximizing): # returns optimal move
        if state.gameover() or depth == self.search_depth:
            return {'move': None, 'score': state.evaluate(self.player)}
        
        