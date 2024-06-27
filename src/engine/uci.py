import sys

from src.board.board import Board
from src.board.colour import Colour
from src.search.search import Search
from src.util.notation import fen_to_board, move_to_notation, notation_to_move


class UCI:
    def __init__(self):
        self.board = Board()
        self.engine_name = "Hobbes"
        self.author = "Dan Kelsey"
        self.search = Search()

    def uci(self):
        print(f"id name {self.engine_name}")
        print(f"id author {self.author}")
        print("uciok")

    def isready(self):
        print("readyok")

    def ucinewgame(self):
        self.search = Search()
        self.board = Board()

    def position(self, command):
        tokens = command.split()
        moves = []
        if "startpos" in tokens:
            self.board = Board()
            if "moves" in tokens:
                moves_index = tokens.index("moves")
                moves = tokens[moves_index + 1:] if moves_index != -1 else []
        elif "fen" in tokens:
            fen_index = tokens.index("fen")
            fen = ' '.join(tokens[fen_index + 1:fen_index + 7])
            self.board = fen_to_board(fen)
            if "moves" in tokens:
                moves_index = tokens.index("moves")
                moves = tokens[moves_index + 1:] if moves_index != -1 else []
        for move in moves:
            self.board.make_move(notation_to_move(move))

    def go(self, command):
        movetime, wtime, btime, winc, binc = self.parse_go_command(command)
        if movetime:
            move = self.search.search(self.board, movetime)
            self.write_move(move)
        elif wtime and btime and winc and binc:
            think_time = self.choose_think_time(wtime, btime, winc, binc)
            move = self.search.search(self.board, think_time / 1000)
            self.write_move(move)

    def parse_go_command(self, command):
        # Default values
        movetime = None
        wtime = None
        btime = None
        winc = None
        binc = None

        parts = command.split()
        for idx in range(len(parts)):
            if parts[idx] == "movetime" and idx + 1 < len(parts):
                movetime = int(parts[idx + 1])
            elif parts[idx] == "wtime" and idx + 1 < len(parts):
                wtime = int(parts[idx + 1])
            elif parts[idx] == "btime" and idx + 1 < len(parts):
                btime = int(parts[idx + 1])
            elif parts[idx] == "winc" and idx + 1 < len(parts):
                winc = int(parts[idx + 1])
            elif parts[idx] == "binc" and idx + 1 < len(parts):
                binc = int(parts[idx + 1])

        return movetime, wtime, btime, winc, binc

    def choose_think_time(self, wtime, btime, winc, binc):
        is_white = self.board.colour == Colour.W
        time_remaining_ms = wtime if is_white else btime
        increment_ms = winc if is_white else binc

        optimal_think_time = min(time_remaining_ms * 0.5, time_remaining_ms * 0.03333 + increment_ms)
        if optimal_think_time > increment_ms * 2:
            optimal_think_time += increment_ms * 0.8

        min_think_time = min(50, int(time_remaining_ms * 0.25))
        think_time = max(optimal_think_time, min_think_time)

        return int(think_time)

    def write_move(self, move):
        print(f"bestmove {move_to_notation(move)}")

    def quit(self):
        sys.exit(0)

    def run(self):
        while True:
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
