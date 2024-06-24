import sys

from src.board.board import Board


class UCI:

    def __init__(self):
        self.board = Board()
        self.engine_name = "Hobbes"
        self.author = "Dan Kelsey"

    def uci(self):
        print(f"id name {self.engine_name}")
        print(f"id author {self.author}")
        print("uciok")

    def isready(self):
        print("readyok")

    def ucinewgame(self):
        self.board = Board()

    def position(self, command):
        tokens = command.split()
        if "startpos" in tokens:
            self.board.set_fen("")
            moves_index = tokens.index("moves")
            moves = tokens[moves_index + 1:] if moves_index != -1 else []
        elif "fen" in tokens:
            fen_index = tokens.index("fen")
            fen = ' '.join(tokens[fen_index + 1:fen_index + 7])
            self.board.set_fen(fen)
            moves_index = tokens.index("moves")
            moves = tokens[moves_index + 1:] if moves_index != -1 else []
        for move in moves:
            self.board.push_uci(move)

    def go(self, command):
        import random
        legal_moves = list(self.board.legal_moves)
        if legal_moves:
            best_move = random.choice(legal_moves)
            print(f"bestmove {best_move.uci()}")

    def quit(self):
        sys.exit(0)

    def run(self):
        while True:
            try:
                command = input().strip()
                if command == "uci":
                    self.uci()
                elif command == "isready":
                    self.isready()
                elif command == "ucinewgame":
                    self.ucinewgame()
                elif command.startswith("position"):
                    self.position(command)
                elif command.startswith("go"):
                    self.go(command)
                elif command == "quit":
                    self.quit()
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)

