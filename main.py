# Imports
import sys
from copy import deepcopy
import math
import platform
from os import system
import random
import string


# Vars
width, height = 4, 4 # height can not be more than 26
board = [ [0 for x in range(width)] for y in range(height) ]

win_streak = 3 # how many pegs in a row to win

search_depth = 6 # how many turns into the future the algorithm will look

COMP = +1
HUMAN = -1

alphabet = list(string.ascii_uppercase)


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
        if sum([state[y-i][x+i] for i in range(n) if y-i >= 0]) == player * n:
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
    return 1
  if win(state, HUMAN): # if human wins
    return -1
  # if finishable(state, COMP, win_streak) == 1:
  #   utility += 2
  # if finishable(state, HUMAN, win_streak) == 1:
  #   utility += -2
  # if finishable(state, COMP, win_streak) > 1:
  #   utility += 5
  # if finishable(state, HUMAN, win_streak) > 1:
  #   utility += -5
  
  return utility


def empty_cells(state): # return list of empty cells in a given board
  cell_cords = []

  for y, row in enumerate(state):
    for x, cell in enumerate(row):
      if cell == 0:
        cell_cords.append([x, y])
  
  return cell_cords # list of [x, y] values


def get_moves(state): # returns a list of possible move cords
  return empty_cells(state) # I know this just uses the above function but the name makes more sense like this


def make_move(state, player, x, y): # return board with given move made
  state_copy = deepcopy(state)
  state_copy[y][x] = player

  return state_copy


def maximize(state, depth=0, this_move=None): # finds move with maximum utility (score)
  if depth == search_depth or gameover(state):
    return this_move, evaluate(state)*(0.95**depth)
  
  max_util = -math.inf
  best_move = None

  for next_move in get_moves(state):
    child_state = make_move(state, COMP, next_move[0], next_move[1])
    check_move, check_util = minimize(child_state, depth+1, next_move)
    if check_util > max_util:
      best_move = check_move
      max_util = check_util
    if check_util == max_util:
      if random.random() < 0.2:
        best_move = check_move
  
  if this_move == None:
    return best_move, (max_util+evaluate(state))*(0.95**depth)
  else:
    return this_move, (max_util+evaluate(state))*(0.95**depth)


def minimize(state, depth=0, this_move=None): # finds move with minimum utility
  if depth == search_depth or gameover(state):
    return this_move, evaluate(state)*(0.95**depth)
  
  min_util = math.inf
  best_move = None

  for next_move in get_moves(state):
    child_state = make_move(state, HUMAN, next_move[0], next_move[1])
    check_move, check_util = maximize(child_state, depth+1, next_move)
    if check_util < min_util:
      best_move = check_move
      min_util = check_util
    if check_util == min_util:
      if random.random() < 0.2:
        best_move = check_move
  
  if this_move == None:
    return best_move, (min_util-evaluate(state))*(0.95**depth)
  else:
    return this_move, (min_util-evaluate(state))*(0.95**depth)


def render(state, h_choice="X", c_choice="O"): # display (and prettify) the board to the console
  chars = {
    0: " ",
    +1: c_choice,
    -1: h_choice
  }
  print("  " + '   '.join(map(str, list(range(1, width+1))))) # x axis labels

  for i, row in enumerate(state):
    print(f"{alphabet[i]} {' | '.join([chars[cell] for cell in row])}")
    if i+1 < height:
      print("  " + '-'*(width*4-3))


def clear(): # clears the console
  os_name = platform.system().lower()
  if 'windows' in os_name:
      system('cls')
  else:
      system('clear')


def parse_cords(raw_cords):
  try:
    raw_cords = raw_cords.upper()
    if raw_cords[0].isalpha() and raw_cords[1:].isdigit():
      return int(raw_cords[1:])-1, alphabet.index(raw_cords[0])
    elif raw_cords[:-1].isdigit() and raw_cords[-1].isalpha():
      return int(raw_cords[:-1])-1, alphabet.index(raw_cords[-1])
    else:
      print("Invalid syntax! Example: D3")
      return None
  except Exception:
    print("Invalid syntax! Example: D3")
    return None


def valid_move(state, x, y): # return if given cords are valid and position on board is empty
  try:
    if x in range(width) and y in range(height):
      if state[y][x] == 0:
        return True
      else:
        print("Given position is occupied!")
        return False
    else:
      print("Move is off the board!")
      return False
  except Exception:
    return False


def human_turn(state, recommend_moves): # takes user input and returns the board with their move made
  print("Your turn!")
  if recommend_moves:
    print("Recommending move...")
    recommended = minimize(state)[0]
    print(f"Recommended move: ({height-recommended[0]}, {recommended[1]+1})")

  cords = parse_cords(input("Enter cell coordinates, or type 'quit' to exit.\nMove: "))

  while not cords or not valid_move(state, cords[0], cords[1]):
    cords = input("Input move: ")
    if cords.upper() == "QUIT":
      sys.exit("Bye!")
    cords = parse_cords(cords)
  
  return make_move(state, HUMAN, cords[0], cords[1])


def main():
  clear()
  print("TicTac10")
  print(f"Size: {width}x{height}")
  print(f"Pegs in a row to win: {win_streak}")
  print(f"Search depth: {search_depth}")

  state = deepcopy(board)

  human_first = input("Do you want to go first? (Y/N): ").upper()
  while human_first not in ['Y', 'N']:
    human_first = input("Invalid input. (Y/N): ").upper()
  
  h_choice = input("Choose X or O: ").upper()
  while h_choice not in ['X', 'O']:
    h_choice = input("Invalid input. X/O: ").upper()

  if h_choice == 'X': # set computer to opposite peg
    c_choice = 'O'
  else:
    c_choice = 'X'

  recommend_moves = False
  # recommend_moves = input("Would you like me to recommend moves? (Y/N): ").upper()
  # while recommend_moves not in ['Y', 'N']:
  #   recommend_moves = input("Invalid input. (Y/N): ").upper()
  # recommend_moves = {'Y':True, 'N':False}[recommend_moves]

  play = True

  while play:
    clear()

    if human_first == 'Y':
      render(state, h_choice, c_choice)

      state = human_turn(state, recommend_moves)
      
    while not gameover(state):
      clear()
      render(state, h_choice, c_choice)

      print("Computer turn...")
      c_move = maximize(state)[0]
      state = make_move(state, COMP, c_move[0], c_move[1])

      clear()

      render(state, h_choice, c_choice)

      if gameover(state):
        break

      state = human_turn(state, recommend_moves)

      clear()

      render(state, h_choice, c_choice)

    if win(state, COMP):
      print("Computer wins!")
    if win(state, HUMAN):
      print("You win!")
    if len(empty_cells(state)) == 0:
      print("Draw!")
    
    retry = input("Do you want to retry? (Y/N): ").upper()
    while retry not in ['Y', 'N']:
      retry = input("Invalid input. (Y/N): ").upper()
    
    if retry == 'N':
      play = False
      print("Bye!")
    else:
      state = board

      human_first = input("Do you want to go first? (Y/N): ").upper()
      while human_first not in ['Y', 'N']:
        human_first = input("Invalid input. (Y/N): ").upper()

# if __name__ == "__main__":
#   main()

while True:
  render(board)

  board = human_turn(board, False)

  render(board)

  print(None in range(10))