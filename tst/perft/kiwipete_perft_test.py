import unittest

import src.movegen.perft as perft


class KiwiPetePerftTest(unittest.TestCase):

    fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"

    def test_depth_1(self):
        nodes, time = perft.run_perft(self.fen, 1)
        self.assertEqual(48, nodes)

    def test_depth_2(self):
        nodes, time = perft.run_perft(self.fen, 2, debug=False)
        self.assertEqual(2039, nodes)

    def test_depth_3(self):
        nodes, time = perft.run_perft(self.fen, 3, debug=False)
        self.assertEqual(97862, nodes)

    def test_depth_4(self):
        nodes, time = perft.run_perft(self.fen, 4, debug=False)
        self.assertEqual(4085603, nodes)

    def test_depth_5(self):
        nodes, time = perft.run_perft(self.fen, 5, debug=False)
        self.assertEqual(193690690, nodes)