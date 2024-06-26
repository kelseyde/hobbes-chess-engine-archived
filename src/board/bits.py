from src.board.colour import Colour
from src.board.piece import Piece

all_squares = 0xFFFFFFFFFFFFFFFF
no_squares = 0x0

# Ranks 1 through 8
ranks = [
    0xFF,
    0xFF00,
    0xFF0000,
    0xFF000000,
    0xFF00000000,
    0xFF0000000000,
    0xFF000000000000,
    0xFF00000000000000
]

# Files a through h
files = [
    0x0101010101010101,
    0x0202020202020202,
    0x0404040404040404,
    0x0808080808080808,
    0x1010101010101010,
    0x2020202020202020,
    0x4040404040404040,
    0x8080808080808080
]

# Bitboards for the starting positions of the different piece types
piece_bbs = [
    0b11111111000000000000000000000000000000001111111100000000,
    0b100001000000000000000000000000000000000000000000000000001000010,
    0b10010000000000000000000000000000000000000000000000000000100100,
    0b1000000100000000000000000000000000000000000000000000000010000001,
    0b100000000000000000000000000000000000000000000000000000001000,
    0b1000000000000000000000000000000000000000000000000000000010000
]

# Bitboards for the starting positions of the white pieces, black pieces, and all pieces
all_bbs = [
    0b1111111111111111,
    0b1111111111111111000000000000000000000000000000000000000000000000,
    0b1111111111111111000000000000000000000000000000001111111111111111
]

# Piece list for the starting positions of the pieces
start_piece_list = [
    Piece.R, Piece.N, Piece.B, Piece.Q, Piece.K, Piece.B, Piece.N, Piece.R,
    Piece.P, Piece.P, Piece.P, Piece.P, Piece.P, Piece.P, Piece.P, Piece.P,
    None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None,
    Piece.P, Piece.P, Piece.P, Piece.P, Piece.P, Piece.P, Piece.P, Piece.P,
    Piece.R, Piece.N, Piece.B, Piece.Q, Piece.K, Piece.B, Piece.N, Piece.R,
]

# Starting castle rights
start_castle_rights = 0b1111
clear_white_rights = 0b1100
clear_black_rights = 0b0011
clear_white_kingside_rights = 0b1110
clear_white_queenside_rights = 0b1101
clear_black_kingside_rights = 0b1011
clear_black_queenside_rights = 0b0111
white_kingside_rights = 0b0001
black_kingside_rights = 0b1000
white_queenside_rights = 0b0010
black_queenside_rights = 0b0100

white_kingside_castle_travel_mask = 0x0000000000000060
white_queenside_castle_travel_mask = 0x000000000000000E
black_kingside_castle_travel_mask = white_kingside_castle_travel_mask << (7 * 8)
black_queenside_castle_travel_mask = white_queenside_castle_travel_mask << (7 * 8)

white_queenside_castle_safe_mask = 0x000000000000001C
white_kingside_castle_safe_mask = white_queenside_castle_safe_mask << 2
black_queenside_castle_safe_mask = white_queenside_castle_safe_mask << (7 * 8)
black_kingside_castle_safe_mask = white_queenside_castle_safe_mask << (7 * 8)

# File and rank maps
file_map = 'abcdefgh'
rank_map = '12345678'

piece_unicode = {
    (Piece.P, Colour.W): '♙', (Piece.P, Colour.B): '♟',
    (Piece.N, Colour.W): '♘', (Piece.N, Colour.B): '♞',
    (Piece.B, Colour.W): '♗', (Piece.B, Colour.B): '♝',
    (Piece.R, Colour.W): '♖', (Piece.R, Colour.B): '♜',
    (Piece.Q, Colour.W): '♕', (Piece.Q, Colour.B): '♛',
    (Piece.K, Colour.W): '♔', (Piece.K, Colour.B): '♚',
}

char_to_piece_map = {
    'p': Piece.P, 'r': Piece.R, 'n': Piece.N, 'b': Piece.B, 'q': Piece.Q, 'k': Piece.K,
    'P': Piece.P, 'R': Piece.R, 'N': Piece.N, 'B': Piece.B, 'Q': Piece.Q, 'K': Piece.K,
}

piece_to_char_map = {
    (Piece.P, Colour.W): 'P', (Piece.R, Colour.W): 'R', (Piece.N, Colour.W): 'N',
    (Piece.B, Colour.W): 'B', (Piece.Q, Colour.W): 'Q', (Piece.K, Colour.W): 'K',
    (Piece.P, Colour.B): 'p', (Piece.R, Colour.B): 'r', (Piece.N, Colour.B): 'n',
    (Piece.B, Colour.B): 'b', (Piece.Q, Colour.B): 'q', (Piece.K, Colour.B): 'k'
}

