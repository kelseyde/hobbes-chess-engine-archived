from enum import Enum


class Colour(Enum):
    W = 0
    B = 1
    ALL = 2

    def __invert__(self):
        match self:
            case Colour.W:
                return Colour.B
            case Colour.B:
                return Colour.W
            case Colour.ALL:
                return Colour.ALL

    def __int__(self):
        return self.value

    def __bool__(self):
        match self:
            case Colour.W:
                return True
            case Colour.B:
                return False
            case Colour.ALL:
                return None

