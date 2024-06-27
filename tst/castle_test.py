import unittest

from src.board.board import Board
from src.board.move_flag import MoveFlag
from src.movegen.movegen import MoveGenerator
from src.util.notation import fen_to_board, notation_to_move
from tst import test_utils

movegen = MoveGenerator()

class CastleTest(unittest.TestCase):

    def test_cannot_castle_with_piece_in_the_way(self):
        fen = "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e1g1", MoveFlag.CASTLE)))

    def test_cannot_castle_if_rook_has_moved(self):
        board = Board()
        board.make_move(notation_to_move("e2e4"))
        board.make_move(notation_to_move("e7e5"))
        board.make_move(notation_to_move("g1f3"))
        board.make_move(notation_to_move("g8f6"))
        board.make_move(notation_to_move("f1e2"))
        board.make_move(notation_to_move("f8e7"))
        board.make_move(notation_to_move("h1g1"))
        board.make_move(notation_to_move("h8g8"))
        board.make_move(notation_to_move("g1h1"))
        board.make_move(notation_to_move("g8h8"))
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e1g1", MoveFlag.CASTLE)))

    def test_cannot_castle_if_king_has_moved(self):
        board = Board()
        board.make_move(notation_to_move("e2e4"))
        board.make_move(notation_to_move("e7e5"))
        board.make_move(notation_to_move("g1f3"))
        board.make_move(notation_to_move("g8f6"))
        board.make_move(notation_to_move("e1f1"))
        board.make_move(notation_to_move("e8f8"))
        board.make_move(notation_to_move("f1e1"))
        board.make_move(notation_to_move("f8e8"))
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e1g1", MoveFlag.CASTLE)))

    def test_cannot_castle_if_king_not_on_starting_square(self):
        board = Board()
        board.make_move(notation_to_move("e2e4"))
        board.make_move(notation_to_move("e7e5"))
        board.make_move(notation_to_move("g1f3"))
        board.make_move(notation_to_move("g8f6"))
        board.make_move(notation_to_move("e1f1"))
        board.make_move(notation_to_move("e8f8"))
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e1g1", MoveFlag.CASTLE)))

    def test_cannot_castle_if_rook_is_captured(self):
        fen = "r1b1k2r/1p3p2/8/3n4/1P6/2Q5/4P3/6KR b kq - 0 9"
        board = fen_to_board(fen)
        board.make_move(notation_to_move("h8h1"))
        board.make_move(notation_to_move("g1h1"))
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e8g8", MoveFlag.CASTLE)))

    def test_kiwipete_castles(self):
        fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        board = fen_to_board(fen)
        board.make_move(notation_to_move("e2a6"))
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("e8g8", MoveFlag.CASTLE)))
