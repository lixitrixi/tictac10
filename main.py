# Imports
from board import Board
import player
from os import system

def main():
    board = Board(5, 5, 5)

    playerX = player.HumanPlayer()
    playerO = player.BotPlayer('O', 6)
    
    while not board.gameover():
        board.render()
        moveX = playerX.get_move(board)
        board.set_move(moveX, 'X')
        system('clear')

        if board.gameover(): break

        board.render()
        moveO = playerO.get_move(board)
        board.set_move(moveO, 'O')
        system('clear')
    
    board.render()
    if len(board.possible_moves()) == 0:
        print('Draw!')
    elif board.iswin('X'):
        print('Player X has won!')
    elif board.iswin('O'):
        print('Player O has won!')

main()
