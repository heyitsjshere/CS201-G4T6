"""
Sorting algorithms with comparison counting for performance analysis.
"""


class SortingAlgorithms:
    """Collection of sorting algorithms with performance tracking."""
    
    def __init__(self):
        """Initialize sorting algorithms."""
        self.comparisons = 0
    
    def reset_comparisons(self):
        """Reset comparison counter."""
        self.comparisons = 0
    
    def quicksort(self, arr, key_func=None, reverse=False):
        """
        Quick Sort algorithm with comparison counting.
        
        Args:
            arr: List to sort
            key_func: Function to extract sort key from elements
            reverse: If True, sort in descending order
            
        Returns:
            tuple: (sorted_list, metrics_dict)
        """
        import time
        import copy
        
        start_time = time.perf_counter()
        self.comparisons = 0
        
        # Create a copy to avoid modifying original
        arr_copy = copy.deepcopy(arr)
        
        if key_func is None:
            key_func = lambda x: x['overall_rating'] if isinstance(x, dict) else x
        
        def compare(a, b):
            self.comparisons += 1
            key_a = key_func(a)
            key_b = key_func(b)
            if reverse:
                return key_b - key_a
            return key_a - key_b
        
        def partition(low, high):
            pivot = arr_copy[high]
            i = low - 1
            
            for j in range(low, high):
                if compare(arr_copy[j], pivot) <= 0:
                    i += 1
                    arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]
            
            arr_copy[i + 1], arr_copy[high] = arr_copy[high], arr_copy[i + 1]
            return i + 1
        
        def quicksort_recursive(low, high):
            if low < high:
                pi = partition(low, high)
                quicksort_recursive(low, pi - 1)
                quicksort_recursive(pi + 1, high)
        
        quicksort_recursive(0, len(arr_copy) - 1)
        
        elapsed = (time.perf_counter() - start_time) * 1000
        
        return arr_copy, {
            'algorithm': 'quicksort',
            'comparisons': self.comparisons,
            'time_ms': elapsed,
            'items_sorted': len(arr),
            'memory_bytes': len(arr) * 100  # Approximate
        }
    
    def mergesort(self, arr, key_func=None, reverse=False):
        """
        Merge Sort algorithm with comparison counting.
        
        Args:
            arr: List to sort
            key_func: Function to extract sort key from elements
            reverse: If True, sort in descending order
            
        Returns:
            tuple: (sorted_list, metrics_dict)
        """
        import time
        import copy
        
        start_time = time.perf_counter()
        self.comparisons = 0
        
        arr_copy = copy.deepcopy(arr)
        
        if key_func is None:
            key_func = lambda x: x['overall_rating'] if isinstance(x, dict) else x
        
        def compare(a, b):
            self.comparisons += 1
            key_a = key_func(a)
            key_b = key_func(b)
            if reverse:
                return key_b < key_a
            return key_a < key_b
        
        def merge(left, right):
            result = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                if compare(left[i], right[j]):
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def mergesort_recursive(arr):
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left = mergesort_recursive(arr[:mid])
            right = mergesort_recursive(arr[mid:])
            
            return merge(left, right)
        
        sorted_arr = mergesort_recursive(arr_copy)
        
        elapsed = (time.perf_counter() - start_time) * 1000
        
        return sorted_arr, {
            'algorithm': 'mergesort',
            'comparisons': self.comparisons,
            'time_ms': elapsed,
            'items_sorted': len(arr),
            'memory_bytes': len(arr) * 100 * 2  # Merge sort uses extra space
        }
    
    def timsort(self, arr, key_func=None, reverse=False):
        """
        Timsort (Python's built-in sort) with comparison counting.
        Note: We can't actually count comparisons in Python's built-in sort,
        but we can measure time and estimate comparisons.
        
        Args:
            arr: List to sort
            key_func: Function to extract sort key from elements
            reverse: If True, sort in descending order
            
        Returns:
            tuple: (sorted_list, metrics_dict)
        """
        import time
        import copy
        
        start_time = time.perf_counter()
        
        arr_copy = copy.deepcopy(arr)
        
        if key_func is None:
            key_func = lambda x: x['overall_rating'] if isinstance(x, dict) else x
        
        # Python's built-in sort
        arr_copy.sort(key=key_func, reverse=reverse)
        
        elapsed = (time.perf_counter() - start_time) * 1000
        
        # Estimate comparisons (Timsort is O(n log n) in worst case)
        n = len(arr)
        estimated_comparisons = int(n * (n.bit_length() - 1))  # Approximate n*log2(n)
        
        return arr_copy, {
            'algorithm': 'timsort',
            'comparisons': estimated_comparisons,  # Estimated
            'time_ms': elapsed,
            'items_sorted': len(arr),
            'memory_bytes': len(arr) * 100
        }
    
    def tree_inorder_sort(self, tree, reverse=False):
        """
        Get sorted list from tree using in-order traversal.
        This is the most efficient for trees.
        
        Args:
            tree: Tree object with _inorder_traversal or similar method
            reverse: If True, reverse the result (descending order)
            
        Returns:
            tuple: (sorted_list, metrics_dict)
        """
        import time
        
        start_time = time.perf_counter()
        self.comparisons = 0
        
        results = []
        
        # Try different tree traversal methods
        if hasattr(tree, '_inorder_traversal'):
            tree._inorder_traversal(tree.root, results)
        elif hasattr(tree, 'inorder_traversal'):
            tree.inorder_traversal(tree.root, results)
        elif hasattr(tree, 'get_all_records'):
            results = tree.get_all_records()
        else:
            # Fallback: try to get all records
            results = []
            if hasattr(tree, 'root'):
                self._inorder_traversal_helper(tree.root, results)
        
        # Comparisons: one per node visited
        self.comparisons = len(results)
        
        if reverse:
            results.reverse()
            # Reverse is O(1) operation, no comparisons needed
        
        elapsed = (time.perf_counter() - start_time) * 1000
        
        return results, {
            'algorithm': 'tree_inorder',
            'comparisons': self.comparisons,
            'time_ms': elapsed,
            'items_sorted': len(results),
            'memory_bytes': len(results) * 100
        }
    
    def _inorder_traversal_helper(self, node, results):
        """Helper for in-order traversal."""
        if node is None:
            return
        
        if hasattr(node, 'left'):
            self._inorder_traversal_helper(node.left, results)
        
        if hasattr(node, 'data'):
            results.append(node.data)
        elif hasattr(node, 'data_list'):
            results.extend(node.data_list)
        
        if hasattr(node, 'right'):
            self._inorder_traversal_helper(node.right, results)

