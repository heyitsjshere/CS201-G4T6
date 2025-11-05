"""
Example: Filtering Operations on Tree Data Structures

This script demonstrates how to use the filtering functionality
added to all tree data structures (BST, AVL, Red-Black, Trie).
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.tree_persistence import load_trees
from utils.filter_benchmarks import FilterBenchmark, compare_trees


def example_1_basic_rating_filter():
    """Example 1: Basic rating-based filtering."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Rating Filter")
    print("=" * 80)
    
    # Load trees
    trees = load_trees('airline')
    tree = trees['AVL']
    
    # Filter high-rated airlines
    print("\nFiltering airlines with rating 4.5-5.0...")
    high_rated = tree.filter_by_rating(min_rating=4.5, max_rating=5.0)
    
    print(f"\nFound {len(high_rated):,} highly-rated airlines")
    print(f"  Dataset size: {tree.get_size():,} records")
    print(f"  Selectivity: {len(high_rated) / tree.get_size() * 100:.2f}%")
    
    print("\nTop 5 results:")
    for i, record in enumerate(high_rated[:5], 1):
        print(f"  {i}. {record['airline_name'][:40]:40} | Rating: {record['overall_rating']:.1f}")


def example_2_field_filter():
    """Example 2: Filter by non-indexed field."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Field Filter (Non-Indexed)")
    print("=" * 80)
    
    # Load trees
    trees = load_trees('airline')
    tree = trees['AVL']
    
    # Filter recommended airlines
    print("\nFiltering recommended airlines only...")
    recommended = tree.filter_by_field('recommended', value=True, condition='equals')
    
    print(f"\nFound {len(recommended):,} recommended airlines")
    print(f"  Dataset size: {tree.get_size():,} records")
    print(f"  Selectivity: {len(recommended) / tree.get_size() * 100:.2f}%")
    
    # Show rating distribution
    ratings = [r['overall_rating'] for r in recommended]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    print(f"\nStatistics:")
    print(f"  Average rating: {avg_rating:.2f}")
    print(f"  Max rating: {max(ratings):.1f}")
    print(f"  Min rating: {min(ratings):.1f}")


def example_3_multi_criteria():
    """Example 3: Multi-criteria filtering."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Multi-Criteria Filter")
    print("=" * 80)
    
    # Load trees
    trees = load_trees('airline')
    tree = trees['AVL']
    
    # Complex filter: high-rated, recommended, Business Class
    print("\nApplying multi-criteria filter...")
    print("  Criteria:")
    print("    - Rating: 4.5 - 5.0")
    print("    - Recommended: Yes")
    
    filters = {
        'rating': {'min': 4.5, 'max': 5.0},
        'recommended': {'value': True}
    }
    
    results = tree.filter_multi_criteria(filters)
    
    print(f"\nFound {len(results):,} matching records")
    print(f"  Dataset size: {tree.get_size():,} records")
    print(f"  Selectivity: {len(results) / tree.get_size() * 100:.2f}%")
    
    print("\nSample results:")
    for i, record in enumerate(results[:3], 1):
        print(f"  {i}. {record['airline_name'][:35]:35} | "
              f"Rating: {record['overall_rating']:.1f} | "
              f"Recommended: {record.get('recommended', 'N/A')}")


def example_4_benchmark_single_tree():
    """Example 4: Benchmark a single tree."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Benchmark Single Tree")
    print("=" * 80)
    
    # Load trees
    trees = load_trees('airline')
    tree = trees['AVL']
    
    # Create benchmark
    print("\nBenchmarking AVL tree filtering...")
    benchmark = FilterBenchmark(tree, 'AVL', 'airline')
    
    # Benchmark rating filter
    result = benchmark.benchmark_rating_filter(4.0, 5.0, num_runs=10)
    
    # Display results
    time_stats = result['time_complexity']
    space_stats = result['space_complexity']
    
    print(f"\nPerformance Metrics:")
    print(f"  Time Complexity:")
    print(f"    Average: {time_stats['avg_time_ms']:.3f}ms")
    print(f"    Min:     {time_stats['min_time_ms']:.3f}ms")
    print(f"    Max:     {time_stats['max_time_ms']:.3f}ms")
    print(f"    Std Dev: {time_stats['std_dev_ms']:.3f}ms")
    
    print(f"\n  Space Complexity:")
    print(f"    Memory:  {space_stats['memory_allocated_kb']:.2f} KB")
    print(f"    Peak:    {space_stats['peak_memory_kb']:.2f} KB")
    print(f"    Results: {space_stats['result_size_kb']:.2f} KB")
    
    print(f"\n  Results:")
    print(f"    Count:       {time_stats['results_count']:,}")
    print(f"    Selectivity: {result['selectivity_percent']:.2f}%")


def example_5_compare_trees():
    """Example 5: Compare performance across all trees."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Compare All Trees")
    print("=" * 80)
    
    # Load trees
    trees = load_trees('airline')
    
    print("\nComparing rating filter performance across all trees...")
    print("  Filter: Rating 4.5 - 5.0 (high selectivity)")
    print("-" * 80)
    
    # Compare trees
    results = compare_trees(
        trees, 
        'airline',
        lambda b: b.benchmark_rating_filter(4.5, 5.0, num_runs=10)
    )
    
    # Sort by time
    results.sort(key=lambda x: x['time_complexity']['avg_time_ms'])
    
    print("\nPerformance Ranking:")
    print(f"{'Rank':5} | {'Tree':12} | {'Avg Time (ms)':15} | {'Memory (KB)':12} | {'Results':10}")
    print("-" * 80)
    
    for i, result in enumerate(results, 1):
        tree_type = result['tree_type']
        time_ms = result['time_complexity']['avg_time_ms']
        memory_kb = result['space_complexity']['memory_allocated_kb']
        count = result['time_complexity']['results_count']
        
        print(f"{i:5} | {tree_type:12} | {time_ms:15.3f} | {memory_kb:12.2f} | {count:10,}")
    
    # Show winner
    winner = results[0]
    print(f"\nFastest: {winner['tree_type']} at {winner['time_complexity']['avg_time_ms']:.3f}ms")


def example_6_selectivity_impact():
    """Example 6: Demonstrate selectivity impact on performance."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Selectivity Impact")
    print("=" * 80)
    
    # Load trees
    trees = load_trees('airline')
    tree = trees['AVL']
    benchmark = FilterBenchmark(tree, 'AVL', 'airline')
    
    print("\nTesting different selectivity levels...")
    print("-" * 80)
    
    test_ranges = [
        (4.8, 5.0, "Very High Selectivity"),
        (4.5, 5.0, "High Selectivity"),
        (3.0, 4.0, "Medium Selectivity"),
        (1.0, 3.0, "Low Selectivity"),
    ]
    
    print(f"{'Selectivity':25} | {'Range':15} | {'Results':10} | {'Time (ms)':12} | {'%':8}")
    print("-" * 80)
    
    for min_r, max_r, desc in test_ranges:
        result = benchmark.benchmark_rating_filter(min_r, max_r, num_runs=5)
        time_ms = result['time_complexity']['avg_time_ms']
        count = result['time_complexity']['results_count']
        percent = result['selectivity_percent']
        
        print(f"{desc:25} | {min_r:.1f} - {max_r:.1f}    | {count:10,} | {time_ms:12.3f} | {percent:7.2f}%")
    
    print("\nObservation: Higher selectivity (fewer results) = faster execution")


def main():
    """Run all examples."""
    print("=" * 80)
    print("FILTERING EXAMPLES - TREE DATA STRUCTURES")
    print("=" * 80)
    print("\nThis demonstrates filtering functionality across all tree types:")
    print("  - Binary Search Tree (BST)")
    print("  - AVL Tree")
    print("  - Red-Black Tree")
    print("  - Trie")
    
    try:
        # Run examples
        example_1_basic_rating_filter()
        example_2_field_filter()
        example_3_multi_criteria()
        example_4_benchmark_single_tree()
        example_5_compare_trees()
        example_6_selectivity_impact()
        
        print("\n" + "=" * 80)
        print("SUCCESS: ALL EXAMPLES COMPLETED!")
        print("=" * 80)
        
        print("\nNext steps:")
        print("  1. Run full experiments: python experiments/run_experiments.py")
        print("  2. Check results: results/filtering/")
        print("  3. Read docs: FILTERING_QUICK_REFERENCE.md")
        
    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        print("\nPlease build trees first:")
        print("   python src/loaders/load_airline_trees.py")
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

