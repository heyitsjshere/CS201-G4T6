"""
Filter Benchmarking Utilities

This module provides functions to measure time and space complexity
of filtering operations across different data structures.
"""

import time
import sys
import statistics
import tracemalloc
from typing import Dict, List, Callable, Any, Optional


class FilterBenchmark:
    """Benchmark filtering operations on tree data structures."""
    
    def __init__(self, tree, tree_name: str, dataset_name: str):
        """
        Initialize benchmark for a specific tree.
        
        Args:
            tree: Tree instance (BST, AVL, RedBlack, or Trie)
            tree_name: Name of tree type (e.g., 'BST', 'AVL')
            dataset_name: Name of dataset (e.g., 'airline', 'airport')
        """
        self.tree = tree
        self.tree_name = tree_name
        self.dataset_name = dataset_name
        self.dataset_size = tree.get_size()
    
    def measure_time(self, operation: Callable, *args, num_runs: int = 10, **kwargs) -> Dict[str, float]:
        """
        Measure execution time for an operation.
        
        Args:
            operation: Function/method to benchmark
            *args: Positional arguments for operation
            num_runs: Number of times to run the operation
            **kwargs: Keyword arguments for operation
            
        Returns:
            Dict with timing statistics (avg, min, max, std_dev) in milliseconds
        """
        times = []
        results_size = 0
        
        for _ in range(num_runs):
            start = time.perf_counter()
            result = operation(*args, **kwargs)
            elapsed = time.perf_counter() - start
            times.append(elapsed * 1000)  # Convert to milliseconds
            results_size = len(result) if hasattr(result, '__len__') else 0
        
        return {
            'avg_time_ms': sum(times) / len(times),
            'min_time_ms': min(times),
            'max_time_ms': max(times),
            'std_dev_ms': statistics.stdev(times) if len(times) > 1 else 0,
            'num_runs': num_runs,
            'results_count': results_size
        }
    
    def measure_space(self, operation: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Measure memory usage for an operation.
        
        Args:
            operation: Function/method to benchmark
            *args: Positional arguments for operation
            **kwargs: Keyword arguments for operation
            
        Returns:
            Dict with space statistics
        """
        # Start memory tracking
        tracemalloc.start()
        
        # Execute operation
        start_snapshot = tracemalloc.take_snapshot()
        result = operation(*args, **kwargs)
        end_snapshot = tracemalloc.take_snapshot()
        
        # Calculate memory difference
        stats = end_snapshot.compare_to(start_snapshot, 'lineno')
        
        total_memory = sum(stat.size_diff for stat in stats)
        peak_memory = tracemalloc.get_traced_memory()[1]
        
        tracemalloc.stop()
        
        # Calculate result size
        results_size = len(result) if hasattr(result, '__len__') else 0
        result_memory = sys.getsizeof(result)
        
        return {
            'memory_allocated_bytes': total_memory,
            'memory_allocated_kb': total_memory / 1024,
            'memory_allocated_mb': total_memory / (1024 ** 2),
            'peak_memory_bytes': peak_memory,
            'peak_memory_kb': peak_memory / 1024,
            'peak_memory_mb': peak_memory / (1024 ** 2),
            'result_size_bytes': result_memory,
            'result_size_kb': result_memory / 1024,
            'results_count': results_size
        }
    
    def benchmark_rating_filter(self, min_rating: float, max_rating: float, 
                               num_runs: int = 10) -> Dict[str, Any]:
        """
        Benchmark filter_by_rating operation.
        
        Args:
            min_rating: Minimum rating for filter
            max_rating: Maximum rating for filter
            num_runs: Number of runs for timing
            
        Returns:
            Complete benchmark results including time and space metrics
        """
        # Measure time
        time_stats = self.measure_time(
            self.tree.filter_by_rating,
            min_rating, max_rating,
            num_runs=num_runs
        )
        
        # Measure space (single run to avoid memory interference)
        space_stats = self.measure_space(
            self.tree.filter_by_rating,
            min_rating, max_rating
        )
        
        # Calculate selectivity
        results_count = time_stats['results_count']
        selectivity = results_count / self.dataset_size if self.dataset_size > 0 else 0
        
        return {
            'tree_type': self.tree_name,
            'dataset': self.dataset_name,
            'dataset_size': self.dataset_size,
            'operation': 'filter_by_rating',
            'filter_params': {
                'min_rating': min_rating,
                'max_rating': max_rating
            },
            'time_complexity': time_stats,
            'space_complexity': space_stats,
            'selectivity': selectivity,
            'selectivity_percent': selectivity * 100
        }
    
    def benchmark_field_filter(self, field_name: str, value: Any = None,
                              condition: str = 'equals', num_runs: int = 10) -> Dict[str, Any]:
        """
        Benchmark filter_by_field operation.
        
        Args:
            field_name: Field to filter by
            value: Value to filter for
            condition: Filter condition
            num_runs: Number of runs for timing
            
        Returns:
            Complete benchmark results
        """
        # Measure time
        time_stats = self.measure_time(
            self.tree.filter_by_field,
            field_name, value=value, condition=condition,
            num_runs=num_runs
        )
        
        # Measure space
        space_stats = self.measure_space(
            self.tree.filter_by_field,
            field_name, value=value, condition=condition
        )
        
        # Calculate selectivity
        results_count = time_stats['results_count']
        selectivity = results_count / self.dataset_size if self.dataset_size > 0 else 0
        
        return {
            'tree_type': self.tree_name,
            'dataset': self.dataset_name,
            'dataset_size': self.dataset_size,
            'operation': 'filter_by_field',
            'filter_params': {
                'field_name': field_name,
                'value': value,
                'condition': condition
            },
            'time_complexity': time_stats,
            'space_complexity': space_stats,
            'selectivity': selectivity,
            'selectivity_percent': selectivity * 100
        }
    
    def benchmark_multi_criteria(self, filters: Dict[str, Any], 
                                num_runs: int = 10) -> Dict[str, Any]:
        """
        Benchmark filter_multi_criteria operation.
        
        Args:
            filters: Dictionary of filter criteria
            num_runs: Number of runs for timing
            
        Returns:
            Complete benchmark results
        """
        # Measure time
        time_stats = self.measure_time(
            self.tree.filter_multi_criteria,
            filters,
            num_runs=num_runs
        )
        
        # Measure space
        space_stats = self.measure_space(
            self.tree.filter_multi_criteria,
            filters
        )
        
        # Calculate selectivity
        results_count = time_stats['results_count']
        selectivity = results_count / self.dataset_size if self.dataset_size > 0 else 0
        
        return {
            'tree_type': self.tree_name,
            'dataset': self.dataset_name,
            'dataset_size': self.dataset_size,
            'operation': 'filter_multi_criteria',
            'filter_params': filters,
            'time_complexity': time_stats,
            'space_complexity': space_stats,
            'selectivity': selectivity,
            'selectivity_percent': selectivity * 100
        }


def compare_trees(trees: Dict[str, Any], dataset_name: str, 
                 benchmark_func: Callable, *args, **kwargs) -> List[Dict[str, Any]]:
    """
    Compare filtering performance across multiple tree types.
    
    Args:
        trees: Dictionary of tree instances {'BST': bst, 'AVL': avl, ...}
        dataset_name: Name of dataset being tested
        benchmark_func: Benchmark function to use
        *args: Arguments for benchmark function
        **kwargs: Keyword arguments for benchmark function
        
    Returns:
        List of benchmark results for each tree
    """
    results = []
    
    for tree_name, tree in trees.items():
        print(f"\nBenchmarking {tree_name}...")
        benchmark = FilterBenchmark(tree, tree_name, dataset_name)
        
        try:
            result = benchmark_func(benchmark, *args, **kwargs)
            results.append(result)
            
            # Print summary
            time_stats = result['time_complexity']
            space_stats = result['space_complexity']
            print(f"   Avg Time: {time_stats['avg_time_ms']:.3f}ms")
            print(f"   Results: {time_stats['results_count']:,} ({result['selectivity_percent']:.2f}%)")
            print(f"   Memory: {space_stats['memory_allocated_kb']:.2f} KB")
        except Exception as e:
            print(f"   ERROR: {e}")
    
    return results


def run_comprehensive_benchmark(trees: Dict[str, Any], dataset_name: str) -> Dict[str, List[Dict]]:
    """
    Run comprehensive filtering benchmarks across all trees.
    
    Args:
        trees: Dictionary of tree instances
        dataset_name: Name of dataset
        
    Returns:
        Dictionary containing all benchmark results organized by test type
    """
    print("=" * 80)
    print(f"COMPREHENSIVE FILTERING BENCHMARK - {dataset_name.upper()}")
    print("=" * 80)
    
    all_results = {
        'rating_filters': [],
        'field_filters': [],
        'multi_criteria_filters': []
    }
    
    # Test 1: Rating filters (different selectivity levels)
    print("\n" + "=" * 80)
    print("TEST 1: Rating Filters (Indexed Field)")
    print("=" * 80)
    
    rating_ranges = [
        (4.5, 5.0, "High selectivity"),
        (3.0, 4.0, "Medium selectivity"),
        (1.0, 3.0, "Low selectivity"),
    ]
    
    for min_rating, max_rating, desc in rating_ranges:
        print(f"\nTesting: {desc} (Rating {min_rating}-{max_rating})")
        print("-" * 80)
        
        results = compare_trees(
            trees, dataset_name,
            lambda b: b.benchmark_rating_filter(min_rating, max_rating, num_runs=10)
        )
        all_results['rating_filters'].extend(results)
    
    # Test 2: Field filters (non-indexed)
    print("\n" + "=" * 80)
    print("TEST 2: Field Filters (Non-Indexed Fields)")
    print("=" * 80)
    
    field_tests = [
        ('recommended', True, 'equals', "Recommended only"),
    ]
    
    for field, value, condition, desc in field_tests:
        print(f"\nTesting: {desc} ({field}={value})")
        print("-" * 80)
        
        results = compare_trees(
            trees, dataset_name,
            lambda b: b.benchmark_field_filter(field, value=value, condition=condition, num_runs=10)
        )
        all_results['field_filters'].extend(results)
    
    # Test 3: Multi-criteria filters
    print("\n" + "=" * 80)
    print("TEST 3: Multi-Criteria Filters")
    print("=" * 80)
    
    multi_filters = [
        {
            'rating': {'min': 4.0, 'max': 5.0},
            'recommended': {'value': True}
        }
    ]
    
    for filters in multi_filters:
        print(f"\nTesting: Multi-criteria filter")
        print(f"   Filters: {filters}")
        print("-" * 80)
        
        results = compare_trees(
            trees, dataset_name,
            lambda b: b.benchmark_multi_criteria(filters, num_runs=10)
        )
        all_results['multi_criteria_filters'].extend(results)
    
    return all_results


def print_comparison_summary(results: Dict[str, List[Dict]]):
    """
    Print a summary comparing performance across data structures.
    
    Args:
        results: Dictionary of benchmark results
    """
    print("\n" + "=" * 80)
    print("PERFORMANCE COMPARISON SUMMARY")
    print("=" * 80)
    
    for test_type, test_results in results.items():
        if not test_results:
            continue
        
        print(f"\n{test_type.replace('_', ' ').title()}")
        print("-" * 80)
        
        # Group by operation parameters
        operations = {}
        for result in test_results:
            key = str(result['filter_params'])
            if key not in operations:
                operations[key] = []
            operations[key].append(result)
        
        for params, op_results in operations.items():
            print(f"\n  Filter: {params}")
            
            # Sort by average time
            op_results.sort(key=lambda x: x['time_complexity']['avg_time_ms'])
            
            for i, result in enumerate(op_results, 1):
                time_ms = result['time_complexity']['avg_time_ms']
                memory_kb = result['space_complexity']['memory_allocated_kb']
                tree = result['tree_type']
                
                print(f"    {i}. {tree:12} | Time: {time_ms:8.3f}ms | Memory: {memory_kb:8.2f}KB")

