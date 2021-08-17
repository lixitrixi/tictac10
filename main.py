# Imports
from board import Board
import player

board = Board(3, 3, 3)

playerX = player.HumanPlayer()
playerO = player.BotPlayer('O', 5)

while not board.gameover():
    board.render()
    moveX = playerX.get_move(board)
    board.set_move(moveX, 'X')

    if board.gameover(): break

    board.render()
    moveO = playerO.get_move(board)
    board.set_move(moveO, 'O')