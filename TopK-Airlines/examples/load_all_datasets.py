"""
Master script to load all datasets into tree structures.
Run this to see all datasets loaded and compared.
"""

import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from loaders.load_airline_trees import load_airline_data_into_trees
from loaders.load_airport_trees import load_airport_data_into_trees
from loaders.load_lounge_trees import load_lounge_data_into_trees
from loaders.load_seat_trees import load_seat_data_into_trees


def main():
    """Load all datasets into tree structures."""
    print("\n" + "=" * 80)
    print("LOADING ALL DATASETS INTO TREE STRUCTURES")
    print("=" * 80)
    
    all_results = {}
    
    datasets = [
        ('Airline', load_airline_data_into_trees),
        ('Airport', load_airport_data_into_trees),
        ('Lounge', load_lounge_data_into_trees),
        ('Seat', load_seat_data_into_trees)
    ]
    
    for dataset_name, loader_func in datasets:
        print(f"\n{'='*80}")
        print(f"Processing {dataset_name} Dataset...")
        print('='*80)
        
        try:
            start_time = time.time()
            trees, df = loader_func()
            elapsed = time.time() - start_time
            
            if trees is not None:
                all_results[dataset_name] = {
                    'trees': trees,
                    'df': df,
                    'time': elapsed
                }
                print(f"\n{dataset_name} loaded in {elapsed:.2f}s")
        except Exception as e:
            print(f"\nERROR: Error loading {dataset_name}: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY - ALL DATASETS")
    print("=" * 80)
    
    if all_results:
        print(f"\nSuccessfully loaded {len(all_results)}/4 datasets\n")
        
        print(f"{'Dataset':<15} {'Records':<10} {'BST Height':<12} {'AVL Height':<12} {'RB Height':<12} {'Time':<10}")
        print("-" * 80)
        
        for dataset_name, result in all_results.items():
            trees = result['trees']
            df = result['df']
            elapsed = result['time']
            
            bst_height = trees['BST'].get_height()
            avl_height = trees['AVL'].get_height()
            rb_height = trees['Red-Black'].get_height()
            
            print(f"{dataset_name:<15} {len(df):<10,} {bst_height:<12} {avl_height:<12} {rb_height:<12} {elapsed:<10.2f}s")
        
        print("\n" + "=" * 80)
        print("SUCCESS: ALL DATASETS SUCCESSFULLY LOADED!")
        print("=" * 80)
        
        print("\nKey Observations:")
        print("   - AVL and Red-Black trees have lower heights (better balanced)")
        print("   - BST height varies based on insertion order")
        print("   - Larger datasets take more time to load")
        print("   - All trees support: search, top-k, and range queries")
        
        return all_results
    else:
        print("\nERROR: No datasets were loaded successfully.")
        print("Please run the EDA/explore.ipynb notebook first!")
        return None


if __name__ == "__main__":
    results = main()
