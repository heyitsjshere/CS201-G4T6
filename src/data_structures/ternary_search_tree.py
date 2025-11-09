"""
Ternary Search Tree (TST) implementation for autocomplete functionality.
More space-efficient than Trie while maintaining fast prefix matching.
"""

import sys
from utils.performance_tracker import _deep_getsizeof


class TSTNode:
    """Node in a Ternary Search Tree."""
    
    def __init__(self, char):
        """
        Initialize a TST node.
        
        Args:
            char (str): Character stored at this node
        """
        self.char = char
        self.left = None
        self.middle = None
        self.right = None
        self.data_list = []  # List of records ending at this node
        self.is_end = False
        self.comparisons = 0


class TernarySearchTree:
    """
    Ternary Search Tree for storing records indexed by string names.
    Combines benefits of BST and Trie for space-efficient prefix matching.
    """
    
    def __init__(self):
        """Initialize an empty Ternary Search Tree."""
        self.root = None
        self.size = 0
        self.comparisons = 0
        self._cached_memory = None  # Cached memory calculation
        self._memory_dirty = True  # Flag to track if cache needs update
    
    def _normalize_string(self, s):
        """Normalize string for insertion (lowercase, strip)."""
        if not s:
            return ""
        return str(s).lower().strip()
    
    def insert(self, key_string, data):
        """
        Insert a record into the TST.

        Args:
            key_string (str): String key (e.g., airline name)
            data (dict): Complete record data
        """
        key = self._normalize_string(key_string)
        if not key:
            return

        self.root = self._insert_recursive(self.root, key, 0, data)
        self.size += 1
        self._memory_dirty = True  # Mark memory cache as dirty after insert

    def _insert_recursive(self, node, key, index, data):
        """Recursively insert into TST."""
        char = key[index]
        comparisons = 1

        if node is None:
            node = TSTNode(char)
        
        if char < node.char:
            node.left = self._insert_recursive(node.left, key, index, data)
            comparisons += 1
        elif char > node.char:
            node.right = self._insert_recursive(node.right, key, index, data)
            comparisons += 1
        elif index < len(key) - 1:
            node.middle = self._insert_recursive(node.middle, key, index + 1, data)
            comparisons += 1
        else:
            # End of string
            node.is_end = True
            node.data_list.append(data)
            comparisons += 1
        
        self.comparisons += comparisons
        return node
    
    def search_prefix(self, prefix, max_results=10):
        """
        Search for all records with keys starting with the given prefix.
        
        Args:
            prefix (str): Prefix to search for
            max_results (int): Maximum number of results to return
            
        Returns:
            tuple: (results_list, metrics_dict)
        """
        import time
        start_time = time.perf_counter()
        comparisons = 0

        normalized_prefix = self._normalize_string(prefix)
        if not normalized_prefix:
            return [], {
                'comparisons': 0,
                'time_ms': 0,
                'memory_bytes': 0,
                'results_count': 0
            }

        # Find the node where prefix ends using the recursive helper
        # The helper handles the complex TST traversal logic correctly
        node, comparisons = self._find_prefix_node(self.root, normalized_prefix, 0, 0)
        if node is None:
            elapsed = (time.perf_counter() - start_time) * 1000
            return [], {
                'comparisons': comparisons,
                'time_ms': elapsed,
                'memory_bytes': self.get_memory_usage(),
                'results_count': 0
            }

        # Collect all records from this node (including the node itself if it's an end node)
        # and all nodes in the middle subtree (continuations of the prefix)
        results = []
        comparisons = self._collect_records(node, results, comparisons, max_results)

        elapsed = (time.perf_counter() - start_time) * 1000
        self.comparisons += comparisons

        return results[:max_results], {
            'comparisons': comparisons,
            'time_ms': elapsed,
            'memory_bytes': self.get_memory_usage(),
            'results_count': len(results),
            'memory_delta': 0  # Not tracking delta with sys.getsizeof
        }
    
    def _find_prefix_node(self, node, prefix, index, comparisons):
        """
        Find the node where the prefix ends.
        This recursively searches the TST to find the node corresponding to the last character of the prefix.

        Returns:
            tuple: (node, comparisons) - The node where prefix ends and number of comparisons made
        """
        if node is None:
            return None, comparisons

        if index >= len(prefix):
            # We've matched the entire prefix, return this node
            return node, comparisons

        char = prefix[index]

        # Compare current node's character with the character we're looking for
        # This is ONE comparison that results in three possible branches
        comparisons += 1
        
        if char < node.char:
            # Character is smaller, search in left subtree
            return self._find_prefix_node(node.left, prefix, index, comparisons)
        elif char > node.char:
            # Character is larger, search in right subtree
            return self._find_prefix_node(node.right, prefix, index, comparisons)
        else:
            # Found matching character, move to next character in middle subtree
            if index == len(prefix) - 1:
                # This is the last character of the prefix, return this node
                return node, comparisons
            else:
                # There are more characters in the prefix, continue in middle subtree
                return self._find_prefix_node(node.middle, prefix, index + 1, comparisons)
    
    def _collect_records(self, node, results, comparisons, max_results):
        """
        Recursively collect all records from a node downwards.
        
        After finding the prefix node, we need to traverse ALL subtrees (left, middle, right)
        because strings that continue the prefix can be in any of these subtrees.
        
        The key insight: Once we've matched the entire prefix, any continuation is valid,
        regardless of whether it's in left/middle/right. However, left/right at the prefix node
        itself represent different characters at the SAME position as the prefix's last character,
        so they don't match. But once we go into middle (next position), then left/right in that
        middle subtree represent different continuations of the prefix, which we DO want.
        
        Actually, wait - let me reconsider. In a TST:
        - Left/Right: Different characters at the CURRENT position
        - Middle: Next position in the string
        
        So when we find the prefix node (e.g., 'a' at position 1 for prefix "qa"):
        - Left/Right of this node: Characters at position 1 that are not 'a' (don't match prefix)
        - Middle of this node: Position 2 (continuations of the prefix)
        
        But in the middle subtree, if there are multiple continuations:
        - Middle of middle: Next character in some strings
        - Left/Right of middle: Different characters at position 2 (e.g., 't' vs 'n' for "qatar" vs "qantas")
        
        So we DO need to traverse left/right in the middle subtree, but NOT left/right of the prefix node itself.
        
        Actually, the correct approach is:
        - Collect from current node if it's an end node
        - Traverse middle subtree (continuations), and recursively traverse left/right within that subtree
        """
        if node is None:
            return comparisons
        
        # Check if we've reached max_results before processing
        if len(results) >= max_results:
            return comparisons
        
        comparisons += 1
        
        # Collect records from this node if it's an end node
        # This handles the case where the prefix itself is a complete string
        if node.is_end:
            # Add records one by one to respect max_results limit
            for record in node.data_list:
                if len(results) >= max_results:
                    break
                results.append(record)
            comparisons += min(len(node.data_list), max_results - len(results) + len(node.data_list))
        
        # Traverse middle subtree (continuations of the prefix)
        # Within the middle subtree, we need to traverse ALL paths (left, middle, right)
        # because continuations can diverge at any position
        if node.middle is not None:
            comparisons = self._collect_all_from_node(node.middle, results, comparisons, max_results)
        
        return comparisons
    
    def _collect_all_from_node(self, node, results, comparisons, max_results):
        """
        Recursively collect ALL records from a node and all its subtrees.
        This is used to collect all continuations after we've matched the prefix.
        """
        if node is None or len(results) >= max_results:
            return comparisons
        
        comparisons += 1
        
        # Collect records from this node if it's an end node
        if node.is_end:
            for record in node.data_list:
                if len(results) >= max_results:
                    break
                results.append(record)
        
        # Traverse all three directions: left, middle, right
        # This ensures we get all continuations, regardless of how they diverge
        if node.left is not None:
            comparisons = self._collect_all_from_node(node.left, results, comparisons, max_results)
        
        if node.middle is not None:
            comparisons = self._collect_all_from_node(node.middle, results, comparisons, max_results)
        
        if node.right is not None:
            comparisons = self._collect_all_from_node(node.right, results, comparisons, max_results)
        
        return comparisons
    
    def get_size(self):
        """Get the number of records in the TST."""
        return self.size
    
    def get_height(self):
        """Get the height of the TST."""
        return self._get_height_recursive(self.root)
    
    def _get_height_recursive(self, node):
        """Recursively calculate TST height."""
        if node is None:
            return 0
        
        left_height = self._get_height_recursive(node.left)
        middle_height = self._get_height_recursive(node.middle)
        right_height = self._get_height_recursive(node.right)
        
        return 1 + max(left_height, middle_height, right_height)
    
    def get_total_comparisons(self):
        """Get total number of comparisons made."""
        return self.comparisons
    
    def get_memory_usage(self):
        """Get actual memory usage in bytes using sys.getsizeof with caching."""
        if self._memory_dirty or self._cached_memory is None:
            self._cached_memory = self._calculate_memory(self.root)
            self._memory_dirty = False
        return self._cached_memory

    def _calculate_memory(self, node, visited=None):
        """Recursively calculate memory usage of the TST with deep size calculation."""
        if visited is None:
            visited = set()
            
        if node is None or id(node) in visited:
            return 0
        
        visited.add(id(node))

        # Size of the node object itself
        memory = sys.getsizeof(node)

        # Size of the data_list
        memory += sys.getsizeof(node.data_list)

        # Deep size of each data item in the list
        for data in node.data_list:
            memory += _deep_getsizeof(data, visited)

        # Recursively calculate memory for all three children
        memory += self._calculate_memory(node.left, visited)
        memory += self._calculate_memory(node.middle, visited)
        memory += self._calculate_memory(node.right, visited)

        return memory
    
    def reset_comparisons(self):
        """Reset comparison counter."""
        self.comparisons = 0
    
    def __str__(self):
        """String representation of the TST."""
        return f"TernarySearchTree(size={self.size}, height={self.get_height()}, memory={self.get_memory_usage()} bytes)"

