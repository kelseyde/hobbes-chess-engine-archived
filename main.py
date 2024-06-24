from src.board.board import Board
from src.board.move import Move
from src.util.notation import notation_to_move

board = Board()
board.print_board()
board.make_move(notation_to_move("e2e4"))
board.print_board()
board.make_move(notation_to_move("e7e5"))
board.print_board()