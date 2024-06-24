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

# Bitboards for the starting positions of the pieces
piece_bbs = [
    0b11111111000000000000000000000000000000001111111100000000,
    0b100001000000000000000000000000000000000000000000000000001000010,
    0b10010000000000000000000000000000000000000000000000000000100100,
    0b1000000100000000000000000000000000000000000000000000000010000001,
    0b100000000000000000000000000000000000000000000000000000001000,
    0b1000000000000000000000000000000000000000000000000000000010000
]
all_bbs = [
    0b1111111111111111,
    0b1111111111111111000000000000000000000000000000000000000000000000,
    0b1111111111111111000000000000000000000000000000001111111111111111
]

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

start_castle_rights = 0b1111

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

