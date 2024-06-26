from enum import Enum


class Piece(Enum):
    P = 0
    N = 1
    B = 2
    R = 3
    Q = 4
    K = 5

    def __int__(self):
        return self.value

    def is_slider(self):
        return self in [Piece.B, Piece.R, Piece.Q]
