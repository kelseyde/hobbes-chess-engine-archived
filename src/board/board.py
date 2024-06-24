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

        piece = self.piece_list[move.start_sq]
        captured_piece = Piece.P if move.is_en_passant() else self.piece_list[move.end_sq]
        match move.flag:
            case MoveFlag.STANDARD:
                self.make_standard_move(move)
            case MoveFlag.DOUBLE_PAWN_PUSH:
                self.make_double_pawn_push(move)
            case MoveFlag.EN_PASSANT:
                self.make_en_passant(move)
            case MoveFlag.CASTLE:
                self.make_castle(move)
            case MoveFlag.PROMOTE_Q | MoveFlag.PROMOTE_R | MoveFlag.PROMOTE_B | MoveFlag.PROMOTE_N:
                self.make_promotion(move)

        self.game_state_history.append(self.game_state)
        self.game_state = self.compute_game_state(move, piece, captured_piece)
        self.move_history.append(move)
        self.colour = Colour.WHITE if self.colour == Colour.BLACK else Colour.BLACK

    def unmake_move(self):
        move = self.move_history.pop()
        self.colour = Colour.WHITE if self.colour == Colour.BLACK else Colour.BLACK
        match move.flag:
            case MoveFlag.STANDARD:
                self.unmake_standard_move(move)
            case MoveFlag.DOUBLE_PAWN_PUSH:
                self.unmake_double_pawn_push(move)
            case MoveFlag.EN_PASSANT:
                self.unmake_en_passant(move)
            case MoveFlag.CASTLE:
                self.unmake_castle(move)
            case MoveFlag.PROMOTE_Q | MoveFlag.PROMOTE_R | MoveFlag.PROMOTE_B | MoveFlag.PROMOTE_N:
                self.unmake_promotion(move)

        self.game_state = self.game_state_history.pop()

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
        kingside = Board.file(move.end_sq) == 6
        rook_start_sq, rook_end_sq = \
            ((7, 5) if self.is_white() else (63, 61)) if kingside \
            else ((0, 3) if self.is_white() else (56, 59))
        self.toggle_squares(Piece.R, self.colour, rook_start_sq, rook_end_sq)

    def make_promotion(self, move):
        piece = move.get_promotion_piece()
        captured_piece = self.piece_list[move.end_sq]
        if captured_piece is not None:
            self.toggle_square(captured_piece, ~self.colour, move.end_sq)
        self.toggle_square(Piece.P, self.colour, move.start_sq)
        self.toggle_square(piece, self.colour, move.end_sq)

    def unmake_standard_move(self, move):
        piece = self.piece_list[move.end_sq]
        captured_piece = self.game_state.captured_piece
        self.toggle_squares(piece, self.colour, move.end_sq, move.start_sq)
        if captured_piece is not None:
            self.toggle_square(captured_piece, ~self.colour, move.end_sq)

    def unmake_double_pawn_push(self, move):
        self.toggle_squares(Piece.P, self.colour, move.end_sq, move.start_sq)

    def unmake_en_passant(self, move):
        self.toggle_squares(Piece.P, self.colour, move.end_sq, move.start_sq)
        pawn_sq = move.end_sq - 8 if self.colour == Colour.WHITE else move.end_sq + 8
        self.toggle_square(Piece.P, ~self.colour, pawn_sq)

    def unmake_castle(self, move):
        self.toggle_squares(Piece.K, self.colour, move.end_sq, move.start_sq)
        kingside = Board.file(move.end_sq) == 6
        rook_start_sq, rook_end_sq = \
            ((7, 5) if self.is_white() else (63, 61)) if kingside \
            else ((0, 3) if self.is_white() else (56, 59))
        self.toggle_squares(Piece.R, self.colour, rook_end_sq, rook_start_sq)

    def unmake_promotion(self, move):
        captured_piece = self.game_state.captured_piece
        self.toggle_squares(Piece.P, self.colour, move.end_sq, move.start_sq)
        if captured_piece is not None:
            self.toggle_square(captured_piece, ~self.colour, move.end_sq)

    def compute_game_state(self, move, piece, captured_piece):
        old_halfmove_clock = self.game_state.halfmove_clock
        new_halfmove_clock = 0 if captured_piece or piece == Piece.P else old_halfmove_clock + 1

        old_fullmove_number = self.game_state.fullmove_number
        new_fullmove_number = old_fullmove_number + 1 if self.colour == Colour.BLACK else old_fullmove_number

        old_castle_rights = self.game_state.castle_rights
        new_castle_rights = self.compute_castle_rights(move, piece)

        old_ep_file = self.game_state.ep_file
        new_ep_file = Board.file(move.end_sq) if move.is_double_pawn_push() else -1

        old_key = self.game_state.key
        new_key = zobrist.update_key(old_key, self, move, piece, old_castle_rights, new_castle_rights, old_ep_file, new_ep_file)

        return GameState(new_key, captured_piece, new_halfmove_clock, new_fullmove_number, new_castle_rights, new_ep_file)

    def compute_castle_rights(self, move, piece):
        start_sq = move.start_sq
        end_sq = move.end_sq
        castle_rights = self.game_state.castle_rights
        if castle_rights == 0:
            return 0
        if piece == Piece.K:
            castle_rights &= bits.clear_white_rights if self.is_white() else bits.clear_black_rights
        if start_sq == 7 or end_sq == 7:
            castle_rights &= bits.clear_white_kingside_rights
        elif start_sq == 0 or end_sq == 0:
            castle_rights &= bits.clear_white_queenside_rights
        elif start_sq == 63 or end_sq == 63:
            castle_rights &= bits.clear_black_kingside_rights
        elif start_sq == 56 or end_sq == 56:
            castle_rights &= bits.clear_black_queenside_rights
        return castle_rights

    def toggle_square(self, piece, colour, square):
        mask = 1 << square
        self.piece_bbs[piece.value] ^= mask
        self.all_bbs[colour.value] ^= mask
        self.all_bbs[Colour.ALL.value] ^= mask
        self.piece_list[square] = piece if self.piece_list[square] is None else None

    def toggle_squares(self, piece, colour, start_sq, end_sq):
        self.toggle_square(piece, colour, start_sq)
        self.toggle_square(piece, colour, end_sq)

    def piece_at(self, square):
        return self.piece_list[square]

    def colour_at(self, square):
        if self.all_bbs[0] & (1 << square):
            return Colour.WHITE
        elif self.all_bbs[1] & (1 << square):
            return Colour.BLACK
        else:
            return None

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
