PAWN_SCORE = 100
KNIGHT_SCORE = 320
BISHOP_SCORE = 330
ROOK_SCORE = 500
QUEEN_SCORE = 900


class Evaluator:

    def evaluate(self, board):
        colour = board.colour

        our_pawns = board.pawns(colour)
        their_pawns = board.pawns(~colour)

        our_knights = board.knights(colour)
        their_knights = board.knights(~colour)

        our_bishops = board.bishops(colour)
        their_bishops = board.bishops(~colour)

        our_rooks = board.rooks(colour)
        their_rooks = board.rooks(~colour)

        our_queens = board.queens(colour)
        their_queens = board.queens(~colour)

        our_pawn_score = self.score_pieces(our_pawns, PAWN_SCORE)
        their_pawn_score = self.score_pieces(their_pawns, PAWN_SCORE)

        our_knight_score = self.score_pieces(our_knights, KNIGHT_SCORE)
        their_knight_score = self.score_pieces(their_knights, KNIGHT_SCORE)

        our_bishop_score = self.score_pieces(our_bishops, BISHOP_SCORE)
        their_bishop_score = self.score_pieces(their_bishops, BISHOP_SCORE)

        our_rook_score = self.score_pieces(our_rooks, ROOK_SCORE)
        their_rook_score = self.score_pieces(their_rooks, ROOK_SCORE)

        our_queen_score = self.score_pieces(our_queens, QUEEN_SCORE)
        their_queen_score = self.score_pieces(their_queens, QUEEN_SCORE)

        return (our_pawn_score + our_knight_score + our_bishop_score + our_rook_score + our_queen_score) - \
            (their_pawn_score + their_knight_score + their_bishop_score + their_rook_score + their_queen_score)

    @staticmethod
    def score_pieces(pieces, score):
        return pieces.bit_count() * score
