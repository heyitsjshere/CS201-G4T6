"""
String Trie (Prefix Tree) implementation for autocomplete functionality.
Stores strings (e.g., airline names) for fast prefix matching.
"""


class StringTrieNode:
    """Node in a String Trie."""
    
    def __init__(self):
        """Initialize a Trie node."""
        self.children = {}  # char -> StringTrieNode
        self.data_list = []  # List of records ending at this node
        self.is_end = False
        self.comparisons = 0  # Track comparisons for this node


class StringTrie:
    """
    String Trie (Prefix Tree) for storing records indexed by string names.
    Optimized for autocomplete/prefix matching.
    """
    
    def __init__(self):
        """Initialize an empty String Trie."""
        self.root = StringTrieNode()
        self.size = 0
        self.comparisons = 0  # Total comparisons across all operations
        self.memory_usage = 0  # Approximate memory usage in bytes
    
    def _normalize_string(self, s):
        """Normalize string for insertion (lowercase, strip)."""
        if not s:
            return ""
        return str(s).lower().strip()
    
    def insert(self, key_string, data):
        """
        Insert a record into the Trie.
        
        Args:
            key_string (str): String key (e.g., airline name)
            data (dict): Complete record data
        """
        key = self._normalize_string(key_string)
        if not key:
            return
        
        node = self.root
        comparisons = 0
        
        # Traverse/create path for each character
        for char in key:
            comparisons += 1
            if char not in node.children:
                node.children[char] = StringTrieNode()
                self.memory_usage += 50  # Approximate per node
            node = node.children[char]
        
        # Store data at the end node
        node.is_end = True
        node.data_list.append(data)
        self.size += 1
        self.comparisons += comparisons
        self.memory_usage += len(str(data))  # Approximate data size
    
    def search_prefix(self, prefix, max_results=10):
        """
        Search for all records with keys starting with the given prefix.
        
        Args:
            prefix (str): Prefix to search for
            max_results (int): Maximum number of results to return
            
        Returns:
            tuple: (results_list, metrics_dict)
                - results_list: List of matching records
                - metrics_dict: Performance metrics (comparisons, time, etc.)
        """
        import time
        start_time = time.perf_counter()
        comparisons = 0
        initial_memory = self.memory_usage
        
        normalized_prefix = self._normalize_string(prefix)
        if not normalized_prefix:
            return [], {
                'comparisons': 0,
                'time_ms': 0,
                'memory_bytes': 0,
                'results_count': 0
            }
        
        node = self.root
        
        # Traverse to the prefix node
        for char in normalized_prefix:
            comparisons += 1
            if char not in node.children:
                # Prefix not found
                elapsed = (time.perf_counter() - start_time) * 1000
                return [], {
                    'comparisons': comparisons,
                    'time_ms': elapsed,
                    'memory_bytes': self.memory_usage,
                    'results_count': 0
                }
            node = node.children[char]
        
        # Collect all records under this prefix
        results = []
        comparisons = self._collect_records(node, results, comparisons, max_results)
        
        elapsed = (time.perf_counter() - start_time) * 1000
        self.comparisons += comparisons
        
        return results[:max_results], {
            'comparisons': comparisons,
            'time_ms': elapsed,
            'memory_bytes': self.memory_usage,
            'results_count': len(results),
            'memory_delta': self.memory_usage - initial_memory
        }
    
    def _collect_records(self, node, results, comparisons, max_results):
        """
        Recursively collect all records from a node downwards.
        We collect ALL records from each node to allow proper averaging.
        The API will deduplicate by name and calculate averages.
        """
        if node is None:
            return comparisons
        
        # Collect ALL records from this node if it's an end node
        # This allows us to calculate proper averages across all reviews
        comparisons += 1
        if node.is_end and node.data_list:
            # Add all records from this node (all reviews for this airline/airport/etc)
            results.extend(node.data_list)
            comparisons += len(node.data_list)
        
        # Stop if we have enough results
        if len(results) >= max_results:
            return comparisons
        
        # Traverse children to find more records
        for child in node.children.values():
            if len(results) >= max_results:
                break
            comparisons = self._collect_records(child, results, comparisons, max_results)
        
        return comparisons
    
    def get_size(self):
        """Get the number of records in the trie."""
        return self.size
    
    def get_height(self):
        """Get the height of the trie."""
        return self._get_height_recursive(self.root)
    
    def _get_height_recursive(self, node):
        """Recursively calculate trie height."""
        if not node.children:
            return 0
        return 1 + max(self._get_height_recursive(child) 
                      for child in node.children.values())
    
    def get_total_comparisons(self):
        """Get total number of comparisons made."""
        return self.comparisons
    
    def get_memory_usage(self):
        """Get approximate memory usage in bytes."""
        return self.memory_usage
    
    def reset_comparisons(self):
        """Reset comparison counter."""
        self.comparisons = 0
    
    def __str__(self):
        """String representation of the Trie."""
        return f"StringTrie(size={self.size}, height={self.get_height()}, memory={self.memory_usage} bytes)"

