import unittest
from src.data_structures.heap import Heap

class TestHeap(unittest.TestCase):

    def setUp(self):
        self.heap = Heap()

    def test_insert_and_get_min(self):
        self.heap.insert(10)
        self.heap.insert(5)
        self.heap.insert(20)
        self.assertEqual(self.heap.get_min(), 5)

    def test_delete_min(self):
        self.heap.insert(10)
        self.heap.insert(5)
        self.heap.insert(20)
        self.heap.delete_min()
        self.assertEqual(self.heap.get_min(), 10)

    def test_empty_heap(self):
        with self.assertRaises(IndexError):
            self.heap.get_min()
        with self.assertRaises(IndexError):
            self.heap.delete_min()

if __name__ == '__main__':
    unittest.main()