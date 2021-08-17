import string
from copy import deepcopy

alphabet = list(string.ascii_uppercase)

class Board():
    def __init__(self, width, height, winstreak):
        self.width = width
        self.height = height
        self.winstreak = winstreak
        self.board = [ [' ' for x in range(width)] for y in range(height) ] # creates an array of empty cells with given dimensions
    
    def reset(self): # resets the board to be empty
        self.board = [ [' ' for x in range(self.width)] for y in range(self.height) ]
    
    def set_move(self, pos, player): # sets a move onto the board
        self.board[pos[1]][pos[0]] = player

    def possible_moves(self): # returns list of all empty cells' (x, y)
        moves = []

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == ' ':
                    moves.append((x, y))

        return moves
    
    def gameover(self): # returns True if board is full or either player has won
        return len(self.possible_moves()) == 0 or self.iswin('X') or self.iswin('O')

    def iswin(self, player): # checks if a given player has won
        for y in range(self.height-self.winstreak+1): # check \ diagonals
            for x in range(self.width-self.winstreak+1):
                if all([self.board[y+i][x+i] == player for i in range(self.winstreak)]): # checks if all cells in a row have the player's peg
                    return True
        
        for y in range(self.winstreak-1,self.height): # check / diagonals
            for x in range(self.width-self.winstreak+1):
                if all([self.board[y-i][x+i] == player for i in range(self.winstreak)]):
                    return True
        
        for y in range(self.height): # check horizontals
            for x in range(self.width-self.winstreak+1):
                if all([self.board[y][x+i] == player for i in range(self.winstreak)]):
                    return True
        
        for y in range(self.height-self.winstreak+1): # check verticals
            for x in range(self.width):
                if all([self.board[y-i][x] == player for i in range(self.winstreak)]):
                    return True

        return False
    
    def evaluate(self, player):
        other_player = 'O' if player == 'X' else 'X'
        if self.iswin(player):
            return (len(self.possible_moves()) + 1)
        elif self.iswin(other_player):
            return -(len(self.possible_moves()) + 1)
        else:
            return 0
    
    def render(self): # displays to terminal

        print(f"  {'   '.join([str(i+1) for i in range(self.width)])}")

        for index, row in enumerate(self.board):
            print(f"{alphabet[index]} {' | '.join(row)}")
            if index + 1 < self.height:
                print("  " + '-'*(self.width*4-3))