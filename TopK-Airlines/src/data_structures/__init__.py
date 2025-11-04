"""
Data structures package containing tree implementations for storing airline data.

Available structures:
- BinarySearchTree: Standard BST
- AVLTree: Self-balancing AVL tree
- RedBlackTree: Self-balancing Red-Black tree  
- Trie: Prefix tree for rating-based indexing
- Heap: Min/Max heap (existing)
- PriorityQueue: Priority queue (existing)
- HashTable: Hash table (existing)
"""

from .binary_search_tree import BinarySearchTree, BSTNode
from .avl_tree import AVLTree, AVLNode
from .red_black_tree import RedBlackTree, RBNode, Color
from .trie import Trie, TrieNode

__all__ = [
    'BinarySearchTree', 'BSTNode',
    'AVLTree', 'AVLNode',
    'RedBlackTree', 'RBNode', 'Color',
    'Trie', 'TrieNode'
]