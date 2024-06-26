import src.board.bits as bits

from src.board.colour import Colour


def lsb(bb):
    return (bb & -bb).bit_length() - 1


def pop_bit(bb):
    return bb & (bb - 1)


def shift_north(bb):
    return bb << 8


def shift_north_east(bb):
    return (bb << 9) & ~bits.files[0]


def shift_east(bb):
    return (bb << 1) & ~bits.files[0]


def shift_south_east(bb):
    return (bb >> 7) & ~bits.files[0]


def shift_south(bb):
    return bb >> 8


def shift_south_west(bb):
    return (bb >> 9) & ~bits.files[7]


def shift_west(bb):
    return (bb >> 1) & ~bits.files[7]


def shift_north_west(bb):
    return (bb << 7) & ~bits.files[7]


def pawn_pushes(board, colour):
    pawns = board.pawns(colour)
    empty = ~board.occupied()
    single_pushes = (shift_north(pawns) if colour == Colour.W else shift_south(pawns)) & empty
    return single_pushes


def pawn_double_pushes(board, colour):
    pawns = board.pawns(colour)
    empty = ~board.occupied()
    rank_mask = bits.ranks[1 if colour == Colour.W else 6]
    single_pushes = (shift_north(pawns & rank_mask) if colour == Colour.W else shift_south(pawns & rank_mask)) & empty
    double_pushes = (shift_north(single_pushes) if colour == Colour.W else shift_south(single_pushes)) & empty
    return double_pushes


def pawn_right_captures(board, colour):
    pawns = board.pawns(colour)
    opponents = board.opponents(colour)
    right_captures = (shift_north_east(pawns) if colour == Colour.W else shift_south_east(pawns)) & opponents
    return right_captures


def pawn_left_captures(board, colour):
    pawns = board.pawns(colour)
    opponents = board.opponents(colour)
    left_captures = (shift_north_west(pawns) if colour == Colour.W else shift_south_west(pawns)) & opponents
    return left_captures


def pawn_right_en_passants(board, colour, ep_file):
    pawns = board.pawns(colour)
    rank = bits.ranks[5 if colour == Colour.W else 2]
    ep_file = bits.files[ep_file]
    a_file = bits.files[0]
    shifted_pawns = shift_north_east(pawns) if colour == Colour.W else shift_south_east(pawns)
    right_en_passants = shifted_pawns & ep_file & ~a_file & rank
    return right_en_passants


def pawn_left_en_passants(board, colour, ep_file):
    pawns = board.pawns(colour)
    rank = bits.ranks[5 if colour == Colour.W else 2]
    ep_file = bits.files[ep_file]
    h_file = bits.files[7]
    shifted_pawns = shift_north_west(pawns) if colour == Colour.W else shift_south_west(pawns)
    left_en_passants = shifted_pawns & ep_file & ~h_file & rank
    return left_en_passants


def pawn_push_promotions(board, colour):
    pawns = board.pawns(colour)
    empty = ~board.occupied()
    shifted_pawns = shift_north(pawns) if colour == Colour.W else shift_south(pawns) & empty
    return shifted_pawns & bits.ranks[7 if colour == Colour.W else 0]


def pawn_right_capture_promotions(board, colour):
    pawns = board.pawns(colour)
    opponents = board.opponents(colour)
    shifted_pawns = shift_north_east(pawns) if colour == Colour.W else shift_south_east(pawns) & opponents
    return shifted_pawns & bits.ranks[7 if colour == Colour.W else 0]


def pawn_left_capture_promotions(board, colour):
    pawns = board.pawns(colour)
    opponents = board.opponents(colour)
    shifted_pawns = shift_north_west(pawns) if colour == Colour.W else shift_south_west(pawns) & opponents
    return shifted_pawns & bits.ranks[7 if colour == Colour.W else 0]


def print_bb(board):
    # Convert the long integer to a binary string, padding with leading zeros to make it 64 bits
    binary_str = format(board, '064b')
    # Iterate over each rank from 7 to 0 (white at the bottom)
    for i in range(8):
        # Iterate over each file from 0 to 7
        for n in range(7, -1, -1):
            # Calculate the index of the square in the binary string
            index = 8 * i + n
            # Print the corresponding bit
            print(binary_str[index], end='')
        # Print a new line after each rank
        print()
    # Print a new line after the entire board
    print()
