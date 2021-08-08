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

def in_a_row(state, player, n): # return if player has (n) in a row
  # check top-left to bottom-right diagonals
  for y in range(height-n+1):
    for x in range(width-n+1):
      if sum([state[y+i][x+i] for i in range(n)]) == player * n:
        return True

  # check bottom-left to top-right diagonals
  for y in range(height-n-1, width):
    for x in range(width-n+1):
      if sum([state[y-i][x+i] for i in range(n)]) == player * n:
        return True
  
  # check horizontals
  for y in range(width):
    for x in range(width-n+1):
      if sum([state[y][x+i] for i in range(n)]) == player * n:
        return True

  # check verticals
  for y in range(height-n+1):
    for x in range(width):
      if sum([state[y+i][x] for i in range(n)]) == player * n:
        return True
  
  return False
  
def finishable(state, player, n): # return number of rows of (n) that can be completed with one more peg
  finishable_streaks = 0

  # check top-left to bottom-right diagonals
  for y in range(height):
    for x in range(width):
      try:
        cells = [state[y+i][x+i] for i in range(n)]
      except IndexError:
        continue
      if sum(cells) == player*(n-1) and -player not in cells:
        finishable_streaks += 1
  
  # check bottom-left to top-right diagonals
  for y in range(height-n-1, width):
    for x in range(width-n):
      try:
        cells = [state[y-i][x+i] for i in range(n)]
      except IndexError:
        continue
      if sum(cells) == player*(n-1) and -player not in cells:
        finishable_streaks += 1
      
  # check horizontals
  for y in range(width):
    for x in range(width-n):
      try:
        cells = [state[y][x+i] for i in range(n)]
      except IndexError:
        continue
      if sum(cells) == player*(n-1) and -player not in cells:
        finishable_streaks += 1
  
  # check verticals
  for y in range(height-n):
    for x in range(width):
      try:
        cells = [state[y+i][x] for i in range(n)]
      except IndexError:
        continue
      if sum(cells) == player*(n-1) and -player not in cells:
        finishable_streaks += 1
  
  return finishable_streaks

def evaluate(state): # find a board's utility (desirability)
  utility = 0
  
  if win(state, COMP): # if computer wins
    return 10
  if win(state, HUMAN): # if human wins
    return -10
  if finishable(state, COMP, win_streak) == 1:
    utility += 0.2
  if finishable(state, HUMAN, win_streak) == 1:
    utility -= 0.2
  if finishable(state, COMP, win_streak) > 1:
    utility += 5
  if finishable(state, HUMAN, win_streak) > 1:
    utility -= -5
  
  return utility

def empty_cells(state): # return list of empty cells in a board
  cells = []

  for y, row in enumerate(state):
    for x, cell in enumerate(row):
      if cell == 0:
        cells.append([x, y])
  
  return cells # list of [x, y] values

def make_move(state, player, x, y): # return board with given move made
  state[y][x] = player

  return state

def children(state, player): # return a list of all next possible board configs
  children = []

  for cell in empty_cells(state):
    children.append(make_move(state, player, cell[0], cell[1]))

  return children

def maximize(state, depth): # maximize computer advantage; returns a move & its utility
  if gameover(state) or depth == search_depth:
    return None, 

def minimize(state, depth): # minimize human advantage
  pass

def render(state): # display (and prettify) the board to the console
  chars = {
    0: " ",
    +1: "X",
    -1: "O"
  }

  print(f"+ {' '.join(map(str, list(range(width))))} +") # top number labels

  for i, row in enumerate(state):
    print(f"{i} {' '.join([chars[cell] for cell in row])}", end=" |\n")
    # print(f"{i}|{'|'.join([chars[cell] for cell in row])}", end="|\n")
  
  print(f"+ {'-'*(width*2-1)} +")

# board = make_move(board, COMP, 9, 4)
# board = make_move(board, COMP, 9, 5)
# board = make_move(board, COMP, 9, 6)
# board = make_move(board, COMP, 9, 7)
# board = make_move(board, COMP, 9, 8)

render(board)

# print(f"COMP won: {win(board, COMP)}")