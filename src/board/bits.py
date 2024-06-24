from src.board.piece import Piece
from src.board.colour import Colour

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

file_map = 'abcdefgh'
rank_map = '12345678'

piece_unicode = {
    (Piece.P, Colour.WHITE): '♙', (Piece.P, Colour.BLACK): '♟',
    (Piece.N, Colour.WHITE): '♘', (Piece.N, Colour.BLACK): '♞',
    (Piece.B, Colour.WHITE): '♗', (Piece.B, Colour.BLACK): '♝',
    (Piece.R, Colour.WHITE): '♖', (Piece.R, Colour.BLACK): '♜',
    (Piece.Q, Colour.WHITE): '♕', (Piece.Q, Colour.BLACK): '♛',
    (Piece.K, Colour.WHITE): '♔', (Piece.K, Colour.BLACK): '♚',
}

char_to_piece_map = {
    'p': Piece.P, 'r': Piece.R, 'n': Piece.N, 'b': Piece.B, 'q': Piece.Q, 'k': Piece.K,
    'P': Piece.P, 'R': Piece.R, 'N': Piece.N, 'B': Piece.B, 'Q': Piece.Q, 'K': Piece.K,
}

piece_to_char_map = {
    (Piece.P, Colour.WHITE): 'P', (Piece.R, Colour.WHITE): 'R', (Piece.N, Colour.WHITE): 'N',
    (Piece.B, Colour.WHITE): 'B', (Piece.Q, Colour.WHITE): 'Q', (Piece.K, Colour.WHITE): 'K',
    (Piece.P, Colour.BLACK): 'p', (Piece.R, Colour.BLACK): 'r', (Piece.N, Colour.BLACK): 'n',
    (Piece.B, Colour.BLACK): 'b', (Piece.Q, Colour.BLACK): 'q', (Piece.K, Colour.BLACK): 'k'
}

