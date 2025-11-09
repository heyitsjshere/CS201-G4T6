"""
Performance tracking utilities for measuring time, space, and comparisons.
"""

import time
import sys
from contextlib import contextmanager
from typing import Dict, Any


class PerformanceTracker:
    """Track performance metrics for operations."""
    
    def __init__(self):
        """Initialize performance tracker."""
        self.comparisons = 0
        self.operations = []
    
    def reset(self):
        """Reset all metrics."""
        self.comparisons = 0
        self.operations = []
    
    def add_comparison(self, count=1):
        """Add to comparison count."""
        self.comparisons += count
    
    def get_comparisons(self):
        """Get total comparisons."""
        return self.comparisons
    
    @contextmanager
    def track_operation(self, operation_name: str):
        """Context manager to track an operation."""
        start_time = time.perf_counter()
        start_memory = sys.getsizeof(self)
        initial_comparisons = self.comparisons
        
        try:
            yield self
        finally:
            elapsed = (time.perf_counter() - start_time) * 1000  # milliseconds
            end_memory = sys.getsizeof(self)
            memory_delta = end_memory - start_memory
            comparisons_delta = self.comparisons - initial_comparisons
            
            self.operations.append({
                'operation': operation_name,
                'time_ms': elapsed,
                'memory_bytes': end_memory,
                'memory_delta': memory_delta,
                'comparisons': comparisons_delta
            })
    
    def get_metrics(self, operation_name: str = None) -> Dict[str, Any]:
        """Get performance metrics for an operation."""
        if operation_name:
            for op in self.operations:
                if op['operation'] == operation_name:
                    return op
            return {}
        
        # Return summary
        if self.operations:
            latest = self.operations[-1]
            return {
                'time_ms': latest['time_ms'],
                'memory_bytes': latest['memory_bytes'],
                'comparisons': latest['comparisons'],
                'total_comparisons': self.comparisons
            }
        return {
            'time_ms': 0,
            'memory_bytes': 0,
            'comparisons': 0,
            'total_comparisons': self.comparisons
        }


def get_memory_usage(obj):
    """Get approximate memory usage of an object."""
    return sys.getsizeof(obj)


def estimate_memory_usage_tree(node, visited=None):
    """Estimate memory usage of a tree structure."""
    if visited is None:
        visited = set()
    
    if node is None or id(node) in visited:
        return 0
    
    visited.add(id(node))
    memory = sys.getsizeof(node)
    
    # Add children
    if hasattr(node, 'left'):
        memory += estimate_memory_usage_tree(node.left, visited)
    if hasattr(node, 'right'):
        memory += estimate_memory_usage_tree(node.right, visited)
    if hasattr(node, 'children'):
        if isinstance(node.children, dict):
            for child in node.children.values():
                memory += estimate_memory_usage_tree(child, visited)
        elif isinstance(node.children, list):
            for child in node.children:
                memory += estimate_memory_usage_tree(child, visited)
    
    # Add data - use deep size for dictionaries to account for all keys/values
    if hasattr(node, 'data'):
        memory += _deep_getsizeof(node.data, visited)
    if hasattr(node, 'data_list'):
        memory += sys.getsizeof(node.data_list)
        for item in node.data_list:
            memory += _deep_getsizeof(item, visited)
    
    return memory


def _deep_getsizeof(obj, visited):
    """
    Recursively calculate deep size of an object including all referenced objects.
    This properly accounts for dictionaries, lists, and nested structures.
    """
    if id(obj) in visited:
        return 0
    
    visited.add(id(obj))
    size = sys.getsizeof(obj)
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            size += _deep_getsizeof(key, visited)
            size += _deep_getsizeof(value, visited)
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            size += _deep_getsizeof(item, visited)
    
    return size


def estimate_memory_usage_hashmap(hash_map):
    """
    Estimate memory usage of a HashMap structure.
    Traverses all buckets and deeply measures stored data.
    """
    if hash_map is None:
        return 0
    
    visited = set()
    total = sys.getsizeof(hash_map)
    buckets = getattr(hash_map, 'buckets', None)
    
    if buckets is not None:
        total += sys.getsizeof(buckets)
        for bucket in buckets:
            total += sys.getsizeof(bucket)
            for rating, data_list in bucket:
                total += sys.getsizeof(rating)
                total += sys.getsizeof(data_list)
                for item in data_list:
                    total += _deep_getsizeof(item, visited)
    
    return total

