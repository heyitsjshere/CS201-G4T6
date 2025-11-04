"""
Filtering Experiments Runner

This script runs comprehensive filtering experiments across all data structures
and datasets, measuring time and space complexity.
"""

import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.tree_persistence import load_trees, list_saved_trees
from utils.filter_benchmarks import (
    FilterBenchmark,
    compare_trees,
    run_comprehensive_benchmark,
    print_comparison_summary
)


def save_results_to_csv(results: dict, output_dir: Path):
    """
    Save benchmark results to CSV files.
    
    Args:
        results: Dictionary of benchmark results
        output_dir: Directory to save results
    """
    output_dir.mkdir(exist_ok=True, parents=True)
    
    all_rows = []
    
    for test_type, test_results in results.items():
        for result in test_results:
            row = {
                'test_type': test_type,
                'tree_type': result['tree_type'],
                'dataset': result['dataset'],
                'dataset_size': result['dataset_size'],
                'operation': result['operation'],
                'filter_params': str(result['filter_params']),
                
                # Time metrics
                'avg_time_ms': result['time_complexity']['avg_time_ms'],
                'min_time_ms': result['time_complexity']['min_time_ms'],
                'max_time_ms': result['time_complexity']['max_time_ms'],
                'std_dev_ms': result['time_complexity']['std_dev_ms'],
                
                # Space metrics
                'memory_kb': result['space_complexity']['memory_allocated_kb'],
                'memory_mb': result['space_complexity']['memory_allocated_mb'],
                'peak_memory_kb': result['space_complexity']['peak_memory_kb'],
                'result_size_kb': result['space_complexity']['result_size_kb'],
                
                # Results metrics
                'results_count': result['time_complexity']['results_count'],
                'selectivity': result['selectivity'],
                'selectivity_percent': result['selectivity_percent']
            }
            all_rows.append(row)
    
    # Create DataFrame and save
    df = pd.DataFrame(all_rows)
    csv_path = output_dir / 'filtering_benchmark_results.csv'
    df.to_csv(csv_path, index=False)
    
    print(f"\n💾 Results saved to: {csv_path}")
    
    return df


def save_results_to_json(results: dict, output_dir: Path):
    """
    Save detailed benchmark results to JSON.
    
    Args:
        results: Dictionary of benchmark results
        output_dir: Directory to save results
    """
    output_dir.mkdir(exist_ok=True, parents=True)
    
    json_path = output_dir / 'filtering_benchmark_detailed.json'
    
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Detailed results saved to: {json_path}")


def generate_report(df: pd.DataFrame, output_dir: Path):
    """
    Generate a human-readable report from benchmark results.
    
    Args:
        df: DataFrame with benchmark results
        output_dir: Directory to save report
    """
    report_path = output_dir / 'filtering_benchmark_report.txt'
    
    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("FILTERING BENCHMARK REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Summary statistics
        f.write("SUMMARY STATISTICS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Tests Run: {len(df)}\n")
        f.write(f"Data Structures: {', '.join(df['tree_type'].unique())}\n")
        f.write(f"Datasets: {', '.join(df['dataset'].unique())}\n\n")
        
        # Performance by tree type
        f.write("\nPERFORMANCE BY TREE TYPE\n")
        f.write("-" * 80 + "\n")
        
        for tree_type in df['tree_type'].unique():
            tree_df = df[df['tree_type'] == tree_type]
            avg_time = tree_df['avg_time_ms'].mean()
            avg_memory = tree_df['memory_kb'].mean()
            
            f.write(f"\n{tree_type}:\n")
            f.write(f"  Average Time: {avg_time:.3f}ms\n")
            f.write(f"  Average Memory: {avg_memory:.2f}KB\n")
            f.write(f"  Tests Run: {len(tree_df)}\n")
        
        # Best performers by operation
        f.write("\n\nBEST PERFORMERS BY OPERATION\n")
        f.write("-" * 80 + "\n")
        
        for operation in df['operation'].unique():
            op_df = df[df['operation'] == operation]
            fastest = op_df.loc[op_df['avg_time_ms'].idxmin()]
            
            f.write(f"\n{operation}:\n")
            f.write(f"  Fastest: {fastest['tree_type']} ({fastest['avg_time_ms']:.3f}ms)\n")
            f.write(f"  Least Memory: {op_df.loc[op_df['memory_kb'].idxmin()]['tree_type']}\n")
        
        # Detailed results by test type
        f.write("\n\nDETAILED RESULTS BY TEST TYPE\n")
        f.write("=" * 80 + "\n")
        
        for test_type in df['test_type'].unique():
            f.write(f"\n{test_type.replace('_', ' ').title()}\n")
            f.write("-" * 80 + "\n\n")
            
            test_df = df[df['test_type'] == test_type]
            
            # Group by filter params
            for params in test_df['filter_params'].unique():
                param_df = test_df[test_df['filter_params'] == params]
                
                f.write(f"\nFilter: {params}\n")
                f.write(f"{'Tree':12} | {'Time (ms)':>12} | {'Memory (KB)':>12} | {'Results':>10} | {'Selectivity':>12}\n")
                f.write("-" * 80 + "\n")
                
                for _, row in param_df.iterrows():
                    f.write(f"{row['tree_type']:12} | {row['avg_time_ms']:12.3f} | "
                           f"{row['memory_kb']:12.2f} | {row['results_count']:10,} | "
                           f"{row['selectivity_percent']:11.2f}%\n")
                
                f.write("\n")
    
    print(f"📄 Report saved to: {report_path}")


def run_dataset_experiments(dataset_name: str, output_dir: Path):
    """
    Run experiments for a specific dataset.
    
    Args:
        dataset_name: Name of dataset to test
        output_dir: Directory to save results
    """
    print("\n" + "=" * 80)
    print(f"LOADING TREES FOR {dataset_name.upper()} DATASET")
    print("=" * 80)
    
    try:
        trees = load_trees(dataset_name)
        print(f"\n✓ Loaded {len(trees)} tree structures: {list(trees.keys())}")
        
        # Run comprehensive benchmarks
        results = run_comprehensive_benchmark(trees, dataset_name)
        
        # Print comparison summary
        print_comparison_summary(results)
        
        # Save results
        dataset_output = output_dir / dataset_name
        dataset_output.mkdir(exist_ok=True, parents=True)
        
        df = save_results_to_csv(results, dataset_output)
        save_results_to_json(results, dataset_output)
        generate_report(df, dataset_output)
        
        return results, df
        
    except FileNotFoundError as e:
        print(f"\n❌ Trees not found for {dataset_name}")
        print(f"   Error: {e}")
        print(f"   Please run the appropriate loader first:")
        print(f"   python src/loaders/load_{dataset_name}_trees.py")
        return None, None
    except Exception as e:
        print(f"\n❌ Error running experiments for {dataset_name}: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def main():
    """Main function to run all filtering experiments."""
    print("=" * 80)
    print("FILTERING EXPERIMENTS - DATA STRUCTURES COMPARISON")
    print("=" * 80)
    print("\nThis script will benchmark filtering operations across:")
    print("  • Binary Search Tree (BST)")
    print("  • AVL Tree")
    print("  • Red-Black Tree")
    print("  • Trie")
    print("\nMetrics measured:")
    print("  • Time Complexity (avg, min, max, std dev)")
    print("  • Space Complexity (memory usage)")
    print("  • Selectivity (percentage of results returned)")
    print("\n")
    
    # Check available datasets
    available = list_saved_trees()
    
    if not available:
        print("❌ No saved trees found!")
        print("\n💡 Please run tree loaders first:")
        print("   python src/loaders/load_airline_trees.py")
        print("   python src/loaders/load_airport_trees.py")
        print("   python src/loaders/load_lounge_trees.py")
        print("   python src/loaders/load_seat_trees.py")
        return
    
    # Output directory
    output_dir = Path(__file__).parent.parent / 'results' / 'filtering'
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Run experiments for each available dataset
    all_results = {}
    all_dataframes = []
    
    for dataset_name in available:
        results, df = run_dataset_experiments(dataset_name, output_dir)
        if results and df is not None:
            all_results[dataset_name] = results
            all_dataframes.append(df)
    
    # Combine all results
    if all_dataframes:
        print("\n" + "=" * 80)
        print("GENERATING COMBINED REPORT")
        print("=" * 80)
        
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        combined_df.to_csv(output_dir / 'all_datasets_combined.csv', index=False)
        
        print(f"\n✅ All experiments completed!")
        print(f"📊 Results saved to: {output_dir}")
        print("\nGenerated files:")
        print(f"  • all_datasets_combined.csv - Combined results from all datasets")
        
        for dataset_name in all_results.keys():
            print(f"  • {dataset_name}/")
            print(f"    - filtering_benchmark_results.csv")
            print(f"    - filtering_benchmark_detailed.json")
            print(f"    - filtering_benchmark_report.txt")
    else:
        print("\n❌ No experiments were successfully completed.")


if __name__ == "__main__":
    main()
