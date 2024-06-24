import unittest

from src.board.move_flag import MoveFlag
from src.util.notation import fen_to_board, board_to_fen, move_to_notation, notation_to_move


class BoardTest(unittest.TestCase):

    def test_make_standard_move(self):
        self.make_unmake_move(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1",
            notation_to_move("g1f3"))

    def test_make_capture(self):
        self.make_unmake_move(
            "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
            "rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2",
            notation_to_move("e4d5"))

    def test_make_double_pawn_push(self):
        self.make_unmake_move(
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2",
            notation_to_move("c7c5", MoveFlag.DOUBLE_PAWN_PUSH))

    def test_make_en_passant(self):
        self.make_unmake_move(
            "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3",
            "rnbqkbnr/ppp1p1pp/5P2/3p4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 3",
            notation_to_move("e5f6", MoveFlag.EN_PASSANT))

    def test_make_kingside_castle_white(self):
        self.make_unmake_move(
            "r1bqk1nr/pppp1ppp/2n5/1Bb1p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
            "r1bqk1nr/pppp1ppp/2n5/1Bb1p3/4P3/5N2/PPPP1PPP/RNBQ1RK1 b kq - 5 4",
            notation_to_move("e1g1", MoveFlag.CASTLE))

    def test_make_kingside_castle_black(self):
        self.make_unmake_move(
            "rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R b KQkq - 0 4",
            "rnbq1rk1/pppp1ppp/5n2/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQ - 1 5",
            notation_to_move("e8g8", MoveFlag.CASTLE))

    def test_make_queenside_castle_white(self):
        self.make_unmake_move(
            "r3kbnr/pppqpppp/2n5/3p1b2/3P1B2/2N5/PPPQPPPP/R3KBNR w KQkq - 6 5",
            "r3kbnr/pppqpppp/2n5/3p1b2/3P1B2/2N5/PPPQPPPP/2KR1BNR b kq - 7 5",
            notation_to_move("e1c1", MoveFlag.CASTLE))

    def test_make_queenside_castle_black(self):
        self.make_unmake_move(
            "r3kbnr/pppqpppp/2n5/3p1b2/8/2N2NP1/PPPPPPBP/R1BQ1K1R b kq - 6 5",
            "2kr1bnr/pppqpppp/2n5/3p1b2/8/2N2NP1/PPPPPPBP/R1BQ1K1R w - - 7 6",
            notation_to_move("e8c8", MoveFlag.CASTLE))

    def test_make_queen_promotion(self):
        self.make_unmake_move(
            "rn1q1bnr/pppbkPpp/8/8/8/8/PPPP1PPP/RNBQKBNR w KQ - 1 5",
            "rn1q1bQr/pppbk1pp/8/8/8/8/PPPP1PPP/RNBQKBNR b KQ - 0 5",
            notation_to_move("f7g8q"))

    def test_make_rook_promotion(self):
        self.make_unmake_move(
            "rnbk1bnr/pp1Ppppp/8/8/8/8/PPPP1PPP/RNBQKBNR w KQ - 1 5",
            "rnRk1bnr/pp2pppp/8/8/8/8/PPPP1PPP/RNBQKBNR b KQ - 0 5",
            notation_to_move("d7c8r"))

    def test_make_bishop_promotion(self):
        self.make_unmake_move(
            "rnb1kb1r/pP2pppp/5n2/q7/8/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5",
            "Bnb1kb1r/p3pppp/5n2/q7/8/8/PPPP1PPP/RNBQKBNR b KQk - 0 5",
            notation_to_move("b7a8b"))

    def test_make_knight_promotion(self):
        self.make_unmake_move(
            "rnbqk1nr/ppp2ppp/8/4P3/1BP5/8/PP2KpPP/RN1Q1BNR b kq - 1 7",
            "rnbqk1nr/ppp2ppp/8/4P3/1BP5/8/PP2K1PP/RN1Q1BnR w kq - 0 8",
            notation_to_move("f2g1n"))

    def make_unmake_move(self, starting_fen, target_fen, move):
        board = fen_to_board(starting_fen)
        board.make_move(move)
        self.assertEqual(target_fen, board_to_fen(board))
        board.unmake_move()
        self.assertEqual(starting_fen, board_to_fen(board))

