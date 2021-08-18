# Imports
from board import Board
import player

def main():
    board = Board(10, 10, 5)

    playerX = player.BotPlayer('X', 3)
    playerO = player.BotPlayer('O', 3)
    
    while not board.gameover():
        board.render()
        moveX = playerX.get_move(board)
        board.set_move(moveX, 'X')

        if board.gameover(): break

        board.render()
        moveO = playerO.get_move(board)
        board.set_move(moveO, 'O')
    
    board.render()
    if len(board.possible_moves()) == 0:
        print('Draw!')
    elif board.iswin('X'):
        print('Player X has won!')
    elif board.iswin('O'):
        print('Player O has won!')

main()
# board = Board(3, 3, 3)

# playerX = player.HumanPlayer()
# playerO = player.BotPlayer('O', 5)

# board.set_move((2,2), 'X')
# board.set_move((2,1), 'X')

# board.render()

# print(playerO.get_move(board))