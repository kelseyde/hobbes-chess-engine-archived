from datetime import datetime

from src.movegen import movegen
from src.util.notation import fen_to_board, move_to_notation

movegen = movegen.MoveGenerator()


def perft(board, depth, start_depth, debug=False):
    moves = movegen.generate_moves(board)
    if debug:
        print(f"{[move_to_notation(move) for move in board.move_history]} "
              f"{len(moves)} "
              f"{[move_to_notation(move) for move in moves]}")
    if depth == 1:
        return len(moves)
    nodes = 0
    for move in moves:
        board.make_move(move)
        nodes += perft(board, depth - 1, start_depth, debug)
        board.unmake_move()
    if debug and depth == start_depth - 1:
        print(f"{move_to_notation(board.move_history[0])}: {nodes}")
    return nodes


def run_perft(fen, depth, debug=False):
    board = fen_to_board(fen)
    start = datetime.now()
    nodes = perft(board, depth, depth, debug)
    end = datetime.now()
    time = end - start
    print(f"Nodes: {nodes}")
    print(f"Time: {time}")
    return nodes, time

#
# run_perft("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 1)
# run_perft("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 2)
# run_perft("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 3)
# run_perft("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 4)
# run_perft("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 5)
# run_perft("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 6)

