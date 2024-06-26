from src.board.board import Board
from src.board.colour import Colour
from src.util.notation import notation_to_move

print(int(Colour.W))
print(int(Colour.B))
print(int(Colour.ALL))

print(int(~Colour.W))
print(int(~Colour.B))
print(int(~Colour.ALL))

board = Board()
board.print_board()
board.make_move(notation_to_move("e2e4"))
board.print_board()
board.make_move(notation_to_move("e7e5"))
board.print_board()