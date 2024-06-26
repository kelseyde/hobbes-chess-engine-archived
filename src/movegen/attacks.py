from src.board import bits
from src.board.board import Board

king_attacks = [
    0x0000000000000302, 0x0000000000000705, 0x0000000000000e0a, 0x0000000000001c14,
    0x0000000000003828, 0x0000000000007050, 0x000000000000e0a0, 0x000000000000c040,
    0x0000000000030203, 0x0000000000070507, 0x00000000000e0a0e, 0x00000000001c141c,
    0x0000000000382838, 0x0000000000705070, 0x0000000000e0a0e0, 0x0000000000c040c0,
    0x0000000003020300, 0x0000000007050700, 0x000000000e0a0e00, 0x000000001c141c00,
    0x0000000038283800, 0x0000000070507000, 0x00000000e0a0e000, 0x00000000c040c000,
    0x0000000302030000, 0x0000000705070000, 0x0000000e0a0e0000, 0x0000001c141c0000,
    0x0000003828380000, 0x0000007050700000, 0x000000e0a0e00000, 0x000000c040c00000,
    0x0000030203000000, 0x0000070507000000, 0x00000e0a0e000000, 0x00001c141c000000,
    0x0000382838000000, 0x0000705070000000, 0x0000e0a0e0000000, 0x0000c040c0000000,
    0x0003020300000000, 0x0007050700000000, 0x000e0a0e00000000, 0x001c141c00000000,
    0x0038283800000000, 0x0070507000000000, 0x00e0a0e000000000, 0x00c040c000000000,
    0x0302030000000000, 0x0705070000000000, 0x0e0a0e0000000000, 0x1c141c0000000000,
    0x3828380000000000, 0x7050700000000000, 0xe0a0e00000000000, 0xc040c00000000000,
    0x0203000000000000, 0x0507000000000000, 0x0a0e000000000000, 0x141c000000000000,
    0x2838000000000000, 0x5070000000000000, 0xa0e0000000000000, 0x40c0000000000000
]

knight_attacks = [
    0x0000000000020400, 0x0000000000050800, 0x00000000000a1100, 0x0000000000142200,
    0x0000000000284400, 0x0000000000508800, 0x0000000000a01000, 0x0000000000402000,
    0x0000000002040004, 0x0000000005080008, 0x000000000a110011, 0x0000000014220022,
    0x0000000028440044, 0x0000000050880088, 0x00000000a0100010, 0x0000000040200020,
    0x0000000204000402, 0x0000000508000805, 0x0000000a1100110a, 0x0000001422002214,
    0x0000002844004428, 0x0000005088008850, 0x000000a0100010a0, 0x0000004020002040,
    0x0000020400040200, 0x0000050800080500, 0x00000a1100110a00, 0x0000142200221400,
    0x0000284400442800, 0x0000508800885000, 0x0000a0100010a000, 0x0000402000204000,
    0x0002040004020000, 0x0005080008050000, 0x000a1100110a0000, 0x0014220022140000,
    0x0028440044280000, 0x0050880088500000, 0x00a0100010a00000, 0x0040200020400000,
    0x0204000402000000, 0x0508000805000000, 0x0a1100110a000000, 0x1422002214000000,
    0x2844004428000000, 0x5088008850000000, 0xa0100010a0000000, 0x4020002040000000,
    0x0400040200000000, 0x0800080500000000, 0x1100110a00000000, 0x2200221400000000,
    0x4400442800000000, 0x8800885000000000, 0x100010a000000000, 0x2000204000000000,
    0x0004020000000000, 0x0008050000000000, 0x00110a0000000000, 0x0022140000000000,
    0x0044280000000000, 0x0088500000000000, 0x0010a00000000000, 0x0020400000000000
]

rook_magics = [
    0x0080001020400080, 0x0040001000200040, 0x0080081000200080, 0x0080040800100080,
    0x0080020400080080, 0x0080010200040080, 0x0080008001000200, 0x0080002040800100,
    0x0000800020400080, 0x0000400020005000, 0x0000801000200080, 0x0000800800100080,
    0x0000800400080080, 0x0000800200040080, 0x0000800100020080, 0x0000800040800100,
    0x0000208000400080, 0x0000404000201000, 0x0000808010002000, 0x0000808008001000,
    0x0000808004000800, 0x0000808002000400, 0x0000010100020004, 0x0000020000408104,
    0x0000208080004000, 0x0000200040005000, 0x0000100080200080, 0x0000080080100080,
    0x0000040080080080, 0x0000020080040080, 0x0000010080800200, 0x0000800080004100,
    0x0000204000800080, 0x0000200040401000, 0x0000100080802000, 0x0000080080801000,
    0x0000040080800800, 0x0000020080800400, 0x0000020001010004, 0x0000800040800100,
    0x0000204000808000, 0x0000200040008080, 0x0000100020008080, 0x0000080010008080,
    0x0000040008008080, 0x0000020004008080, 0x0000010002008080, 0x0000004081020004,
    0x0000204000800080, 0x0000200040008080, 0x0000100020008080, 0x0000080010008080,
    0x0000040008008080, 0x0000020004008080, 0x0000800100020080, 0x0000800041000080,
    0x00FFFCDDFCED714A, 0x007FFCDDFCED714A, 0x003FFFCDFFD88096, 0x0000040810002101,
    0x0001000204080011, 0x0001000204000801, 0x0001000082000401, 0x0001FFFAABFAD1A2
]

bishop_magics = [
    0x0002020202020200, 0x0002020202020000, 0x0004010202000000, 0x0004040080000000,
    0x0001104000000000, 0x0000821040000000, 0x0000410410400000, 0x0000104104104000,
    0x0000040404040400, 0x0000020202020200, 0x0000040102020000, 0x0000040400800000,
    0x0000011040000000, 0x0000008210400000, 0x0000004104104000, 0x0000002082082000,
    0x0004000808080800, 0x0002000404040400, 0x0001000202020200, 0x0000800802004000,
    0x0000800400A00000, 0x0000200100884000, 0x0000400082082000, 0x0000200041041000,
    0x0002080010101000, 0x0001040008080800, 0x0000208004010400, 0x0000404004010200,
    0x0000840000802000, 0x0000404002011000, 0x0000808001041000, 0x0000404000820800,
    0x0001041000202000, 0x0000820800101000, 0x0000104400080800, 0x0000020080080080,
    0x0000404040040100, 0x0000808100020100, 0x0001010100020800, 0x0000808080010400,
    0x0000820820004000, 0x0000410410002000, 0x0000082088001000, 0x0000002011000800,
    0x0000080100400400, 0x0001010101000200, 0x0002020202000400, 0x0001010101000200,
    0x0000410410400000, 0x0000208208200000, 0x0000002084100000, 0x0000000020880000,
    0x0000001002020000, 0x0000040408020000, 0x0004040404040000, 0x0002020202020000,
    0x0000104104104000, 0x0000002082082000, 0x0000000020841000, 0x0000000000208800,
    0x0000000010020200, 0x0000000404080200, 0x0000040404040400, 0x0002020202020200
]

rook_shifts = [
    52, 53, 53, 53, 53, 53, 53, 52,
    53, 54, 54, 54, 54, 54, 54, 53,
    53, 54, 54, 54, 54, 54, 54, 53,
    53, 54, 54, 54, 54, 54, 54, 53,
    53, 54, 54, 54, 54, 54, 54, 53,
    53, 54, 54, 54, 54, 54, 54, 53,
    53, 54, 54, 54, 54, 54, 54, 53,
    53, 54, 54, 53, 53, 53, 53, 53
]

bishop_shifts = [
    58, 59, 59, 59, 59, 59, 59, 58,
    59, 59, 59, 59, 59, 59, 59, 59,
    59, 59, 57, 57, 57, 57, 59, 59,
    59, 59, 57, 55, 55, 57, 59, 59,
    59, 59, 57, 55, 55, 57, 59, 59,
    59, 59, 57, 57, 57, 57, 59, 59,
    59, 59, 59, 59, 59, 59, 59, 59,
    58, 59, 59, 59, 59, 59, 59, 58
]

diagonal_vectors = [-9, -7, 7, 9]

orthogonal_vectors = [-8, -1, 1, 8]

a_file_offset_exceptions = [-9, -1, 7]

h_file_offset_exceptions = [-7, 1, 9]


def is_valid_vector_offset(sq, offset):
    a_file = (bits.files[0] & 1 << sq) != 0
    h_file = (bits.files[7] & 1 << sq) != 0
    is_a_file_exception = offset in a_file_offset_exceptions
    is_h_file_exception = offset in h_file_offset_exceptions
    return (not a_file or not is_a_file_exception) and (not h_file or not is_h_file_exception)


def init_movement_mask(sq, diagonal):
    movement_mask = 0
    vectors = diagonal_vectors if diagonal else orthogonal_vectors
    for vector in vectors:
        current_sq = sq
        if not is_valid_vector_offset(sq, vector):
            continue
        for distance in range(1, 8):
            current_sq += vector
            if Board.is_valid_square_index(current_sq + vector) and is_valid_vector_offset(current_sq, vector):
                movement_mask |= 1 << current_sq
            else:
                break
    return movement_mask


def init_attack_mask(sq, blockers, diagonal):
    attack_mask = 0
    vectors = diagonal_vectors if diagonal else orthogonal_vectors
    for vector in vectors:
        current_sq = sq
        for distance in range(1, 8):
            if Board.is_valid_square_index(current_sq + vector) and is_valid_vector_offset(current_sq, vector):
                current_sq += vector
                attack_mask |= 1 << current_sq
                if blockers & 1 << current_sq:
                    break
            else:
                break
    return attack_mask


def init_magic_masks(diagonal):
    return [init_movement_mask(sq, diagonal) for sq in range(64)]


def init_blocker_masks(movement_mask):
    move_squares = []
    for sq in range(64):
        if (movement_mask & 1 << sq) != 0:
            move_squares.append(sq)
    pattern_count = 1 << len(move_squares)
    blocker_masks = [0] * pattern_count

    for pattern in range(pattern_count):
        for bit_index in range(len(move_squares)):
            # bit = ((pattern & 0xffffffff) >> bit_index) & 1
            bit = (pattern >> bit_index) & 1
            blocker_masks[pattern] |= bit << move_squares[bit_index]
    return blocker_masks


def init_magic_table(sq, diagonal, magic, shift):
    num_bits = 64 - shift
    table_size = 1 << num_bits
    table = [0] * table_size

    movement_mask = init_movement_mask(sq, diagonal)
    blocker_masks = init_blocker_masks(movement_mask)

    for blocker_mask in blocker_masks:
        # index = (blocker_mask * magic) & 0xffffffff >> shift
        index = (blocker_mask * magic) >> shift
        index &= (1 << (64 - shift)) - 1
        attacks = init_attack_mask(sq, blocker_mask, diagonal)
        table[index] = attacks

    return table


def init_magic_attacks(diagonal, magics, shifts):
    magic_attacks = [0] * 64
    for sq in range(64):
        magic_attacks[sq] = init_magic_table(sq, diagonal, magics[sq], shifts[sq])
    return magic_attacks


def init_magic_lookups(attacks, masks, magics, shifts):
    return [
        {
            "attacks": attacks[sq],
            "mask": masks[sq],
            "magic": magics[sq],
            "shift": shifts[sq]
        }
        for sq in range(64)]


rook_masks = init_magic_masks(False)

bishop_masks = init_magic_masks(True)

rook_attacks = init_magic_attacks(False, rook_magics, rook_shifts)

bishop_attacks = init_magic_attacks(True, bishop_magics, bishop_shifts)

rook_magic_lookups = init_magic_lookups(rook_attacks, rook_masks, rook_magics, rook_shifts)

bishop_magic_lookups = init_magic_lookups(bishop_attacks, bishop_masks, bishop_magics, bishop_shifts)


def bishop_attacks(sq, blockers):
    return slider_attacks(sq, blockers, bishop_magic_lookups)


def rook_attacks(sq, blockers):
    return slider_attacks(sq, blockers, rook_magic_lookups)


def slider_attacks(sq, occ, lookups):
    lookup = lookups[sq]
    occ &= lookup["mask"]
    occ *= lookup["magic"]
    occ &= 0xffffffffffffffff  # 64-bit mask to handle large integers
    occ >>= lookup["shift"]
    return lookup["attacks"][occ]