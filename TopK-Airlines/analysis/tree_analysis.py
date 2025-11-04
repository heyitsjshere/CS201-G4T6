"""
Comprehensive analysis of tree data structures across all datasets.
Analyzes performance, characteristics, and behaviors of different tree types.
"""

import sys
from pathlib import Path
import time
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.tree_persistence import load_trees, list_saved_trees
from utils.data_loader import load_cleaned_data


def get_tree_metadata(tree, tree_type):
    """Extract metadata about a tree structure."""
    metadata = {
        'type': tree_type,
        'height': tree.get_height() if hasattr(tree, 'get_height') else 'N/A'
    }
    
    # Count nodes (if possible)
    try:
        if hasattr(tree, 'root'):
            node_count = count_nodes(tree.root)
            metadata['node_count'] = node_count
    except:
        metadata['node_count'] = 'N/A'
    
    return metadata


def count_nodes(node):
    """Recursively count nodes in a tree."""
    if node is None:
        return 0
    
    count = 1
    if hasattr(node, 'left') and hasattr(node, 'right'):
        count += count_nodes(node.left)
        count += count_nodes(node.right)
    elif hasattr(node, 'children'):
        for child in node.children.values():
            count += count_nodes(child)
    
    return count


def benchmark_search_operations(tree, tree_type, dataset_name, test_ratings):
    """Benchmark search operations on a tree."""
    results = []
    
    for rating in test_ratings:
        start = time.perf_counter()
        found = tree.search(rating)
        elapsed = time.perf_counter() - start
        
        results.append({
            'rating': rating,
            'found': found is not None,
            'time_ms': elapsed * 1000,
            'num_results': len(found) if found else 0
        })
    
    avg_time = sum(r['time_ms'] for r in results) / len(results)
    
    return {
        'tree_type': tree_type,
        'dataset': dataset_name,
        'operation': 'search',
        'num_tests': len(test_ratings),
        'avg_time_ms': avg_time,
        'min_time_ms': min(r['time_ms'] for r in results),
        'max_time_ms': max(r['time_ms'] for r in results),
        'details': results
    }


def benchmark_topk_operations(tree, tree_type, dataset_name, k_values=[10, 50, 100]):
    """Benchmark top-K operations on a tree."""
    results = []
    
    for k in k_values:
        start = time.perf_counter()
        top_k = tree.get_top_k(k)
        elapsed = time.perf_counter() - start
        
        results.append({
            'k': k,
            'time_ms': elapsed * 1000,
            'results_returned': len(top_k)
        })
    
    avg_time = sum(r['time_ms'] for r in results) / len(results)
    
    return {
        'tree_type': tree_type,
        'dataset': dataset_name,
        'operation': 'top_k',
        'num_tests': len(k_values),
        'avg_time_ms': avg_time,
        'details': results
    }


def benchmark_range_operations(tree, tree_type, dataset_name, ranges):
    """Benchmark range query operations on a tree."""
    results = []
    
    for min_rating, max_rating in ranges:
        start = time.perf_counter()
        range_results = tree.get_range(min_rating, max_rating)
        elapsed = time.perf_counter() - start
        
        results.append({
            'range': f"{min_rating}-{max_rating}",
            'time_ms': elapsed * 1000,
            'results_returned': len(range_results)
        })
    
    avg_time = sum(r['time_ms'] for r in results) / len(results)
    
    return {
        'tree_type': tree_type,
        'dataset': dataset_name,
        'operation': 'range_query',
        'num_tests': len(ranges),
        'avg_time_ms': avg_time,
        'details': results
    }


def analyze_dataset_trees(dataset_name, df):
    """Analyze all tree structures for a dataset."""
    print(f"\n{'=' * 80}")
    print(f"Analyzing {dataset_name.upper()} dataset")
    print(f"{'=' * 80}")
    print(f"Dataset size: {len(df):,} records")
    
    # Load all available trees for this dataset
    try:
        trees = load_trees(dataset_name)
        print(f"Loaded {len(trees)} tree structures: {list(trees.keys())}")
    except Exception as e:
        print(f"❌ Error loading trees: {e}")
        return None
    
    analysis_results = {
        'dataset': dataset_name,
        'dataset_size': len(df),
        'trees_analyzed': list(trees.keys()),
        'timestamp': datetime.now().isoformat(),
        'tree_metadata': {},
        'performance_benchmarks': {
            'search': [],
            'top_k': [],
            'range_query': []
        }
    }
    
    # Get sample ratings for testing
    sample_ratings = df['overall_rating'].sample(min(10, len(df))).tolist()
    
    # Define test ranges based on dataset statistics
    min_rating = df['overall_rating'].min()
    max_rating = df['overall_rating'].max()
    mid_rating = (min_rating + max_rating) / 2
    
    test_ranges = [
        (min_rating, mid_rating),
        (mid_rating, max_rating),
        (min_rating, max_rating),
        (7.0, 10.0),  # High ratings
        (1.0, 5.0)    # Low ratings
    ]
    
    # Analyze each tree
    for tree_name, tree in trees.items():
        print(f"\n--- {tree_name} Tree ---")
        
        # 1. Get metadata
        metadata = get_tree_metadata(tree, tree_name)
        analysis_results['tree_metadata'][tree_name] = metadata
        print(f"Height: {metadata['height']}")
        print(f"Nodes: {metadata.get('node_count', 'N/A')}")
        
        # 2. Benchmark search
        print("  Benchmarking search operations...")
        search_results = benchmark_search_operations(tree, tree_name, dataset_name, sample_ratings)
        analysis_results['performance_benchmarks']['search'].append(search_results)
        print(f"    Avg search time: {search_results['avg_time_ms']:.6f} ms")
        
        # 3. Benchmark top-K
        print("  Benchmarking top-K operations...")
        topk_results = benchmark_topk_operations(tree, tree_name, dataset_name)
        analysis_results['performance_benchmarks']['top_k'].append(topk_results)
        print(f"    Avg top-K time: {topk_results['avg_time_ms']:.6f} ms")
        
        # 4. Benchmark range queries
        print("  Benchmarking range queries...")
        range_results = benchmark_range_operations(tree, tree_name, dataset_name, test_ranges)
        analysis_results['performance_benchmarks']['range_query'].append(range_results)
        print(f"    Avg range query time: {range_results['avg_time_ms']:.6f} ms")
    
    return analysis_results


def generate_summary_report(all_results):
    """Generate a summary comparison across all datasets and trees."""
    print(f"\n{'=' * 80}")
    print("SUMMARY REPORT")
    print(f"{'=' * 80}")
    
    summary = {
        'total_datasets': len(all_results),
        'analysis_timestamp': datetime.now().isoformat(),
        'dataset_summaries': {},
        'tree_comparisons': {},
        'key_findings': []
    }
    
    # Summarize each dataset
    for result in all_results:
        dataset = result['dataset']
        summary['dataset_summaries'][dataset] = {
            'size': result['dataset_size'],
            'trees_available': result['trees_analyzed'],
            'tree_heights': {name: meta['height'] for name, meta in result['tree_metadata'].items()}
        }
    
    # Compare tree performance across datasets
    all_tree_types = set()
    for result in all_results:
        all_tree_types.update(result['trees_analyzed'])
    
    for tree_type in all_tree_types:
        summary['tree_comparisons'][tree_type] = {
            'datasets': [],
            'avg_search_time': [],
            'avg_topk_time': [],
            'avg_range_time': []
        }
        
        for result in all_results:
            if tree_type in result['trees_analyzed']:
                dataset = result['dataset']
                summary['tree_comparisons'][tree_type]['datasets'].append(dataset)
                
                # Get average times
                search_times = [b for b in result['performance_benchmarks']['search'] if b['tree_type'] == tree_type]
                topk_times = [b for b in result['performance_benchmarks']['top_k'] if b['tree_type'] == tree_type]
                range_times = [b for b in result['performance_benchmarks']['range_query'] if b['tree_type'] == tree_type]
                
                if search_times:
                    summary['tree_comparisons'][tree_type]['avg_search_time'].append(search_times[0]['avg_time_ms'])
                if topk_times:
                    summary['tree_comparisons'][tree_type]['avg_topk_time'].append(topk_times[0]['avg_time_ms'])
                if range_times:
                    summary['tree_comparisons'][tree_type]['avg_range_time'].append(range_times[0]['avg_time_ms'])
    
    # Generate key findings
    print("\n📊 KEY FINDINGS:")
    
    # Find fastest tree for each operation
    for op_type in ['search', 'top_k', 'range_query']:
        op_name = op_type.replace('_', ' ').title()
        fastest_tree = None
        fastest_time = float('inf')
        
        for tree_type in all_tree_types:
            if tree_type in summary['tree_comparisons']:
                times_key = f"avg_{op_type}_time" if op_type != 'top_k' else 'avg_topk_time'
                times = summary['tree_comparisons'][tree_type].get(times_key, [])
                if times:
                    avg = sum(times) / len(times)
                    if avg < fastest_time:
                        fastest_time = avg
                        fastest_tree = tree_type
        
        if fastest_tree:
            finding = f"Fastest for {op_name}: {fastest_tree} ({fastest_time:.6f} ms avg)"
            summary['key_findings'].append(finding)
            print(f"  • {finding}")
    
    # Tree height comparison
    print("\n📏 TREE HEIGHTS:")
    for dataset, info in summary['dataset_summaries'].items():
        print(f"  {dataset.upper()}:")
        for tree_name, height in info['tree_heights'].items():
            print(f"    {tree_name:15} - Height: {height}")
    
    return summary


def save_results(all_results, summary, output_dir):
    """Save analysis results to JSON files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    detailed_file = output_path / f"tree_analysis_detailed_{timestamp}.json"
    with open(detailed_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\n💾 Detailed results saved to: {detailed_file}")
    
    # Save summary
    summary_file = output_path / f"tree_analysis_summary_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"💾 Summary saved to: {summary_file}")
    
    # Save human-readable report
    report_file = output_path / f"tree_analysis_report_{timestamp}.txt"
    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("TREE DATA STRUCTURES ANALYSIS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Dataset summaries
        f.write("DATASET SUMMARIES\n")
        f.write("-" * 80 + "\n")
        for result in all_results:
            f.write(f"\n{result['dataset'].upper()} Dataset:\n")
            f.write(f"  Size: {result['dataset_size']:,} records\n")
            f.write(f"  Trees: {', '.join(result['trees_analyzed'])}\n")
            f.write(f"  Tree Heights:\n")
            for name, meta in result['tree_metadata'].items():
                f.write(f"    {name:15} - {meta['height']}\n")
        
        # Performance comparison
        f.write("\n\nPERFORMANCE COMPARISON\n")
        f.write("-" * 80 + "\n")
        for tree_type in summary['tree_comparisons']:
            f.write(f"\n{tree_type} Tree:\n")
            comp = summary['tree_comparisons'][tree_type]
            f.write(f"  Datasets: {', '.join(comp['datasets'])}\n")
            if comp['avg_search_time']:
                avg = sum(comp['avg_search_time']) / len(comp['avg_search_time'])
                f.write(f"  Avg Search Time: {avg:.6f} ms\n")
            if comp['avg_topk_time']:
                avg = sum(comp['avg_topk_time']) / len(comp['avg_topk_time'])
                f.write(f"  Avg Top-K Time: {avg:.6f} ms\n")
            if comp['avg_range_time']:
                avg = sum(comp['avg_range_time']) / len(comp['avg_range_time'])
                f.write(f"  Avg Range Query Time: {avg:.6f} ms\n")
        
        # Key findings
        f.write("\n\nKEY FINDINGS\n")
        f.write("-" * 80 + "\n")
        for finding in summary['key_findings']:
            f.write(f"• {finding}\n")
    
    print(f"💾 Human-readable report saved to: {report_file}")


def main():
    """Main analysis function."""
    print("=" * 80)
    print("TREE DATA STRUCTURES COMPREHENSIVE ANALYSIS")
    print("=" * 80)
    
    # List all available trees
    print("\n📋 Available saved trees:")
    available_trees = list_saved_trees()
    
    # Datasets to analyze
    datasets = ['airline', 'airport', 'lounge', 'seat']
    
    # Load cleaned data for each dataset
    print("\n📂 Loading cleaned datasets...")
    all_data = load_cleaned_data()
    
    # Run analysis on each dataset
    all_results = []
    for dataset_name in datasets:
        if dataset_name in all_data:
            df = all_data[dataset_name]
            result = analyze_dataset_trees(dataset_name, df)
            if result:
                all_results.append(result)
        else:
            print(f"⚠️  Warning: {dataset_name} data not found")
    
    # Generate summary report
    if all_results:
        summary = generate_summary_report(all_results)
        
        # Save all results
        output_dir = Path(__file__).parent.parent / 'results'
        save_results(all_results, summary, output_dir)
        
        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETE!")
        print("=" * 80)
    else:
        print("\n❌ No results to analyze")


if __name__ == "__main__":
    main()
