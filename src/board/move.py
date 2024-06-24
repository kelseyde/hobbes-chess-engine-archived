import src.board.bits as bits

from src.board.board import Board
from src.board.move_flag import MoveFlag
from src.board.piece import Piece


class Move:

    def __init__(self, start_sq, end_sq, flag=MoveFlag.STANDARD):
        self.start_sq = start_sq
        self.end_sq = end_sq
        self.flag = flag

    def get_promotion_piece(self):
        match self.flag:
            case MoveFlag.PROMOTE_QUEEN:
                return Piece.Q
            case MoveFlag.PROMOTE_ROOK:
                return Piece.R
            case MoveFlag.PROMOTE_BISHOP:
                return Piece.B
            case MoveFlag.PROMOTE_KNIGHT:
                return Piece.N
            case _:
                return None

    def to_notation(self):

        start_file = bits.file_map[Board.file(self.start_sq)]
        start_rank = bits.rank_map[Board.rank(self.start_sq)]
        end_file = bits.file_map[Board.file(self.end_sq)]
        end_rank = bits.rank_map[Board.rank(self.end_sq)]

        promotion_piece = self.get_promotion_piece()
        promotion_suffix = ''

        if promotion_piece:
            promotion_suffix = promotion_piece.name.lower()

        return f"{start_file}{start_rank}{end_file}{end_rank}{promotion_suffix}"

    @staticmethod
    def from_chess_notation(notation):
        start_file = notation[0]
        start_rank = notation[1]
        end_file = notation[2]
        end_rank = notation[3]

        start_sq = Board.square_index(bits.file_map.index(start_file), bits.rank_map.index(start_rank))
        end_sq = Board.square_index(bits.file_map.index(end_file), bits.rank_map.index(end_rank))

        promotion_suffix = notation[4] if len(notation) > 4 else ''

        if promotion_suffix == 'q':
            flag = MoveFlag.PROMOTE_QUEEN
        elif promotion_suffix == 'r':
            flag = MoveFlag.PROMOTE_ROOK
        elif promotion_suffix == 'b':
            flag = MoveFlag.PROMOTE_BISHOP
        elif promotion_suffix == 'n':
            flag = MoveFlag.PROMOTE_KNIGHT
        else:
            flag = MoveFlag.STANDARD

        return Move(start_sq, end_sq, flag)

