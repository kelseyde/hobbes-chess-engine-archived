import zobrist


class GameState:

    def __init__(self, key, captured_piece, halfmove_clock, castle_rights, ep_square):
        self.key = key
        self.captured_piece = captured_piece
        self.halfmove_clock = halfmove_clock
        self.castle_rights = castle_rights
        self.ep_square = ep_square
