import profile

import src.movegen.attacks as attacks
from src.board import bits
from src.board.bitwise import lsb, pop_bit, pawn_pushes, pawn_double_pushes, pawn_right_captures, pawn_left_captures, \
    pawn_right_en_passants, pawn_left_en_passants, pawn_push_promotions, pawn_right_capture_promotions, \
    pawn_left_capture_promotions, shift_north_east, shift_north_west, shift_south_west, shift_south_east
from src.board.colour import Colour
from src.board.board import Board
from src.board.move import Move
from src.board.move_flag import MoveFlag
from src.movegen import pin, ray


class MoveGenerator:

    def __init__(self):
        self.moves = []
        self.checkers_mask = 0
        self.num_checkers = 0
        self.pin_mask = 0
        self.pin_ray_masks = [0] * 64
        self.capture_mask = 0
        self.push_mask = 0

    def generate_moves(self, board):

        self.moves = []
        self.capture_mask = bits.all_squares
        self.push_mask = bits.all_squares
        self.pin_mask, self.pin_ray_masks = pin.calculate_pin_masks(board, board.colour)
        self.checkers_mask = self.calculate_attacker_mask(board, board.king(board.colour))
        self.num_checkers = self.checkers_mask.bit_count()

        self.generate_king_moves(board)

        if self.num_checkers > 1:
            return self.moves

        if self.num_checkers == 1:
            self.capture_mask = self.checkers_mask
            checker_sq = lsb(self.checkers_mask)
            if board.piece_at(checker_sq).is_slider():
                king_sq = lsb(board.king(board.colour))
                self.push_mask = ray.ray_between(checker_sq, king_sq)
            else:
                self.push_mask = bits.no_squares

        self.generate_knight_moves(board)
        self.generate_pawn_moves(board)
        self.generate_sliding_moves(board)
        self.generate_castle_moves(board)

        return self.moves

    def generate_king_moves(self, board):
        colour = board.colour
        king_sq = lsb(board.king(colour))
        friendlies = board.friendlies(colour)
        king_moves = attacks.king_attacks[king_sq] & ~friendlies
        board.remove_king(colour)
        while king_moves:
            end_sq = lsb(king_moves)
            if not self.is_attacked(board, 1 << end_sq, colour):
                self.moves.append(Move(king_sq, end_sq))
            king_moves = pop_bit(king_moves)
        board.add_king(colour, king_sq)

    def generate_castle_moves(self, board):
        if self.num_checkers > 0:
            return
        colour = board.colour
        occupied = board.occupied()
        start_sq = lsb(board.king(colour))
        if board.game_state.is_kingside_legal(colour):
            self.generate_castle_move(board, colour, True, start_sq, occupied)
        if board.game_state.is_queenside_legal(colour):
            self.generate_castle_move(board, colour, False, start_sq, occupied)

    def generate_castle_move(self, board, colour, kingside, start_sq, occ):
        travel_squares = self.get_castle_travel_squares(kingside, colour)
        blocked_squares = occ & travel_squares
        safe_squares = self.get_castle_safe_squares(kingside, colour)
        if not blocked_squares and not self.is_attacked(board, safe_squares, colour):
            end_sq = self.get_castle_end_square(kingside, colour)
            self.moves.append(Move(start_sq, end_sq, MoveFlag.CASTLE))

    def generate_knight_moves(self, board):
        colour = board.colour
        knights = board.knights(colour) & ~self.pin_mask
        friendlies = board.friendlies(colour)
        while knights:
            start_sq = lsb(knights)
            knight_attacks = attacks.knight_attacks[start_sq] & ~friendlies & (self.push_mask | self.capture_mask)
            while knight_attacks:
                end_sq = lsb(knight_attacks)
                self.moves.append(Move(start_sq, end_sq))
                knight_attacks = pop_bit(knight_attacks)
            knights = pop_bit(knights)

    def generate_pawn_moves(self, board):
        colour = board.colour

        single_pushes = pawn_pushes(board, colour) & self.push_mask
        while single_pushes:
            end_sq = lsb(single_pushes)
            start_sq = end_sq - 8 if colour == Colour.W else end_sq + 8
            if not self.is_pinned(start_sq) or self.is_moving_along_pin_ray(start_sq, end_sq):
                self.moves.append(Move(start_sq, end_sq))
            single_pushes = pop_bit(single_pushes)

        double_pushes = pawn_double_pushes(board, colour) & self.push_mask
        while double_pushes:
            end_sq = lsb(double_pushes)
            start_sq = end_sq - 16 if colour == Colour.W else end_sq + 16
            if not self.is_pinned(start_sq) or self.is_moving_along_pin_ray(start_sq, end_sq):
                self.moves.append(Move(start_sq, end_sq, MoveFlag.DOUBLE_PAWN_PUSH))
            double_pushes = pop_bit(double_pushes)

        right_captures = pawn_right_captures(board, colour) & self.capture_mask
        while right_captures:
            end_sq = lsb(right_captures)
            start_sq = end_sq - 9 if colour == Colour.W else end_sq + 7
            if not self.is_pinned(start_sq) or self.is_moving_along_pin_ray(start_sq, end_sq):
                self.moves.append(Move(start_sq, end_sq))
            right_captures = pop_bit(right_captures)

        left_captures = pawn_left_captures(board, colour) & self.capture_mask
        while left_captures:
            end_sq = lsb(left_captures)
            start_sq = end_sq - 7 if colour == Colour.W else end_sq + 9
            if not self.is_pinned(start_sq) or self.is_moving_along_pin_ray(start_sq, end_sq):
                self.moves.append(Move(start_sq, end_sq))
            left_captures = pop_bit(left_captures)

        if board.game_state.ep_file >= 0:
            right_en_passants = pawn_right_en_passants(board, colour, board.game_state.ep_file)
            while right_en_passants:
                end_sq = lsb(right_en_passants)
                start_sq = end_sq - 9 if colour == Colour.W else end_sq + 7
                move = Move(start_sq, end_sq, MoveFlag.EN_PASSANT)
                if self.is_legal_move(board, move, colour):
                    self.moves.append(Move(start_sq, end_sq, MoveFlag.EN_PASSANT))
                right_en_passants = pop_bit(right_en_passants)

            left_en_passants = pawn_left_en_passants(board, colour, board.game_state.ep_file)
            while left_en_passants:
                end_sq = lsb(left_en_passants)
                start_sq = end_sq - 7 if colour == Colour.W else end_sq + 9
                move = Move(start_sq, end_sq, MoveFlag.EN_PASSANT)
                if self.is_legal_move(board, move, colour):
                    self.moves.append(Move(start_sq, end_sq, MoveFlag.EN_PASSANT))
                left_en_passants = pop_bit(left_en_passants)

        push_promotions = pawn_push_promotions(board, colour) & self.push_mask
        while push_promotions:
            end_sq = lsb(push_promotions)
            start_sq = end_sq - 8 if colour == Colour.W else end_sq + 8
            self.moves.extend(self.promotion_moves(start_sq, end_sq))
            push_promotions = pop_bit(push_promotions)

        right_capture_promotions = pawn_right_capture_promotions(board, colour) & (self.capture_mask | self.push_mask)
        while right_capture_promotions:
            end_sq = lsb(right_capture_promotions)
            start_sq = end_sq - 9 if colour == Colour.W else end_sq + 7
            if not self.is_pinned(start_sq) or self.is_moving_along_pin_ray(start_sq, end_sq):
                self.moves.extend(self.promotion_moves(start_sq, end_sq))
            right_capture_promotions = pop_bit(right_capture_promotions)

        left_capture_promotions = pawn_left_capture_promotions(board, colour) & (self.capture_mask | self.push_mask)
        while left_capture_promotions:
            end_sq = lsb(left_capture_promotions)
            start_sq = end_sq - 7 if colour == Colour.W else end_sq + 9
            if not self.is_pinned(start_sq) or self.is_moving_along_pin_ray(start_sq, end_sq):
                self.moves.extend(self.promotion_moves(start_sq, end_sq))
            left_capture_promotions = pop_bit(left_capture_promotions)

    def generate_sliding_moves(self, board):
        colour = board.colour
        friendlies = board.friendlies(colour)
        occupied = board.occupied()

        diagonal_sliders = board.bishops(colour) | board.queens(colour)
        while diagonal_sliders:
            start_sq = lsb(diagonal_sliders)
            slider_attacks = attacks.bishop_attacks(start_sq, occupied) & ~friendlies & (self.push_mask | self.capture_mask)
            if self.is_pinned(start_sq):
                slider_attacks &= self.pin_ray_masks[start_sq]
            while slider_attacks:
                end_sq = lsb(slider_attacks)
                self.moves.append(Move(start_sq, end_sq))
                slider_attacks = pop_bit(slider_attacks)
            diagonal_sliders = pop_bit(diagonal_sliders)

        orthogonal_sliders = board.rooks(colour) | board.queens(colour)
        while orthogonal_sliders:
            start_sq = lsb(orthogonal_sliders)
            slider_attacks = attacks.rook_attacks(start_sq, occupied) & ~friendlies & (self.push_mask | self.capture_mask)
            if self.is_pinned(start_sq):
                slider_attacks &= self.pin_ray_masks[start_sq]
            while slider_attacks:
                end_sq = lsb(slider_attacks)
                self.moves.append(Move(start_sq, end_sq))
                slider_attacks = pop_bit(slider_attacks)
            orthogonal_sliders = pop_bit(orthogonal_sliders)

    def is_check(self, board, colour):
        king_sq = lsb(board.king(colour))
        return self.is_attacked(board, 1 << king_sq, colour)

    def is_attacked(self, board, square_mask, colour):
        while square_mask != 0:
            sq = lsb(square_mask)

            pawns = board.pawns(~colour)
            if pawns:
                pawn_attack_mask = self.pawn_attacks(board, sq, colour)
                if pawn_attack_mask & pawns:
                    return True

            knights = board.knights(~colour)
            if knights:
                knight_attack_mask = self.knight_attacks(board, sq, colour)
                if knight_attack_mask & knights:
                    return True

            bishops = board.bishops(~colour)
            queens = board.queens(~colour)
            diagonal_sliders = bishops | queens
            if diagonal_sliders:
                bishop_attack_mask = self.bishop_attacks(board, sq, colour)
                if bishop_attack_mask & diagonal_sliders:
                    return True

            rooks = board.rooks(~colour)
            orthogonal_sliders = rooks | queens
            if orthogonal_sliders:
                rook_attack_mask = self.rook_attacks(board, sq, colour)
                if rook_attack_mask & orthogonal_sliders:
                    return True

            kings = board.king(~colour)
            king_attack_mask = self.king_attacks(board, sq, colour)
            if king_attack_mask & kings:
                return True

            square_mask = pop_bit(square_mask)
        return False

    def is_legal_move(self, board, move, colour):
        board.make_move(move)
        is_check = self.is_check(board, colour)
        board.unmake_move()
        return not is_check

    def calculate_attacker_mask(self, board, square_mask):
        attacker_mask = 0
        while square_mask != 0:
            square = lsb(square_mask)

            pawns = board.pawns(~board.colour)
            pawn_attack_mask = self.pawn_attacks(board, square, board.colour)
            attacker_mask |= pawn_attack_mask & pawns

            knights = board.knights(~board.colour)
            knight_attack_mask = self.knight_attacks(board, square, board.colour)
            attacker_mask |= knight_attack_mask & knights

            bishops = board.bishops(~board.colour)
            bishop_attack_mask = self.bishop_attacks(board, square, board.colour)
            attacker_mask |= bishop_attack_mask & bishops

            rooks = board.rooks(~board.colour)
            rook_attack_mask = self.rook_attacks(board, square, board.colour)
            attacker_mask |= rook_attack_mask & rooks

            queens = board.queens(~board.colour)
            queen_attack_mask = self.queen_attacks(board, square, board.colour)
            attacker_mask |= queen_attack_mask & queens

            kings = board.king(~board.colour)
            king_attack_mask = self.king_attacks(board, square, board.colour)
            attacker_mask |= king_attack_mask & kings

            square_mask = pop_bit(square_mask)
        return attacker_mask

    def pawn_attacks(self, board, square, colour):
        square_mask = 1 << square
        friendlies = board.friendlies(colour)

        left_capture = shift_north_west(square_mask) if colour == Colour.W else shift_south_west(square_mask)
        right_capture = shift_north_east(square_mask) if colour == Colour.W else shift_south_east(square_mask)
        return (left_capture | right_capture) & ~friendlies

    def knight_attacks(self, board, square, colour):
        friendlies = board.friendlies(colour)
        return attacks.knight_attacks[square] & ~friendlies

    def bishop_attacks(self, board, square, colour):
        return self.sliding_attacks(board, square, colour, True, False)

    def rook_attacks(self, board, square, colour):
        return self.sliding_attacks(board, square, colour, False, True)

    def queen_attacks(self, board, square, colour):
        return self.sliding_attacks(board, square, colour, True, True)

    def king_attacks(self, board, square, colour):
        friendlies = board.friendlies(colour)
        return attacks.king_attacks[square] & ~friendlies

    def sliding_attacks(self, board, square, colour, diagonal, orthogonal):
        friendlies = board.friendlies(colour)
        occupied = board.occupied()
        attack_mask = 0
        if diagonal:
            attack_mask |= attacks.bishop_attacks(square, occupied)
        if orthogonal:
            attack_mask |= attacks.rook_attacks(square, occupied)
        return attack_mask & ~friendlies

    def promotion_moves(self, start_sq, end_sq):
        return [Move(start_sq, end_sq, MoveFlag.PROMOTE_Q), Move(start_sq, end_sq, MoveFlag.PROMOTE_R),
                Move(start_sq, end_sq, MoveFlag.PROMOTE_B), Move(start_sq, end_sq, MoveFlag.PROMOTE_N)]

    def is_pinned(self, sq):
        return 1 << sq & self.pin_mask

    def is_moving_along_pin_ray(self, start_sq, end_sq):
        pin_ray = self.pin_ray_masks[start_sq]
        return 1 << end_sq & pin_ray

    def get_castle_travel_squares(self, kingside, colour):
        if kingside:
            return bits.white_kingside_castle_travel_mask if colour == Colour.W else bits.black_kingside_castle_travel_mask
        else:
            return bits.white_queenside_castle_travel_mask if colour == Colour.W else bits.black_queenside_castle_travel_mask

    def get_castle_safe_squares(self, kingside, colour):
        if kingside:
            return bits.white_kingside_castle_safe_mask if colour == Colour.W else bits.black_kingside_castle_safe_mask
        else:
            return bits.white_queenside_castle_safe_mask if colour == Colour.W else bits.black_queenside_castle_safe_mask

    def get_castle_end_square(self, kingside, colour):
        if kingside:
            return 6 if colour == Colour.W else 62
        else:
            return 2 if colour == Colour.W else 58