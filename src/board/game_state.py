import src.board.bits as bits


class GameState:

    def __init__(self, key=0, captured_piece=None, halfmove_clock=0, castle_rights=bits.start_castle_rights, ep_file=-1):
        self.key = key
        self.captured_piece = captured_piece
        self.halfmove_clock = halfmove_clock
        self.castle_rights = castle_rights
        self.ep_file = ep_file
