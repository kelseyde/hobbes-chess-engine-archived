from datetime import datetime

from src.board import bits
from src.board.bitwise import lsb

start = datetime.now()
for _ in range(40000000):
    bb = lsb(bits.white_queenside_castle_safe_mask)
end = datetime.now()
print(end - start)
