import unittest

from src.board.board import Board
from src.board.move_flag import MoveFlag
from src.movegen.movegen import MoveGenerator
from src.util.notation import notation_to_move, fen_to_board
from tst import test_utils

movegen = MoveGenerator()

class CheckmateTest(unittest.TestCase):

    def test_fools_mate(self):
        board = Board()
        board.make_move(notation_to_move("f2f3"))
        board.make_move(notation_to_move("e7e5"))
        board.make_move(notation_to_move("g2g4"))
        board.make_move(notation_to_move("d8h4"))
        moves = movegen.generate_moves(board)
        self.assertEqual(0, len(moves))

    def test_scholars_mate(self):
        board = Board()
        board.make_move(notation_to_move("e2e4"))
        board.make_move(notation_to_move("e7e5"))
        board.make_move(notation_to_move("f1c4"))
        board.make_move(notation_to_move("b8c6"))
        board.make_move(notation_to_move("d1f3"))
        board.make_move(notation_to_move("g8f6"))
        board.make_move(notation_to_move("f3f7"))
        moves = movegen.generate_moves(board)
        self.assertEqual(0, len(moves))

    def test_discovered_checkmate(self):
        fen = "rn3r2/pbppq1p1/1p2pN2/8/3P2NP/6P1/PPP1BP1R/R3K1k1 w Q - 5 18"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("e1d2")))
        board.make_move(notation_to_move("e1d2"))
        moves = movegen.generate_moves(board)
        self.assertEqual(0, len(moves))

    def test_long_castles_checkmate(self):
        fen = "rn3r2/pbppq1p1/1p2pN2/8/3P2NP/6P1/PPP1BP1R/R3K1k1 w Q - 5 18"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("e1c1", MoveFlag.CASTLE)))
        board.make_move(notation_to_move("e1c1", MoveFlag.CASTLE))
        moves = movegen.generate_moves(board)
        self.assertEqual(0, len(moves))

    def test_en_passant_checkmate(self):
        fen = "rnbq1bnr/1pp1pk2/p2p3p/1B3Pp1/6Q1/1P6/PBPP1PPP/RN2K1NR w KQ g6 0 7"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("f5g6", MoveFlag.EN_PASSANT)))
        board.make_move(notation_to_move("f5g6", MoveFlag.EN_PASSANT))
        moves = movegen.generate_moves(board)
        self.assertEqual(0, len(moves))

    def test_knight_promotion_checkmate(self):
        fen = "rnbqkbnr/pppp1ppp/8/8/8/1P6/PKP1pPPP/RNBQ1BNR b kq - 1 5"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("e2d1", MoveFlag.PROMOTE_N)))
        board.make_move(notation_to_move("e2d1", MoveFlag.PROMOTE_N))
        moves = movegen.generate_moves(board)
        self.assertEqual(0, len(moves))
