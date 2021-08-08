# Imports
import sys
from math import inf as infinity


# Vars
width, height = 10, 10
board = [ [0 for x in range(width)] for y in range(height) ]

win_streak = 5 # how many pegs in a row to win

search_depth = 3 # how many turns into the future the algorithm will look

COMP = +1
HUMAN = -1


# Functions
def win(state, player): # calculate if a certain player has won
  pass

def gameover(state): # return True if a player has won or the board is full
  pass

def in_a_row(state, player, n): # check if a player has (n) in a row
  pass

def evaluate(state): # find a board's utility (desirability)
  pass

def make_move(state, pos): # return board with given move made; pos = (x, y)
  pass

def children(state, player): # returns a list of all next possible boards
  pass

def maximize(state, depth): # maximize computer advantage
  pass

def minimize(state, depth): # minimize human advantage
  pass

def render(state):
  chars = {
    0: " ",
    +1: "X",
    -1: "O"
  }

  print(f"  {' '.join(map(str, list(range(width))))}")

  for i, row in enumerate(state):
    print(f"{i} {' '.join([chars[cell] for cell in row])}")

render(board)