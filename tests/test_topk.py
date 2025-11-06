# test_topk.py

import unittest
from src.algorithms.topk import TopKAirlines

class TestTopKAirlines(unittest.TestCase):

    def setUp(self):
        self.topk = TopKAirlines()

    def test_add_airline(self):
        self.topk.add_airline("Airline A", 4.5)
        self.assertIn("Airline A", self.topk.airlines)

    def test_get_top_k(self):
        self.topk.add_airline("Airline A", 4.5)
        self.topk.add_airline("Airline B", 4.7)
        self.topk.add_airline("Airline C", 4.2)
        top_k = self.topk.get_top_k(2)
        self.assertEqual(len(top_k), 2)
        self.assertIn("Airline B", top_k)
        self.assertIn("Airline A", top_k)

    def test_empty_top_k(self):
        top_k = self.topk.get_top_k(3)
        self.assertEqual(top_k, [])

if __name__ == '__main__':
    unittest.main()