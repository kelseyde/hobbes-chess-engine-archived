import unittest

from src.board.board import Board
from src.util.notation import fen_to_board, board_to_fen


class NotationTest(unittest.TestCase):

    def test_fen_starting_position(self):
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        board = fen_to_board(fen)
        board.print_board()
        self.assert_board(board, Board())
        new_fen = board_to_fen(board)
        self.assertEqual(fen, new_fen)

    def test_fen_en_passant(self):
        fen = 'rnbqkbnr/1pp1pppp/p7/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'
        board = fen_to_board(fen)
        board.print_board()
        new_fen = board_to_fen(board)
        self.assertEqual(fen, new_fen)

    def test_fen_castle_rights(self):
        fen = 'r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1 b kq - 5 4'
        board = fen_to_board(fen)
        board.print_board()
        new_fen = board_to_fen(board)
        self.assertEqual(fen, new_fen)

    def test_fen_promotion(self):
        fen = 'Qnbqkb1r/p4ppp/4pn2/8/8/8/PPPP1PPP/RNBQKBNR b KQk - 0 5'
        board = fen_to_board(fen)
        board.print_board()
        new_fen = board_to_fen(board)
        self.assertEqual(fen, new_fen)

    def assert_board(self, actual, expected):
        self.assertEqual(actual.piece_bbs, expected.piece_bbs)
        self.assertEqual(actual.all_bbs, expected.all_bbs)
        self.assertEqual(actual.piece_list, expected.piece_list)
        self.assertEqual(actual.move_history, expected.move_history)
        self.assertEqual(actual.game_state.key, expected.game_state.key)
        self.assertEqual(actual.game_state.castle_rights, expected.game_state.castle_rights)
        self.assertEqual(actual.game_state.ep_file, expected.game_state.ep_file)
        self.assertEqual(actual.game_state.halfmove_clock, expected.game_state.halfmove_clock)
        self.assertEqual(actual.game_state_history, expected.game_state_history)
        self.assertEqual(actual.colour, expected.colour)