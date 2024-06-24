def lsb(bb):
    return bb & -bb


def pop_bit(bb):
    bit = lsb(bb)
    bb &= ~bit
    return bit


def shift_north(bb):
    return bb << 8


def shift_north_east(bb):
    return (bb & 0x7F7F7F7F7F7F7F7F) << 9


def shift_east(bb):
    return (bb & 0xFEFEFEFEFEFEFEFE) << 1


def shift_south_east(bb):
    return (bb & 0xFEFEFEFEFEFEFEFE) >> 7


def shift_south(bb):
    return bb >> 8


def shift_south_west(bb):
    return (bb & 0x7F7F7F7F7F7F7F7F) >> 9


def shift_west(bb):
    return (bb & 0x7F7F7F7F7F7F7F7F) >> 1


def shift_north_west(bb):
    return (bb & 0xFEFEFEFEFEFEFEFE) << 7
