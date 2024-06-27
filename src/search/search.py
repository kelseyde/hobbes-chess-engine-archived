import random
from datetime import datetime
from time import time

from src.eval.evaluator import Evaluator
from src.movegen.movegen import MoveGenerator
from src.util.notation import fen_to_board, move_to_notation

MAX_VALUE = 1000000000
MIN_VALUE = -1000000000
MATE_SCORE = 1000000
DRAW_SCORE = 0


class Search:

    def __init__(self):
        self.max_depth = 256
        self.best_move = -1
        self.best_move_current_depth = None
        self.timeout = -1
        self.movegen = MoveGenerator()
        self.eval = Evaluator()

    def search(self, board, ms):
        """
        Do an iterative deepening search: search to depth 1, then 2, then 3, and so on, until time runs out.
        """

        start = time() * 1000
        self.timeout = start + ms

        current_depth = 1
        self.best_move = None
        self.best_move_current_depth = None

        alpha = MIN_VALUE
        beta = MAX_VALUE

        # Keep searching to greater depths until we run out of time or depth.
        while not self.is_timeout() and current_depth <= self.max_depth:

            print(f"Searching to depth {current_depth}")

            # Reset the best move at the current depth.
            self.best_move_current_depth = None

            # Start a search limited to the current depth.
            self.search_to_depth(board, 0, current_depth, alpha, beta)

            # If we completed the search, update the best move.
            if self.best_move_current_depth:
                self.best_move = self.best_move_current_depth
            current_depth += 1

        if not self.best_move:
            print("Time ran out, selecting a random move")
            return self.random_move(board)

        return self.best_move

    def search_to_depth(self, board, depth_from_root, depth_remaining, alpha, beta):
        """
        Do a minimax search: find the move that maximises our score, limited to a certain depth.
        """

        # Exit early if we run out of time
        if self.is_timeout():
            return 0

        # Generate all legal moves in the position
        moves = self.movegen.generate_moves(board)

        if len(moves) == 0:
            return -MATE_SCORE if self.movegen.is_check(board, board.colour) else DRAW_SCORE

        # If we have reached the maximum depth, evaluate the position.
        if depth_remaining == 0:
            return self.eval.evaluate(board)

        # Loop through all the legal moves.
        for move in moves:

            # Make the move on the board, search the resulting position, and then unmake the move.
            board.make_move(move)
            score = -self.search_to_depth(board, depth_from_root + 1, depth_remaining - 1, -beta, -alpha)
            board.unmake_move()

            if self.is_timeout():
                return alpha

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

                # If we are at the root of the search tree, update the best move.
                if depth_from_root == 0:
                    self.best_move_current_depth = move

        return alpha

    def random_move(self, board):
        moves = board.generate_moves()
        return random.choice(moves)

    def is_timeout(self):
        return time() * 1000 > self.timeout
