import src.board.bits as bits
from src.board import zobrist
from src.board.board import Board
from src.board.colour import Colour
from src.board.game_state import GameState
from src.board.move import Move
from src.board.move_flag import MoveFlag
from src.board.piece import Piece


def square_to_notation(square):
    file = bits.file_map[Board.file(square)]
    rank = bits.rank_map[Board.rank(square)]
    return f"{file}{rank}"


def notation_to_square(notation):
    file = notation[0]
    rank = notation[1]
    return Board.square_index(bits.file_map.index(file), bits.rank_map.index(rank))


def move_to_notation(move):

    start_file = bits.file_map[Board.file(move.start_sq)]
    start_rank = bits.rank_map[Board.rank(move.start_sq)]
    end_file = bits.file_map[Board.file(move.end_sq)]
    end_rank = bits.rank_map[Board.rank(move.end_sq)]

    promotion_piece = move.get_promotion_piece()
    promotion_suffix = ''

    if promotion_piece:
        promotion_suffix = promotion_piece.name.lower()

    return f"{start_file}{start_rank}{end_file}{end_rank}{promotion_suffix}"


def notation_to_move(notation, flag=None):
    start_file = notation[0]
    start_rank = notation[1]
    end_file = notation[2]
    end_rank = notation[3]

    start_sq = Board.square_index(bits.file_map.index(start_file), bits.rank_map.index(start_rank))
    end_sq = Board.square_index(bits.file_map.index(end_file), bits.rank_map.index(end_rank))

    if flag is not None:
        return Move(start_sq, end_sq, flag)

    promotion_suffix = notation[4] if len(notation) > 4 else ''

    if promotion_suffix == 'q':
        flag = MoveFlag.PROMOTE_Q
    elif promotion_suffix == 'r':
        flag = MoveFlag.PROMOTE_R
    elif promotion_suffix == 'b':
        flag = MoveFlag.PROMOTE_B
    elif promotion_suffix == 'n':
        flag = MoveFlag.PROMOTE_N
    else:
        flag = MoveFlag.STANDARD

    return Move(start_sq, end_sq, flag)


def fen_to_board(fen):
    board = Board()

    # Clear current board state
    board.piece_bbs = [0 for piece in Piece]
    board.all_bbs = [0, 0, 0]
    board.piece_list = [None] * 64
    board.move_history = []
    board.game_state = GameState()
    board.game_state_history = []

    fen_parts = fen.split()
    piece_placement, active_color, castling_rights, ep_target, halfmove_clock, fullmove_number = fen_parts

    # Set up the pieces on the board
    rank = 7
    file = 0
    for char in piece_placement:
        if char == '/':
            rank -= 1
            file = 0
        elif char.isdigit():
            file += int(char)
        else:
            piece = bits.char_to_piece_map[char]
            color = Colour.W if char.isupper() else Colour.B
            square = board.square_index(file, rank)
            board.toggle_square(piece, color, square)
            file += 1

    # Set active color
    board.colour = Colour.W if active_color == 'w' else Colour.B

    # Set castling rights
    board.game_state.castle_rights = 0
    if 'K' in castling_rights:
        board.game_state.castle_rights |= 1
    if 'Q' in castling_rights:
        board.game_state.castle_rights |= 2
    if 'k' in castling_rights:
        board.game_state.castle_rights |= 4
    if 'q' in castling_rights:
        board.game_state.castle_rights |= 8

    # Set en passant target square
    board.game_state.ep_file = -1 if ep_target == '-' \
        else Board.file(notation_to_square(ep_target))

    # Set halfmove clock and fullmove number
    board.game_state.halfmove_clock = int(halfmove_clock)
    board.game_state.fullmove_number = int(fullmove_number)

    # Generate Zobrist key
    board.game_state.key = zobrist.generate_key(board)

    return board


def board_to_fen(board: Board) -> str:
    fen_parts = []

    # Piece Placement
    piece_placement = []
    for rank in range(7, -1, -1):
        empty_count = 0
        for file in range(8):
            square = board.square_index(file, rank)
            piece = board.piece_at(square)
            if piece is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    piece_placement.append(str(empty_count))
                    empty_count = 0
                colour = board.colour_at(square)
                piece_placement.append(bits.piece_to_char_map[(piece, colour)])
        if empty_count > 0:
            piece_placement.append(str(empty_count))
        piece_placement.append('/')
    piece_placement.pop()  # Remove the last '/'
    fen_parts.append(''.join(piece_placement))

    # Active Color
    fen_parts.append('w' if board.colour == Colour.W else 'b')

    # Castling Rights
    castling_rights = ''
    if board.game_state.castle_rights & 1:
        castling_rights += 'K'
    if board.game_state.castle_rights & 2:
        castling_rights += 'Q'
    if board.game_state.castle_rights & 4:
        castling_rights += 'k'
    if board.game_state.castle_rights & 8:
        castling_rights += 'q'
    fen_parts.append(castling_rights if castling_rights else '-')

    # En Passant Target Square
    if board.game_state.ep_file <= 0:
        fen_parts.append('-')
    else:
        file = bits.file_map[board.game_state.ep_file]
        rank = '6' if board.colour == Colour.W else '3'
        fen_parts.append(file + rank)

    # Halfmove Clock
    fen_parts.append(str(board.game_state.halfmove_clock))

    # Fullmove Number
    fen_parts.append(str(board.game_state.fullmove_number))

    return ' '.join(fen_parts)