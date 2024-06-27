import random
from datetime import datetime
from time import time

from src.eval.evaluator import Evaluator
from src.hash.tt import TranspositionTable, HashFlag
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
        self.nodes = 0
        self.movegen = MoveGenerator()
        self.tt = TranspositionTable(128)
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

            print(f"info depth {current_depth} nodes {self.nodes} time {int(time() * 1000 - start)} tt_tries {self.tt.tries} tt_hits {self.tt.hits} tt_hit_rate {self.tt.get_hit_rate()}")

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

        # Look up the current position in the transposition table.
        tt_entry = self.tt.lookup(board.game_state.key)
        if tt_entry is not None:
            tt_depth = tt_entry[1]
            tt_score = tt_entry[2]
            if tt_depth >= depth_remaining:
                tt_flag = tt_entry[4]
                if tt_flag == HashFlag.EXACT:
                    return tt_score
                elif tt_flag == HashFlag.LOWER and tt_score <= alpha:
                    return alpha
                elif tt_flag == HashFlag.UPPER and tt_score >= beta:
                    return beta

        # Generate all legal moves in the position
        moves = self.movegen.generate_moves(board)

        if len(moves) == 0:
            return -MATE_SCORE if self.movegen.is_check(board, board.colour) else DRAW_SCORE

        # If we have reached the maximum depth, evaluate the position.
        if depth_remaining == 0:
            return self.eval.evaluate(board)

        best_move = None
        tt_flag = HashFlag.LOWER

        # Loop through all the legal moves.
        for move in moves:

            # Make the move on the board, search the resulting position, and then unmake the move.
            board.make_move(move)
            self.nodes += 1
            score = -self.search_to_depth(board, depth_from_root + 1, depth_remaining - 1, -beta, -alpha)
            board.unmake_move()

            if self.is_timeout():
                return alpha

            if score >= beta:
                tt_flag = HashFlag.LOWER
                self.tt.store(board.game_state.key, depth_remaining, beta, move, tt_flag)
                return beta

            if score > alpha:
                alpha = score
                best_move = move
                tt_flag = HashFlag.EXACT

                # If we are at the root of the search tree, update the best move.
                if depth_from_root == 0:
                    self.best_move_current_depth = move

        # Store the best move in the transposition table.
        self.tt.store(board.game_state.key, depth_remaining, alpha, best_move, tt_flag)
        return alpha

    def random_move(self, board):
        moves = board.generate_moves()
        return random.choice(moves)

    def is_timeout(self):
        return time() * 1000 > self.timeout
