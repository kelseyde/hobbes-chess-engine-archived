from src.board.move_flag import MoveFlag
from src.board.piece import Piece


class Move:

    def __init__(self, start_sq, end_sq, flag=MoveFlag.STANDARD):
        self.start_sq = start_sq
        self.end_sq = end_sq
        self.flag = flag

    def get_promotion_piece(self):
        match self.flag:
            case MoveFlag.PROMOTE_Q:
                return Piece.Q
            case MoveFlag.PROMOTE_R:
                return Piece.R
            case MoveFlag.PROMOTE_B:
                return Piece.B
            case MoveFlag.PROMOTE_N:
                return Piece.N
            case _:
                return None

    def is_en_passant(self):
        return self.flag == MoveFlag.EN_PASSANT

    def is_castle(self):
        return self.flag == MoveFlag.CASTLE

    def is_double_pawn_push(self):
        return self.flag == MoveFlag.DOUBLE_PAWN_PUSH

    def is_promotion(self):
        return self.flag in {MoveFlag.PROMOTE_Q, MoveFlag.PROMOTE_R, MoveFlag.PROMOTE_B, MoveFlag.PROMOTE_N}

