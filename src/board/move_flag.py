from enum import Enum


class MoveFlag(Enum):
    STANDARD = 0
    DOUBLE_PAWN_PUSH = 1
    EN_PASSANT = 2
    CASTLE = 3
    PROMOTE_QUEEN = 4
    PROMOTE_ROOK = 5
    PROMOTE_BISHOP = 6
    PROMOTE_KNIGHT = 7
