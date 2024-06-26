from src.board.bitwise import lsb, pop_bit
from src.movegen import attacks, ray


def calculate_pin_masks(board, colour):

    pin_mask = 0
    pin_ray_masks = [0] * 64

    king_sq = lsb(board.king(colour))
    friendlies = board.friendlies(colour)
    opponents = board.opponents(colour)

    sliders = board.rooks(~colour) | board.queens(~colour)
    if sliders != 0:
        possible_pinners = sliders & attacks.rook_attacks(king_sq, 0)
        pin_mask, pin_ray_masks = calculate_pins(pin_mask, pin_ray_masks, king_sq, friendlies, opponents, possible_pinners)

    sliders = board.bishops(~colour) | board.queens(~colour)
    if sliders != 0:
        possible_pinners = sliders & attacks.bishop_attacks(king_sq, 0)
        pin_mask, pin_ray_masks = calculate_pins(pin_mask, pin_ray_masks, king_sq, friendlies, opponents, possible_pinners)

    return pin_mask, pin_ray_masks


def calculate_pins(pin_mask, pin_ray_masks, king_sq, friendlies, opponents, possible_pinners):
    while possible_pinners != 0:
        possible_pinner = lsb(possible_pinners)
        pin_ray = ray.ray_between(possible_pinner, king_sq)

        if pin_ray & opponents != 0:
            possible_pinners = pop_bit(possible_pinners)
            continue

        friendlies_between = pin_ray & friendlies
        if friendlies_between.bit_count() == 1:
            friendly_square = lsb(friendlies_between)
            pin_mask |= friendlies_between
            pin_ray_masks[friendly_square] = pin_ray | (1 << possible_pinner)

        possible_pinners = pop_bit(possible_pinners)

    return pin_mask, pin_ray_masks
