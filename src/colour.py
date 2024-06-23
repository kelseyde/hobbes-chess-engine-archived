from enum import Enum


class Colour(Enum):
    WHITE = 0
    BLACK = 1
    ALL = 2

    def __invert__(self):
        match self:
            case Colour.WHITE:
                return Colour.BLACK
            case Colour.BLACK:
                return Colour.WHITE
            case Colour.ALL:
                return Colour.ALL

