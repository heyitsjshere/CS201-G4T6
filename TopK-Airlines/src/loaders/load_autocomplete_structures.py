"""
Load datasets into autocomplete data structures (Trie, Ternary Search Tree).
"""

import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from utils.data_loader import load_cleaned_data
from utils.tree_persistence import save_trees, load_trees
from data_structures.string_trie import StringTrie
from data_structures.ternary_search_tree import TernarySearchTree
from data_structures.sorted_array import SortedArray


def get_name_field(dataset_name):
    """Get the name field for a dataset."""
    field_map = {
        'airline': 'airline_name',
        'airport': 'airport_name',
        'lounge': 'lounge_name',
        'seat': 'airline_name'  # Seats use airline_name as identifier
    }
    return field_map.get(dataset_name, 'name')


def load_autocomplete_structures(dataset_name='airline'):
    """
    Load dataset into autocomplete data structures.
    
    Args:
        dataset_name: Name of dataset ('airline', 'airport', 'lounge', 'seat')
    
    Returns:
        dict: Dictionary containing autocomplete structures
    """
    print("=" * 80)
    print(f"LOADING {dataset_name.upper()} DATASET INTO AUTOCOMPLETE STRUCTURES")
    print("=" * 80)
    
    # Load cleaned data
    print(f"\nLoading {dataset_name} data...")
    df = load_cleaned_data(dataset_name)
    print(f"Loaded {len(df):,} records")
    
    # Get name field
    name_field = get_name_field(dataset_name)
    
    # Initialize structures
    print("\nInitializing autocomplete structures...")
    trie = StringTrie()
    tst = TernarySearchTree()
    sorted_arr = SortedArray()
    
    structures = {
        'Trie': trie,
        'TernarySearchTree': tst,
        'SortedArray': sorted_arr
    }
    
    # Insert data
    print("\nInserting records into structures...")
    print("-" * 80)
    
    for tree_name, tree in structures.items():
        start_time = time.time()
        comparisons_before = tree.get_total_comparisons()
        
        for _, row in df.iterrows():
            name = row.get(name_field, '')
            if name:
                tree.insert(name, row.to_dict())
        
        elapsed = time.time() - start_time
        comparisons = tree.get_total_comparisons() - comparisons_before
        
        print(f"{tree_name:20} | Size: {tree.get_size():,} | Height: {tree.get_height():3} | "
              f"Time: {elapsed:.3f}s | Comparisons: {comparisons:,}")
    
    print("-" * 80)
    print(f"All {len(df):,} records inserted into autocomplete structures")
    
    return structures, df


def save_autocomplete_structures(structures, dataset_name):
    """Save autocomplete structures to disk."""
    try:
        # Create a save structure compatible with existing save_trees function
        # We'll save them with a different naming convention
        save_trees(structures, f"{dataset_name}_autocomplete")
        print(f"\nSaved autocomplete structures for {dataset_name}")
    except Exception as e:
        print(f"\nWARNING: Could not save structures: {e}")


def main():
    """Main function to load autocomplete structures for all datasets."""
    datasets = ['airline', 'airport', 'lounge', 'seat']
    
    all_structures = {}
    
    for dataset_name in datasets:
        try:
            structures, df = load_autocomplete_structures(dataset_name)
            all_structures[dataset_name] = structures
            save_autocomplete_structures(structures, dataset_name)
        except Exception as e:
            print(f"\nERROR: Error loading {dataset_name}: {e}")
    
    print("\n" + "=" * 80)
    print("SUCCESS: AUTOCOMPLETE STRUCTURES LOADED!")
    print("=" * 80)
    
    return all_structures


if __name__ == "__main__":
    structures = main()

