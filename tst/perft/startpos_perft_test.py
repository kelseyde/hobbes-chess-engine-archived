import unittest

import src.movegen.perft as perft


class StartPosPerftTest(unittest.TestCase):

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def test_depth_1(self):
        nodes, time = perft.run_perft(self.fen, 1)
        self.assertEqual(20, nodes)

    def test_depth_2(self):
        nodes, time = perft.run_perft(self.fen, 2, debug=True)
        self.assertEqual(400, nodes)

    def test_depth_3(self):
        nodes, time = perft.run_perft(self.fen, 3, debug=True)
        self.assertEqual(8902, nodes)

    def test_depth_4(self):
        nodes, time = perft.run_perft(self.fen, 4, debug=False)
        self.assertEqual(197281, nodes)

    def test_depth_5(self):
        nodes, time = perft.run_perft(self.fen, 5, debug=False)
        self.assertEqual(4865609, nodes)

    def test_depth_6(self):
        nodes, time = perft.run_perft(self.fen, 6, debug=False)
        self.assertEqual(119060324, nodes)

    def test_debug(self):
        fen = "rnbqkbnr/pppp1ppp/8/4p3/3P4/P7/1PP1PPPP/RNBQKBNR b KQkq - 0 2"
        perft.run_perft(fen, 2, debug=True)

