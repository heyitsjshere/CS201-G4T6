"""
Simple benchmark runner without Unicode issues
"""
import sys
import os
import pickle
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from utils.filter_benchmarks import FilterBenchmark
import pandas as pd

print("=" * 70)
print("FILTERING BENCHMARK - SIMPLIFIED")
print("=" * 70)

# Load trees directly
print("\n1. Loading trees from files...")
tree_dir = Path("data/trees")
trees = {}

tree_files = {
    'BST': 'airline_bst_tree.pkl',
    'AVL': 'airline_avl_tree.pkl',
    'Red-Black': 'airline_red_black_tree.pkl',
    'Trie': 'airline_trie_tree.pkl'
}

for name, filename in tree_files.items():
    filepath = tree_dir / filename
    if filepath.exists():
        try:
            with open(filepath, 'rb') as f:
                trees[name] = pickle.load(f)
            print(f"   [OK] Loaded {name}: {trees[name].get_size():,} records")
        except Exception as e:
            print(f"   [SKIP] {name}: {e}")
    else:
        print(f"   [SKIP] {name}: File not found")

if not trees:
    print("\n[ERROR] No trees loaded!")
    sys.exit(1)

print(f"\n   Total: {len(trees)} trees loaded")

# Run benchmarks
print("\n2. Running benchmarks...")
print("=" * 70)

results = []

test_cases = [
    (4.8, 5.0, "Very High Selectivity"),
    (4.5, 5.0, "High Selectivity"),
    (4.0, 5.0, "Medium Selectivity"),
    (3.0, 5.0, "Low Selectivity"),
]

for min_rating, max_rating, desc in test_cases:
    print(f"\nTest: {desc} (Rating {min_rating}-{max_rating})")
    print("-" * 70)
    
    for tree_name, tree in trees.items():
        try:
            benchmark = FilterBenchmark(tree, tree_name, 'airline')
            result = benchmark.benchmark_rating_filter(min_rating, max_rating, num_runs=5)
            
            avg_time = result['time_complexity']['avg_time_ms']
            memory = result['space_complexity']['memory_allocated_kb']
            count = result['time_complexity']['results_count']
            selectivity = result['selectivity_percent']
            
            print(f"   {tree_name:12} | Time: {avg_time:7.3f}ms | Memory: {memory:7.2f}KB | Results: {count:6,} ({selectivity:5.2f}%)")
            
            results.append({
                'tree': tree_name,
                'selectivity_level': desc,
                'min_rating': min_rating,
                'max_rating': max_rating,
                'avg_time_ms': avg_time,
                'memory_kb': memory,
                'results': count,
                'selectivity_pct': selectivity
            })
            
        except Exception as e:
            print(f"   {tree_name:12} | [ERROR] {e}")

# Save results
print("\n3. Saving results...")
output_dir = Path("results/filtering/airline")
output_dir.mkdir(exist_ok=True, parents=True)

df = pd.DataFrame(results)
csv_file = output_dir / "benchmark_results.csv"
df.to_csv(csv_file, index=False)
print(f"   [OK] Saved to {csv_file}")

# Print summary
print("\n4. Performance Summary")
print("=" * 70)

for level in df['selectivity_level'].unique():
    level_df = df[df['selectivity_level'] == level]
    print(f"\n{level}:")
    level_df_sorted = level_df.sort_values('avg_time_ms')
    
    for _, row in level_df_sorted.iterrows():
        print(f"   {row['tree']:12} - {row['avg_time_ms']:6.2f}ms")
    
    fastest = level_df_sorted.iloc[0]
    slowest = level_df_sorted.iloc[-1]
    speedup = slowest['avg_time_ms'] / fastest['avg_time_ms']
    print(f"   Speedup: {fastest['tree']} is {speedup:.1f}x faster than {slowest['tree']}")

print("\n" + "=" * 70)
print("BENCHMARK COMPLETE!")
print("=" * 70)
print(f"\nResults saved to: {csv_file}")
print("You can open this file in Excel to analyze the data.")

