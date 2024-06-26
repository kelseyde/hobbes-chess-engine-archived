from src.board.board import Board


def ray_between(start_sq, end_sq):
    if not Board.is_valid_square_index(start_sq) or not Board.is_valid_square_index(end_sq) or start_sq == end_sq:
        return 0

    direction_offset = compute_direction_offset(start_sq, end_sq)
    if direction_offset == 0:
        return 0

    ray = 0
    current_sq = start_sq + direction_offset
    while Board.is_valid_square_index(current_sq) and current_sq != end_sq:
        ray |= 1 << current_sq
        current_sq += direction_offset

    return ray


def compute_direction_offset(start_sq, end_sq):
    start_rank = Board.rank(start_sq)
    start_file = Board.file(start_sq)
    end_rank = Board.rank(end_sq)
    end_file = Board.file(end_sq)

    if start_rank == end_rank:
        return 1 if start_sq < end_sq else -1

    if start_file == end_file:
        return 8 if start_sq < end_sq else -8

    start_diagonal = Board.diagonal(start_sq)
    end_diagonal = Board.diagonal(end_sq)
    start_anti_diagonal = Board.anti_diagonal(start_sq)
    end_anti_diagonal = Board.anti_diagonal(end_sq)

    if start_diagonal == end_diagonal:
        return 7 if start_sq < end_sq else -7

    if start_anti_diagonal == end_anti_diagonal:
        return 9 if start_sq < end_sq else -9

    return 0
