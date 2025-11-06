"""
Sorted Array implementation for autocomplete functionality.
Uses binary search for prefix matching.
"""

import bisect
import time


class SortedArray:
    """
    Sorted Array for storing records indexed by string names.
    Uses binary search for efficient prefix matching.
    """
    
    def __init__(self):
        """Initialize an empty Sorted Array."""
        self.data = []  # List of (name, record) tuples, sorted by name
        self.comparisons = 0
        self.memory_usage = 0
    
    def _normalize_string(self, s):
        """Normalize string for insertion/search (lowercase, strip)."""
        if not s:
            return ""
        return str(s).lower().strip()
    
    def insert(self, key_string, data):
        """
        Insert a record into the sorted array.
        
        Args:
            key_string (str): String key (e.g., airline name)
            data (dict): Complete record data
        """
        normalized_key = self._normalize_string(key_string)
        if not normalized_key:
            return
        
        # Use bisect to find insertion point (maintains sorted order)
        original_name = str(key_string).strip()  # Keep original for display
        
        # Find insertion point - compare based on normalized_key
        # We need to extract just the key part for comparison
        insertion_point = bisect.bisect_left([item[0] for item in self.data], normalized_key)
        
        # Insert at the correct position
        self.data.insert(insertion_point, (normalized_key, original_name, data))
        self.memory_usage += len(str(data)) + len(key_string) + 50  # Approximate
    
    def search_prefix(self, prefix, max_results=10):
        """
        Search for all records with keys starting with the given prefix.
        
        Args:
            prefix (str): Prefix to search for
            max_results (int): Maximum number of results to return
            
        Returns:
            tuple: (results_list, metrics_dict)
        """
        start_time = time.perf_counter()
        comparisons = 0
        initial_memory = self.memory_usage
        
        normalized_prefix = self._normalize_string(prefix)
        if not normalized_prefix or not self.data:
            return [], {
                'comparisons': 0,
                'time_ms': 0,
                'memory_bytes': self.memory_usage,
                'results_count': 0
            }
        
        # Find the starting position using binary search
        # Extract just the keys for binary search
        keys = [item[0] for item in self.data]
        start_pos = bisect.bisect_left(keys, normalized_prefix)
        comparisons += 1
        
        # Collect all records that start with the prefix
        results = []
        i = start_pos
        
        while i < len(self.data):
            comparisons += 1
            normalized_name, original_name, record = self.data[i]
            
            # Check if this record starts with the prefix
            if normalized_name.startswith(normalized_prefix):
                results.append(record)
                comparisons += 1
                
                # Stop if we've reached max_results
                if len(results) >= max_results:
                    break
            else:
                # Since array is sorted, no more matches possible
                break
            
            i += 1
        
        elapsed = (time.perf_counter() - start_time) * 1000
        self.comparisons += comparisons
        
        return results[:max_results], {
            'comparisons': comparisons,
            'time_ms': elapsed,
            'memory_bytes': self.memory_usage,
            'results_count': len(results),
            'memory_delta': self.memory_usage - initial_memory
        }
    
    def get_size(self):
        """Get the number of records in the array."""
        return len(self.data)
    
    def get_height(self):
        """Sorted Array doesn't have a height concept, return 0."""
        return 0
    
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
        """String representation of the Sorted Array."""
        return f"SortedArray(size={len(self.data)}, memory={self.memory_usage} bytes)"

