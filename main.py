# Imports
from board import Board
import player
from os import system

def main():
    board = Board(3, 3, 3)

    playerX = player.HumanPlayer()
    playerO = player.BotPlayer('O', 6)
    
    while not board.gameover():
        board.render()
        moveX = playerX.get_move(board)
        board.set_move(moveX, 'X')

        if board.gameover(): break

        board.render()
        moveO = playerO.get_move(board)
        board.set_move(moveO, 'O')
        print(f"Computer Move: {moveO}")
    
    board.render()
    if len(board.possible_moves()) == 0:
        print('Draw!')
    elif board.iswin('X'):
        print('Player X has won!')
    elif board.iswin('O'):
        print('Player O has won!')

main()
