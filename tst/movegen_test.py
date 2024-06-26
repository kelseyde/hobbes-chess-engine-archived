import unittest

from src.board.board import Board
from src.board.move_flag import MoveFlag
from src.movegen.movegen import MoveGenerator
from src.util.notation import move_to_notation, fen_to_board, notation_to_move
from tst import test_utils

movegen = MoveGenerator()


class MoveGenTest(unittest.TestCase):

    def test_starting_position(self):
        board = Board()
        moves = movegen.generate_moves(board)
        print([move_to_notation(move) for move in moves])
        self.assertEqual(20, len(moves))

    def test_white_kingside_castles(self):
        fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.is_legal_move(board, notation_to_move("e1g1", MoveFlag.CASTLE)))
        print([move_to_notation(move) for move in moves])

    def test_white_queenside_castles(self):
        fen = "rnbq1rk1/pp3pbp/2pp1np1/3Pp3/4P3/2N1BP2/PPPQ2PP/R3KBNR w KQ - 0 8"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.is_legal_move(board, notation_to_move("e1c1", MoveFlag.CASTLE)))
        print([move_to_notation(move) for move in moves])

    def test_black_kingside_castles(self):
        fen = "rnbqk2r/ppp1ppbp/3p1np1/8/3PP3/2N1BP2/PPP3PP/R2QKBNR b KQkq - 0 5"
        board = fen_to_board(fen)
        self.assertTrue(test_utils.is_legal_move(board, notation_to_move("e8g8", MoveFlag.CASTLE)))

    def test_black_queenside_castles(self):
        pass

    def test_white_right_en_passant(self):
        pass

    def test_white_left_en_passant(self):
        pass

    def test_black_right_en_passant(self):
        pass

    def test_black_left_en_passant(self):
        pass

    def test_queen_moves(self):
        fen = "5k2/4b3/8/8/8/2Q5/8/5K2 w - - 0 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_all([
            notation_to_move("c3h8"),
            notation_to_move("c3g7"),
            notation_to_move("c3f6"),
            notation_to_move("c3e5"),
            notation_to_move("c3d4"),
            notation_to_move("c3a1"),
            notation_to_move("c3b2"),
            notation_to_move("c3c1"),
            notation_to_move("c3c2"),
            notation_to_move("c3c4"),
            notation_to_move("c3c5"),
            notation_to_move("c3c6"),
            notation_to_move("c3c7"),
            notation_to_move("c3c8"),
            notation_to_move("c3b3"),
            notation_to_move("c3a3"),
            notation_to_move("c3d3"),
            notation_to_move("c3e3"),
            notation_to_move("c3f3"),
            notation_to_move("c3g3"),
            notation_to_move("c3h3")
        ], moves))

    def test_knight_moves(self):
        fen = "1k6/8/4N3/N7/8/4N3/8/5K2 w - - 0 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_all([
            notation_to_move("e3d1"),
            notation_to_move("e3c2"),
            notation_to_move("e3c4"),
            notation_to_move("e3d5"),
            notation_to_move("e3f5"),
            notation_to_move("e3g4"),
            notation_to_move("e3g2"),
            notation_to_move("e6f8"),
            notation_to_move("e6d8"),
            notation_to_move("e6d4"),
            notation_to_move("e6f4"),
            notation_to_move("e6g5"),
            notation_to_move("e6g7"),
            notation_to_move("e6c5"),
            notation_to_move("e6c7"),
            notation_to_move("a5b3"),
            notation_to_move("a5c4"),
            notation_to_move("a5c6"),
            notation_to_move("a5b7")
        ], moves))

    def test_pawn_captures(self):
        fen = "rnbqkbnr/1ppppppp/p7/1N6/8/8/PPPPPPPP/R1BQKBNR b KQkq - 1 2"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        print([move_to_notation(move) for move in moves])
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("c6b5")))
