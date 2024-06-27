from enum import Enum

ENTRY_SIZE_BYTES = 32
CHECKMATE_BOUND = 1000000 - 256


class TranspositionTable:

    def __init__(self, size_mb):
        self.size = (size_mb * 1024 * 1024) // ENTRY_SIZE_BYTES
        assert (self.size & (self.size - 1)) == 0, "Size must be a power of 2"
        self.mask = self.size - 1  # Mask to get lower bits for indexing
        self.table = [None] * self.size
        self.tries = 0
        self.hits = 0

    def store(self, zobrist, depth, score, best_move, flag):
        index = self.index(zobrist)
        self.table[index] = (zobrist, depth, score, best_move, flag)

    def lookup(self, zobrist):
        self.tries += 1
        index = self.index(zobrist)
        entry = self.table[index]
        if entry is not None and entry[0] == zobrist:
            self.hits += 1
            return entry
        return None

    def clear(self):
        self.tries = 0
        self.hits = 0
        self.table = [None] * self.size

    def index(self, key):
        return key & self.mask

    def get_hit_rate(self):
        return self.hits / self.tries if self.tries > 0 else 0.0


class HashFlag(Enum):
    EXACT = 0
    LOWER = 1
    UPPER = 2
