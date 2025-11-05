"""
Example: How to use saved tree structures without rebuilding them.

This script shows you how to:
1. Load pre-built trees from disk
2. Perform queries on them
3. Use them in your analysis
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.tree_persistence import load_trees, list_saved_trees


def example_1_list_available_trees():
    """Show what trees are available on disk."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: List Available Saved Trees")
    print("=" * 80)
    
    available = list_saved_trees()
    return available


def example_2_load_specific_trees():
    """Load specific tree types for a dataset."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Load Specific Trees")
    print("=" * 80)
    
    # Load only BST and AVL trees for airline dataset
    trees = load_trees('airline', tree_types=['BST', 'AVL'])
    
    print("\n Using loaded trees:")
    for tree_name, tree in trees.items():
        print(f"   {tree_name}: {tree.get_size():,} nodes, height {tree.get_height()}")
    
    return trees


def example_3_load_all_trees():
    """Load all available trees for a dataset."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Load All Trees for Airline Dataset")
    print("=" * 80)
    
    # Load all trees for airline dataset
    trees = load_trees('airline')
    
    print("\n All trees loaded:")
    for tree_name, tree in trees.items():
        print(f"   {tree_name}: {tree.get_size():,} nodes, height {tree.get_height()}")
    
    return trees


def example_4_perform_queries(trees):
    """Perform queries on loaded trees."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Perform Queries on Loaded Trees")
    print("=" * 80)
    
    if not trees:
        print("  No trees loaded. Run example_3_load_all_trees() first.")
        return
    
    # Use any tree (they all have the same data)
    tree = trees['AVL']
    
    # Query 1: Get top 5 airlines
    print("\n Query 1: Top 5 highest rated airlines")
    print("-" * 80)
    top_5 = tree.get_top_k(5)
    for i, record in enumerate(top_5, 1):
        print(f"   {i}. {record['airline_name'][:40]:40} | Rating: {record['overall_rating']:.1f}")
    
    # Query 2: Search for specific rating
    print("\n Query 2: Find all records with rating 5.0")
    print("-" * 80)
    results = tree.search(5.0)
    print(f"   Found {len(results)} records with perfect rating!")
    if results:
        print(f"   Examples: {', '.join([r['airline_name'][:20] for r in results[:3]])}")
    
    # Query 3: Range query
    print("\n Query 3: Find all records with rating between 4.5 and 5.0")
    print("-" * 80)
    high_rated = tree.get_range(4.5, 5.0)
    print(f"   Found {len(high_rated)} highly rated records")
    
    # Query 4: Count by rating
    print("\n Query 4: Distribution of ratings")
    print("-" * 80)
    all_records = tree.get_range(0, 10)
    rating_counts = {}
    for record in all_records:
        rating = record['overall_rating']
        rating_counts[rating] = rating_counts.get(rating, 0) + 1
    
    # Show top 5 most common ratings
    sorted_ratings = sorted(rating_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for rating, count in sorted_ratings:
        print(f"   Rating {rating:.1f}: {count:,} records")


def example_5_compare_tree_performance(trees):
    """Compare query performance across different tree types."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Compare Tree Performance")
    print("=" * 80)
    
    if not trees:
        print("  No trees loaded.")
        return
    
    import time
    
    print("\n  Top-K query performance (k=100):")
    print("-" * 80)
    for tree_name, tree in trees.items():
        start = time.time()
        results = tree.get_top_k(100)
        elapsed = time.time() - start
        print(f"   {tree_name:12} | Time: {elapsed*1000:.3f}ms | Results: {len(results)}")
    
    print("\n  Range query performance (4.0 to 5.0):")
    print("-" * 80)
    for tree_name, tree in trees.items():
        start = time.time()
        results = tree.get_range(4.0, 5.0)
        elapsed = time.time() - start
        print(f"   {tree_name:12} | Time: {elapsed*1000:.3f}ms | Results: {len(results)}")


def main():
    """Run all examples."""
    print("=" * 80)
    print("USING SAVED TREE STRUCTURES - EXAMPLES")
    print("=" * 80)
    print("\nThis demonstrates how to load and use pre-built trees")
    print("without rebuilding them every time.\n")
    
    try:
        # Example 1: List available trees
        available = example_1_list_available_trees()
        
        if not available:
            print("\n  No saved trees found!")
            print("\n To create trees, run one of these:")
            print("   python src\\loaders\\load_airline_trees.py")
            print("   python src\\loaders\\load_airport_trees.py")
            print("   python src\\loaders\\load_lounge_trees.py")
            print("   python src\\loaders\\load_seat_trees.py")
            return
        
        # Example 2: Load specific trees
        specific_trees = example_2_load_specific_trees()
        
        # Example 3: Load all trees
        all_trees = example_3_load_all_trees()
        
        # Example 4: Perform queries
        example_4_perform_queries(all_trees)
        
        # Example 5: Compare performance
        example_5_compare_tree_performance(all_trees)
        
        print("\n" + "=" * 80)
        print(" ALL EXAMPLES COMPLETED!")
        print("=" * 80)
        
        print("\n Now you can use these patterns in your own code:")
        print("""
        from src.utils.tree_persistence import load_trees
        
        # Load trees
        trees = load_trees('airline')
        
        # Use them
        bst = trees['BST']
        top_airlines = bst.get_top_k(10)
        
        # Do your analysis!
        """)
        
    except FileNotFoundError as e:
        print(f"\n ERROR: {e}")
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
