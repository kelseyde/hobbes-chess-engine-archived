import random

piece_square_hash = [[[0 for i in range(12)] for j in range(2)] for k in range(64)]
castling_rights_hash = [random.getrandbits(64) for l in range(16)]
en_passant_hash = [random.getrandbits(64) for m in range(8)]
turn_hash = random.getrandbits(64)

for i in range(64):
    for j in range(2):
        for k in range(6):
            piece_square_hash[i][j][k] = random.getrandbits(64)


def generate_key(board):
    key = 0
    for i in range(64):
        piece = board.piece_at(i)
        if piece is not None:
            colour = 0 if board.all_bbs[0] & (1 << i) else 1
            key ^= piece_square_hash[i][colour][piece.value]
    key ^= turn_hash
    key ^= castling_rights_hash[board.game_state.castle_rights]
    if board.game_state.ep_file >= 0:
        key ^= en_passant_hash[board.game_state.ep_file + 1]
    return key


def update_key(old_key, board, move, piece, old_castle_rights, new_castle_rights, old_ep_file, new_ep_file):
    key = old_key
    start_sq = move.start_sq
    end_sq = move.end_sq
    colour = 0 if board.all_bbs[0] & (1 << start_sq) else 1

    # Remove the piece from the start square
    key ^= piece_square_hash[start_sq][colour][piece.value]

    # Place the piece on the end square
    key ^= piece_square_hash[end_sq][colour][piece.value]

    # Toggle the turn
    key ^= turn_hash

    # Update castling rights
    key ^= castling_rights_hash[old_castle_rights]
    key ^= castling_rights_hash[new_castle_rights]

    # Update en passant file
    if old_ep_file >= 0:
        key ^= en_passant_hash[old_ep_file]
    if new_ep_file >= 0:
        key ^= en_passant_hash[new_ep_file]

    return key

