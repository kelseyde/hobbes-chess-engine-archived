import src.board.bits as bits
import src.board.zobrist as zobrist
from src.board.piece import Piece
from src.board.colour import Colour
from src.board.move_flag import MoveFlag
from src.board.game_state import GameState


class Board:

    def __init__(self):
        self.piece_bbs = bits.piece_bbs
        self.all_bbs = bits.all_bbs
        self.piece_list = bits.start_piece_list
        self.colour = Colour.WHITE
        self.move_history = []
        self.game_state = GameState()
        self.game_state.key = zobrist.generate_key(self)
        self.game_state_history = []

    def make_move(self, move):

        match move.flag:
            case MoveFlag.STANDARD:
                self.make_standard_move(move)
            case MoveFlag.DOUBLE_PAWN_PUSH:
                self.make_double_pawn_push(move)
            case MoveFlag.EN_PASSANT:
                self.make_en_passant(move)
            case MoveFlag.CASTLE:
                self.make_castle(move)
            case MoveFlag.PROMOTE_QUEEN, MoveFlag.PROMOTE_ROOK, MoveFlag.PROMOTE_BISHOP, MoveFlag.PROMOTE_KNIGHT:
                self.make_promotion(move)

        self.move_history.append(move)
        self.colour = Colour.WHITE if self.colour == Colour.BLACK else Colour.BLACK

    def unmake_move(self, move):

        match move.flag:
            case MoveFlag.STANDARD:
                self.unmake_standard_move(move)
            case MoveFlag.DOUBLE_PAWN_PUSH:
                self.unmake_double_pawn_push(move)
            case MoveFlag.EN_PASSANT:
                self.unmake_en_passant(move)
            case MoveFlag.CASTLE:
                self.unmake_castle(move)
            case MoveFlag.PROMOTE_QUEEN, MoveFlag.PROMOTE_ROOK, MoveFlag.PROMOTE_BISHOP, MoveFlag.PROMOTE_KNIGHT:
                self.unmake_promotion(move)

        self.move_history.pop()
        self.colour = Colour.WHITE if self.colour == Colour.BLACK else Colour.BLACK

    def make_standard_move(self, move):
        piece = self.piece_list[move.start_sq]
        captured_piece = self.piece_list[move.end_sq]
        if captured_piece is not None:
            self.toggle_square(captured_piece, ~self.colour, move.end_sq)
        self.toggle_squares(piece, self.colour, move.start_sq, move.end_sq)

    def make_double_pawn_push(self, move):
        self.toggle_squares(Piece.P, self.colour, move.start_sq, move.end_sq)

    def make_en_passant(self, move):
        self.toggle_squares(Piece.P, self.colour, move.start_sq, move.end_sq)
        pawn_sq = move.end_sq - 8 if self.colour == Colour.WHITE else move.end_sq + 8
        self.toggle_square(Piece.P, ~self.colour, pawn_sq)

    def make_castle(self, move):
        self.toggle_squares(Piece.K, self.colour, move.start_sq, move.end_sq)
        kingside = move.end_sq == 6
        rook_start_sq = (7 if self.is_white() else 63) if kingside else (0 if self.is_white() else 56)
        rook_end_sq = (5 if self.is_white() else 61) if kingside else (3 if self.is_white() else 59)
        self.toggle_squares(Piece.R, self.colour, rook_start_sq, rook_end_sq)

    def make_promotion(self, move):
        piece = move.get_promotion_piece()
        captured_piece = self.piece_list[move.end_sq]
        if captured_piece is not None:
            self.toggle_square(captured_piece, ~self.colour, move.end_sq)
        self.toggle_squares(piece, self.colour, move.start_sq, move.end_sq)

    def unmake_standard_move(self, move):
        pass

    def unmake_double_pawn_push(self, move):
        pass

    def unmake_en_passant(self, move):
        pass

    def unmake_castle(self, move):
        pass

    def unmake_promotion(self, move):
        pass

    def toggle_square(self, piece, colour, square):
        mask = 1 << square
        self.piece_bbs[piece] ^= mask
        self.all_bbs[colour] ^= mask
        self.all_bbs[Colour.ALL] ^= mask
        self.piece_list[square] = piece if self.piece_list[square] is None else None

    def toggle_squares(self, piece, colour, start_sq, end_sq):
        self.toggle_square(piece, colour, start_sq)
        self.toggle_square(piece, colour, end_sq)

    def piece_at(self, square):
        return self.piece_list[square]

    def is_white(self):
        return self.colour == Colour.WHITE

    def print_board(self):
        board_str = ''
        for rank in range(7, -1, -1):
            for file in range(8):
                square = self.square_index(file, rank)
                piece = self.piece_at(square)
                if piece is not None:
                    colour = Colour.WHITE if self.all_bbs[0] & (1 << square) else Colour.BLACK
                    board_str += bits.piece_unicode[(piece, colour)]
                else:
                    board_str += '·'
                board_str += ' '
            board_str += '\n'

        print(board_str)

    @staticmethod
    def file(square):
        return square % 8

    @staticmethod
    def rank(square):
        return square // 8

    @staticmethod
    def diagonal(square):
        return (square % 8) - (square // 8)

    @staticmethod
    def anti_diagonal(square):
        return (square % 8) + (square // 8)

    @staticmethod
    def square_index(file, rank):
        return 8 * rank + file







