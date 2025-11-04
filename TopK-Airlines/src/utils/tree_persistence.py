"""
Utility to save and load tree structures to/from disk using pickle.
This allows you to build trees once and reuse them without rebuilding.
"""

import pickle
import sys
from pathlib import Path
import time

# Increase recursion limit for pickling large trees
sys.setrecursionlimit(100000)


def save_trees(trees, dataset_name, output_dir='data/trees'):
    """
    Save tree structures to disk.
    
    Args:
        trees (dict): Dictionary of tree structures
        dataset_name (str): Name of the dataset (e.g., 'airline', 'airport')
        output_dir (str): Directory to save the trees
    
    Returns:
        dict: Paths where each tree was saved
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    saved_paths = {}
    
    print(f"\n💾 Saving {dataset_name} trees to disk...")
    print("-" * 80)
    
    for tree_name, tree in trees.items():
        # Create filename
        filename = f"{dataset_name}_{tree_name.lower().replace('-', '_')}_tree.pkl"
        filepath = output_path / filename
        
        # Save using pickle with highest protocol and recursion limit handling
        start_time = time.time()
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(tree, f, protocol=pickle.HIGHEST_PROTOCOL)
        except RecursionError:
            # If still hitting recursion, increase limit temporarily
            old_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(200000)
            try:
                with open(filepath, 'wb') as f:
                    pickle.dump(tree, f, protocol=pickle.HIGHEST_PROTOCOL)
            finally:
                sys.setrecursionlimit(old_limit)
        
        elapsed = time.time() - start_time
        
        # Get file size
        size_mb = filepath.stat().st_size / (1024 * 1024)
        
        print(f"{tree_name:12} | Size: {tree.get_size():,} nodes | "
              f"File: {size_mb:.2f} MB | Time: {elapsed:.3f}s")
        
        saved_paths[tree_name] = str(filepath)
    
    print("-" * 80)
    print(f"✓ All trees saved to: {output_path.absolute()}")
    
    return saved_paths


def load_trees(dataset_name, tree_types=None, input_dir='data/trees'):
    """
    Load tree structures from disk.
    
    Args:
        dataset_name (str): Name of the dataset (e.g., 'airline', 'airport')
        tree_types (list): List of tree types to load (e.g., ['BST', 'AVL'])
                          If None, loads all available trees
        input_dir (str): Directory where trees are saved
    
    Returns:
        dict: Dictionary of loaded tree structures
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        raise FileNotFoundError(
            f"Trees directory not found at {input_path.absolute()}.\n"
            "Please run a loader script first and save the trees."
        )
    
    # Determine which trees to load
    tree_name_map = {
        'BST': f"{dataset_name}_bst_tree.pkl",
        'AVL': f"{dataset_name}_avl_tree.pkl",
        'Red-Black': f"{dataset_name}_red_black_tree.pkl",
        'Trie': f"{dataset_name}_trie_tree.pkl"
    }
    
    if tree_types is None:
        tree_types = list(tree_name_map.keys())
    
    trees = {}
    
    print(f"\n📂 Loading {dataset_name} trees from disk...")
    print("-" * 80)
    
    for tree_type in tree_types:
        if tree_type not in tree_name_map:
            print(f"⚠️  Unknown tree type: {tree_type}")
            continue
        
        filename = tree_name_map[tree_type]
        filepath = input_path / filename
        
        if not filepath.exists():
            print(f"⚠️  {tree_type:12} | File not found: {filename}")
            continue
        
        # Load using pickle
        start_time = time.time()
        with open(filepath, 'rb') as f:
            tree = pickle.load(f)
        elapsed = time.time() - start_time
        
        # Get file size
        size_mb = filepath.stat().st_size / (1024 * 1024)
        
        print(f"✓ {tree_type:12} | Size: {tree.get_size():,} nodes | "
              f"File: {size_mb:.2f} MB | Time: {elapsed:.3f}s")
        
        trees[tree_type] = tree
    
    print("-" * 80)
    print(f"✓ Loaded {len(trees)} tree(s) for {dataset_name}")
    
    return trees


def list_saved_trees(input_dir='data/trees'):
    """
    List all saved trees in the directory.
    
    Args:
        input_dir (str): Directory where trees are saved
    
    Returns:
        dict: Dictionary of available datasets and their trees
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"⚠️  Trees directory not found at {input_path.absolute()}")
        return {}
    
    # Find all pickle files
    tree_files = list(input_path.glob('*_tree.pkl'))
    
    if not tree_files:
        print(f"⚠️  No saved trees found in {input_path.absolute()}")
        return {}
    
    # Group by dataset
    datasets = {}
    for filepath in tree_files:
        # Parse filename: dataset_treetype_tree.pkl
        parts = filepath.stem.split('_')
        if len(parts) >= 2:
            dataset = parts[0]
            tree_type = '_'.join(parts[1:-1])  # Everything between dataset and 'tree'
            
            if dataset not in datasets:
                datasets[dataset] = []
            
            size_mb = filepath.stat().st_size / (1024 * 1024)
            datasets[dataset].append({
                'type': tree_type,
                'file': filepath.name,
                'size_mb': size_mb
            })
    
    # Print summary
    print("\n" + "=" * 80)
    print("SAVED TREES INVENTORY")
    print("=" * 80)
    
    for dataset, trees in datasets.items():
        print(f"\n📊 Dataset: {dataset}")
        print("-" * 80)
        for tree_info in trees:
            print(f"   {tree_info['type']:20} | {tree_info['file']:40} | {tree_info['size_mb']:.2f} MB")
    
    print("\n" + "=" * 80)
    print(f"Total: {len(datasets)} dataset(s), {sum(len(t) for t in datasets.values())} tree(s)")
    print("=" * 80)
    
    return datasets


if __name__ == "__main__":
    # List all saved trees
    list_saved_trees()
