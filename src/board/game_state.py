import src.board.bits as bits


class GameState:

    def __init__(self,
                 key=0,
                 captured_piece=None,
                 halfmove_clock=0,
                 fullmove_number=0,
                 castle_rights=bits.start_castle_rights,
                 ep_file=-1):
        self.key = key
        self.captured_piece = captured_piece
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number
        self.castle_rights = castle_rights
        self.ep_file = ep_file

    def is_kingside_legal(self, colour):
        kingside_mask = bits.white_kingside_rights if colour == bits.Colour.W else bits.black_kingside_rights
        return self.castle_rights & kingside_mask

    def is_queenside_legal(self, colour):
        queenside_mask = bits.white_queenside_rights if colour == bits.Colour.W else bits.black_queenside_rights
        return self.castle_rights & queenside_mask

