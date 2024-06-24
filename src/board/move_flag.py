from enum import Enum


class MoveFlag(Enum):
    STANDARD = 0
    DOUBLE_PAWN_PUSH = 1
    EN_PASSANT = 2
    CASTLE = 3
    PROMOTE_Q = 4
    PROMOTE_R = 5
    PROMOTE_B = 6
    PROMOTE_N = 7
