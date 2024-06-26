import unittest

from src.board.move_flag import MoveFlag
from src.movegen.movegen import MoveGenerator
from src.util.notation import fen_to_board, notation_to_move
from tst import test_utils

movegen = MoveGenerator()


class CheckTest(unittest.TestCase):

    def test_check_blocks_other_moves(self):
        fen = "r1bqkbnr/pppp1Qpp/2n5/4p3/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertEqual(1, len(moves))
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("e8f7")))

    def test_cannot_move_pinned_pawn(self):
        fen = "rnbqkbnr/pppp1ppp/8/4p3/Q7/2P5/PP1PPPPP/RNB1KBNR b KQkq - 1 2"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("d7d6")))
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("d7d5")))

    def test_cannot_en_passant_with_pinned_pawn(self):
        fen = "rnb1kbnr/ppp1qppp/8/3pP3/3p4/5N2/PPP2PPP/RNBQKB1R w KQkq - 0 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e5d6", MoveFlag.EN_PASSANT)))

    def test_cannot_move_pinned_knight(self):
        fen = "rnbqkb1r/ppppn1pp/8/5p2/3P4/5N2/PPP1QPPP/RNB1KB1R b KQkq - 3 5"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e7d5")))
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e7f5")))
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e7c6")))
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e7g6")))

    def test_cannot_move_from_check_into_another_check(self):
        fen = "rnb1kbnr/pppp1Qpp/8/4p3/4P2q/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e8e7")))

    def test_cannot_capture_protected_checker_with_king(self):
        fen = "r1b1kbnr/ppppqQpp/2n5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e8f7")))

    def test_can_capture_protected_checker_other_piece(self):
        fen = "r1b1kbnr/ppppqQpp/2n5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("e7f7")))

    def test_cannot_castle_out_of_check(self):
        fen = "rnbqk2r/ppp2ppp/3b1n2/3p4/3P4/3B1N2/PPP1QPPP/RNB1K2R b KQkq - 5 6"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e8g8", MoveFlag.CASTLE)))

    def test_cannot_castle_through_check(self):
        fen = "rn1qkbnr/p1p2ppp/bp1p4/4p3/4PP2/5N2/PPPP2PP/RNBQK2R w KQkq - 0 5"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e1g1", MoveFlag.CASTLE)))

    def test_cannot_castle_queenside_through_knight_check(self):
        fen = "r3k2r/p1ppqpb1/bnN1pnp1/3P4/1p2P3/2N2Q1p/PPPBBPPP/R3K2R b KQkq - 1 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("e8c8", MoveFlag.CASTLE)))

    def test_cannot_step_king_back_on_ray_of_orthogonal_checker(self):
        fen = "8/8/8/2k5/2r2K2/8/8/8 w - - 0 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("f4g4")))

    def test_cannot_step_king_back_on_ray_of_diagonal_checker(self):
        fen = "8/8/3b4/2k5/5K2/8/8/8 w - - 0 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("f4g3")))

    def test_cannot_en_passant_into_check(self):
        fen = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
        board = fen_to_board(fen)
        board.make_move(notation_to_move("e2e4"))
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("f4e3", MoveFlag.EN_PASSANT)))

    def test_can_en_passant_checking_pawn(self):
        fen = "8/2p5/3p4/1P4r1/1K3p1k/8/4P1P1/1R6 b - - 3 2"
        board = fen_to_board(fen)
        board.make_move(notation_to_move("c7c5", MoveFlag.DOUBLE_PAWN_PUSH))
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("b5c6", MoveFlag.EN_PASSANT)))

    def test_must_block_queen_check(self):
        fen = "r3kbnr/p2n1ppp/8/8/3PQ3/8/PPP2PPP/R1B1K2R b KQkq - 0 12"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("g8f6")))

    def test_pinned_orthogonal_slider_can_step_forward_in_the_ray(self):
        fen = "6k1/8/3r4/8/8/8/3R4/3K4 w - - 0 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("d2d3")))
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("d2d6")))

    def test_pinned_orthogonal_slider_can_step_backward_in_the_ray(self):
        fen = "6k1/8/3r4/3R4/8/8/8/3K4 w - - 0 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("d5d4")))
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("d5d3")))

    def test_pinned_diagonal_slider_can_step_forward_in_the_ray(self):
        fen = "6k1/8/8/7q/8/5B2/8/3K4 w - - 0 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("f3g4")))
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("f3h5")))

    def test_pinned_diagonal_slider_can_step_backward_in_the_ray(self):
        fen = "6k1/8/8/7q/6B1/8/8/3K4 w - - 0 1"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("g4f3")))
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("g4e2")))

    def test_can_block_check_with_pawn_push(self):
        fen = "rnbqkbnr/ppp1pppp/3p4/8/Q7/2P5/PP1PPPPP/RNB1KBNR b KQkq - 1 2"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("b7b5", MoveFlag.DOUBLE_PAWN_PUSH)))

    def test_king_cannot_move_into_rook_check(self):
        fen = "r5k1/5b2/q2p4/p2nn1P1/2p5/P3P3/1PB2PK1/2BR3R b - - 2 42"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertFalse(test_utils.contains_move(moves, notation_to_move("g8h8")))

    def test_can_capture_the_checking_diagonal_slider(self):
        fen = "rnbqk1nr/pppp1ppp/8/4p3/1b1P4/P7/1PP1PPPP/RNBQKBNR w KQkq - 1 3"
        board = fen_to_board(fen)
        moves = movegen.generate_moves(board)
        self.assertTrue(test_utils.contains_move(moves, notation_to_move("a3b4")))