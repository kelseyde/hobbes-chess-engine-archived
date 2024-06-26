from src.movegen.movegen import MoveGenerator
from src.util.notation import move_to_notation

movegen = MoveGenerator()


def get_legal_move(board, move):
    legal_moves = movegen.generate_moves(board)
    for legal_move in legal_moves:
        if move.start_sq == legal_move.start_sq and move.end_sq == legal_move.end_sq and move.flag == legal_move.flag:
            return legal_move
    raise ValueError(f"Illegal move! {move_to_notation(move)}")


def is_legal_move(board, move):
    legal_moves = movegen.generate_moves(board)
    for legal_move in legal_moves:
        if move.start_sq == legal_move.start_sq and move.end_sq == legal_move.end_sq and move.flag == legal_move.flag:
            return True
    return False


def contains_move(moves, move):
    for legal_move in moves:
        if move.start_sq == legal_move.start_sq and move.end_sq == legal_move.end_sq and move.flag == legal_move.flag:
            return True
    return False


def contains_all(target_moves, actual_moves):
    for move in target_moves:
        if not contains_move(actual_moves, move):
            print(move_to_notation(move))
            return False
    return True
