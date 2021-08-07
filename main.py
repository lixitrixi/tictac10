# Imports
import sys
from getopt import getopt


# Vars
width, height = 10, 10
board = [ [+1 for y in range(height)] for x in range(width) ]

COMP = +1
HUMAN = -1

# Functions
def render(state):
  # displays board to console
  # state: current state of the board

  chars = {
    0: " ",
    +1: "X",
    -1: "O"
  }

  for row in state:
    print(' '.join([chars[cell] for cell in row]))

render(board)