# Imports
import sys
import copy
from math import inf as infinity


# Vars
width, height = 10, 10
board = [ [0 for x in range(width)] for y in range(height) ]

win_streak = 5 # how many pegs in a row to win

search_depth = 2 # how many turns into the future the algorithm will look

COMP = +1
HUMAN = -1


# Functions
def win(state, player): # return True if player has won
  return in_a_row(state, player, win_streak)

def gameover(state): # check if player wins or board is full
  return len(empty_cells(state)) == 0 or win(state, COMP) or win(state, HUMAN)

def in_a_row(state, player, n): # return if player has (n) in a row
  # check top-left to bottom-right diagonals
  for y in range(height):
    for x in range(width):
      try:
        if sum([state[y+i][x+i] for i in range(n)]) == player * n:
          return True
      except IndexError:
        continue

  # check bottom-left to top-right diagonals
  for y in range(height-n-1, width):
    for x in range(width-n+1):
      try:
        if sum([state[y-i][x+i] for i in range(n)]) == player * n:
          return True
      except IndexError:
        continue
  
  # check horizontals
  for y in range(width):
    for x in range(width-n+1):
      try:
        if sum([state[y][x+i] for i in range(n)]) == player * n:
          return True
      except IndexError:
        continue

  # check verticals
  for y in range(height-n+1):
    for x in range(width):
      try:
        if sum([state[y+i][x] for i in range(n)]) == player * n:
          return True
      except IndexError:
        continue
  
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
  cell_cords = []

  for y, row in enumerate(state):
    for x, cell in enumerate(row):
      if cell == 0:
        cell_cords.append([x, y])
  
  return cell_cords # list of [x, y] values

def make_move(state, player, x, y): # return board with given move made
  state_copy = copy.deepcopy(state)
  state_copy[y][x] = player

  return state_copy

def children(state, player): # return a list of all next possible board configs
  child_list = []

  for cell in empty_cells(board):
    child_list.append(make_move(state, player, cell[0], cell[1]))
  
  return child_list

def maximize(state, player, depth): # maximize computer advantage; returns a move & its utility
  if gameover(state) or depth >= search_depth:
    return state, evaluate(state)
  
  best_state = None
  maximum_utility = -infinity

  for child_state in children(state, player):
    check_state, check_utility = minimize(child_state, -player, depth+1)

    if check_utility-(depth*0.2) > maximum_utility:
      best_state = check_state
      maximum_utility = check_utility
  
  return best_state, maximum_utility

def minimize(state, player, depth): # minimize human advantage
  if gameover(state) or depth >= search_depth:
    return state, evaluate(state)
  
  best_state = None
  minimum_utility = infinity

  for child_state in children(state, player):
    check_state, check_utility = maximize(child_state, -player, depth+1)

    if check_utility+(depth*0.2) < minimum_utility:
      best_state = check_state
      minimum_utility = check_utility
  
  return best_state, minimum_utility

def render(state, h_choice, c_choice): # display (and prettify) the board to the console
  chars = {
    0: " ",
    +1: c_choice,
    -1: h_choice
  }

  print('-'*(width*2+15))

  print(f"+ {' '.join(map(str, list(range(width))))} +") # top number labels

  for i, row in enumerate(state):
    print(f"{i} {' '.join([chars[cell] for cell in row])}", end=" |\n")
    # print(f"{i}|{'|'.join([chars[cell] for cell in row])}", end="|\n")
  
  print(f"+ {'-'*(width*2-1)} +")

def parse_cords(raw_cords):
  cords = raw_cords.split(',')
  return int(cords[0]), int(cords[1])

def main():
  print("TicTac10")
  print(f"Pegs in a row to win: {win_streak}")
  print(f"Search depth: {search_depth}")

  h_choice = None
  c_choice = None
  human_first = None
  state = board
  
  while h_choice not in ['X', 'O']: # human chooses X or O
    h_choice = input("Choose X or O: ").upper()
  
  if h_choice == "O": # set computer to other char
    c_choice = "X"
  else:
    c_choice = "O"
  
  while human_first not in ['Y', 'N']:
    human_first = input("Do you want to go first? (Y/N): ").upper()
  
  render(state, h_choice, c_choice)

  if human_first == "Y":
    print("Your turn!")
    x, y = parse_cords(input("Input x,y: "))
    state = make_move(state, HUMAN, x, y)
    render(state, h_choice, c_choice)
  
  while not gameover(state): # main game loop
    print("Computer turn...")
    state = maximize(state, COMP, 0)[0]
    render(state, h_choice, c_choice)

    if gameover(state): break

    print("Your turn!")
    x, y = parse_cords(input("Input x,y: "))
    state = make_move(state, HUMAN, x, y)
    render(state, h_choice, c_choice)
  
  if len(empty_cells(state)) == 0:
    print("Draw!")
  elif win(state, COMP):
    print("Computer won!")
  elif win(state, HUMAN):
    print("You won!")


if __name__ == "__main__":
  main()
