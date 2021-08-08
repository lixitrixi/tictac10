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
def win(state, player): # return True if player has won
  return in_a_row(state, player, win_streak)

def gameover(state): # check if player wins or board is full
  return len(empty_cells(state)) == 0 or win(state, COMP) or win(state, HUMAN)

def in_a_row(state, player, n): # check if a player has (n) in a row
  pass

def evaluate(state): # find a board's utility (desirability)
  utility = 0
  
  if win(state, COMP): # if computer wins
    utility = 10
  if win(state, HUMAN): # if human wins
    utility = -10
  
  return utility

def empty_cells(state): # return list of empty cells in a board
  cells = []

  for y, row in enumerate(state):
    for x, cell in enumerate(row):
      if cell == 0:
        cells.append([x, y])
  
  return cells

def make_move(state, player, x, y): # return board with given move made
  state[y][x] = player
  
  return state

def children(state, player): # return a list of all next possible boards
  children = []

  for cell in empty_cells(state):
    children.append(make_move(state, player, cell[0], cell[1]))

  return children

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
    # print(f"{i}|{'|'.join([chars[cell] for cell in row])}", end="|\n")
