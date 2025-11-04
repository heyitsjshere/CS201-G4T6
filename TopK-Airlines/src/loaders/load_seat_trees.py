"""
Load seat dataset into various tree data structures.
Each row is stored with overall_rating as the key.
"""

import sys
from pathlib import Path
import time
import random

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

# Increase recursion limit for large datasets
sys.setrecursionlimit(50000)

from utils.data_loader import load_cleaned_data
from utils.tree_persistence import save_trees, load_trees
from data_structures.binary_search_tree import BinarySearchTree
from data_structures.avl_tree import AVLTree
from data_structures.red_black_tree import RedBlackTree
from data_structures.trie import Trie


def load_seat_data_into_trees():
    """
    Load seat dataset into all tree structures.
    
    Returns:
        dict: Dictionary containing all tree structures
    """
    print("=" * 80)
    print("LOADING SEAT DATASET INTO TREE STRUCTURES")
    print("=" * 80)
    
    # Load cleaned seat data
    print("\n📂 Loading seat data...")
    seat_df = load_cleaned_data('seat')
    print(f"✓ Loaded {len(seat_df):,} seat records")
    
    # Initialize all tree structures
    print("\n🌳 Initializing tree structures...")
    bst = BinarySearchTree()
    avl = AVLTree()
    rbt = RedBlackTree()
    trie = Trie()
    
    trees = {
        'BST': bst,
        'AVL': avl,
        'Red-Black': rbt,
        'Trie': trie
    }
    
    # Insert data into each tree
    print("\n⏳ Inserting records into trees...")
    print("-" * 80)
    
    # Convert dataframe to list of tuples
    records = [(row['overall_rating'], row.to_dict()) for _, row in seat_df.iterrows()]
    
    for tree_name, tree in trees.items():
        start_time = time.time()
        
        # Create a copy and shuffle ONLY for BST to prevent unbalanced tree
        if tree_name == 'BST':
            tree_records = records.copy()
            random.shuffle(tree_records)
        else:
            tree_records = records
        
        for rating, data in tree_records:
            tree.insert(rating, data)
        
        elapsed = time.time() - start_time
        
        print(f"{tree_name:12} | Size: {tree.get_size():,} | Height: {tree.get_height():3} | "
              f"Time: {elapsed:.3f}s")
    
    print("-" * 80)
    print(f"✓ All {len(seat_df):,} records inserted into all trees")
    
    return trees, seat_df


def demonstrate_tree_operations(trees, df):
    """
    Demonstrate various operations on the tree structures.
    
    Args:
        trees (dict): Dictionary of tree structures
        df (DataFrame): Original dataframe for comparison
    """
    print("\n" + "=" * 80)
    print("DEMONSTRATING TREE OPERATIONS")
    print("=" * 80)
    
    # Demo 1: Search for specific rating
    print("\n1️⃣  SEARCH: Find all records with rating 4.0")
    print("-" * 80)
    target_rating = 4.0
    
    for tree_name, tree in trees.items():
        start_time = time.time()
        results = tree.search(target_rating)
        elapsed = time.time() - start_time
        
        print(f"{tree_name:12} | Found: {len(results):4} records | Time: {elapsed:.6f}s")
    
    # Demo 2: Get top K highest rated
    print("\n2️⃣  TOP-K: Get top 10 highest rated seats")
    print("-" * 80)
    k = 10
    
    for tree_name, tree in trees.items():
        start_time = time.time()
        top_k = tree.get_top_k(k)
        elapsed = time.time() - start_time
        
        if len(top_k) > 0:
            avg_rating = sum(r['overall_rating'] for r in top_k) / len(top_k)
            print(f"{tree_name:12} | Retrieved: {len(top_k):2} | Avg Rating: {avg_rating:.2f} | "
                  f"Time: {elapsed:.6f}s")
    
    # Show top 3 results
    print("\n   Top 3 seats:")
    top_k = trees['BST'].get_top_k(3)
    for i, record in enumerate(top_k, 1):
        airline = record['airline_name'][:20]
        aircraft = record['aircraft'][:20] if len(record['aircraft']) > 0 else 'N/A'
        print(f"   {i}. {airline:20} | {aircraft:20} | Rating: {record['overall_rating']:.1f}")
    
    # Demo 3: Range search
    print("\n3️⃣  RANGE: Find all records with rating between 4.0 and 5.0")
    print("-" * 80)
    min_rating, max_rating = 4.0, 5.0
    
    for tree_name, tree in trees.items():
        start_time = time.time()
        results = tree.get_range(min_rating, max_rating)
        elapsed = time.time() - start_time
        
        print(f"{tree_name:12} | Found: {len(results):5} records | Time: {elapsed:.6f}s")


def main():
    """Main function to load and demonstrate seat tree structures."""
    try:
        # Load data into trees
        trees, df = load_seat_data_into_trees()
        
        # Demonstrate operations
        demonstrate_tree_operations(trees, df)
        
        # Try to save trees to disk (skip BST if too deep)
        try:
            trees_to_save = {}
            for name, tree in trees.items():
                # Skip BST if height is too large for pickle
                if name == 'BST' and tree.get_height() > 1000:
                    print(f"\n⚠️  Skipping {name} save (height {tree.get_height()} too large for pickle)")
                else:
                    trees_to_save[name] = tree
            
            if trees_to_save:
                save_trees(trees_to_save, 'seat')
        except Exception as save_error:
            print(f"\n⚠️  Warning: Could not save trees to disk: {save_error}")
            print("   Trees are still available in memory for current session.")
        
        print("\n" + "=" * 80)
        print("✅ SEAT DATA SUCCESSFULLY LOADED INTO ALL TREE STRUCTURES!")
        print("=" * 80)
        
        print("\n📋 Summary:")
        print(f"   - Total records: {len(df):,}")
        print(f"   - Tree structures: {len(trees)}")
        print(f"   - Columns: {list(df.columns)}")
        
        print("\n💡 You can now use these trees for:")
        print("   - Fast search by rating")
        print("   - Top-K queries")
        print("   - Range queries")
        print("   - Efficient sorted traversal")
        
        return trees, df
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("\n⚠️  Please run the EDA/explore.ipynb notebook first!")
        return None, None
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    trees, df = main()
