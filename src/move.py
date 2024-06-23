from enum import Enum
from piece import Piece

class MoveFlag(Enum):
    STANDARD = 0
    DOUBLE_PAWN_PUSH = 1
    EN_PASSANT = 2
    CASTLE = 3
    PROMOTE_QUEEN = 4
    PROMOTE_ROOK = 5
    PROMOTE_BISHOP = 6
    PROMOTE_KNIGHT = 7


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

