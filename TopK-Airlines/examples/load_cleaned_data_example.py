"""
Example script demonstrating how to load and use cleaned datasets with data structures.

This script shows various ways to load the cleaned data and prepare it for use
with custom data structures (heap, priority queue, hash table, etc.).
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.data_loader import load_cleaned_data, get_dataset_info


def example_1_load_all_datasets():
    """Example 1: Load all cleaned datasets at once."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Load All Cleaned Datasets")
    print("=" * 80)
    
    # Load all datasets into a dictionary
    datasets = load_cleaned_data()
    
    # Access individual datasets
    print("\nAccessing individual datasets:")
    for name, df in datasets.items():
        print(f"\n{name}:")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)[:5]}...")  # Show first 5 columns
        print(f"  Sample row:\n{df.iloc[0]}")


def example_2_load_specific_dataset():
    """Example 2: Load a specific cleaned dataset."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Load Specific Dataset")
    print("=" * 80)
    
    # Load just the airline dataset
    airline_df = load_cleaned_data('airline')
    
    print(f"\nAirline dataset loaded:")
    print(f"  Total records: {len(airline_df):,}")
    print(f"  Columns: {list(airline_df.columns)}")
    print(f"\nFirst 3 rows:")
    print(airline_df.head(3))


def example_3_get_dataset_info():
    """Example 3: Get dataset information without loading full data."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Get Dataset Info (Lightweight)")
    print("=" * 80)
    
    # Get info without loading the entire dataset
    info = get_dataset_info('airline')
    
    print("\nDataset Information:")
    print(f"  Name: {info['name']}")
    print(f"  Path: {info['path']}")
    print(f"  Rows: {info['row_count']:,}")
    print(f"  Columns: {info['column_count']}")
    print(f"  Column names: {info['columns']}")
    print(f"  Data types: {info['dtypes']}")


def example_4_prepare_for_data_structures():
    """Example 4: Prepare data for use with custom data structures."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Prepare Data for Data Structures")
    print("=" * 80)
    
    # Load airline dataset
    airline_df = load_cleaned_data('airline')
    
    # Example: Extract data for a heap/priority queue
    # Assuming you want to rank airlines by some score
    print("\n--- Preparing data for Heap/Priority Queue ---")
    
    # Find a rating column
    rating_cols = [col for col in airline_df.columns if 'rating' in col.lower() or 'score' in col.lower()]
    if rating_cols:
        rating_col = rating_cols[0]
        airline_col = [col for col in airline_df.columns if 'airline' in col.lower()][0]
        
        # Convert to list of tuples (score, airline_name) for heap
        heap_data = list(zip(airline_df[rating_col], airline_df[airline_col]))
        print(f"Created {len(heap_data):,} (score, airline) tuples for heap")
        print(f"Sample entries: {heap_data[:5]}")
    
    # Example: Create hash table mapping
    print("\n--- Preparing data for Hash Table ---")
    
    # Create a dictionary/hash table mapping airline to their records
    if rating_cols:
        airline_col = [col for col in airline_df.columns if 'airline' in col.lower()][0]
        
        # Group by airline
        airline_hash = {}
        for _, row in airline_df.iterrows():
            airline_name = row[airline_col]
            if airline_name not in airline_hash:
                airline_hash[airline_name] = []
            airline_hash[airline_name].append(row.to_dict())
        
        print(f"Created hash table with {len(airline_hash)} unique airlines")
        print(f"Sample airlines: {list(airline_hash.keys())[:5]}")
    
    # Example: Prepare data records as objects
    print("\n--- Converting to structured records ---")
    
    # Convert each row to a dictionary for easy access
    records = airline_df.to_dict('records')
    print(f"Created {len(records):,} record dictionaries")
    print(f"Sample record keys: {list(records[0].keys())}")
    print(f"Sample record:\n{records[0]}")


def example_5_filter_and_prepare():
    """Example 5: Filter data and prepare for Top-K algorithms."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Filter and Prepare for Top-K Algorithms")
    print("=" * 80)
    
    # Load airline dataset
    airline_df = load_cleaned_data('airline')
    
    # Find relevant columns
    airline_col = [col for col in airline_df.columns if 'airline' in col.lower()]
    rating_cols = [col for col in airline_df.columns if 'rating' in col.lower() or 'score' in col.lower()]
    
    if airline_col and rating_cols:
        airline_col = airline_col[0]
        rating_col = rating_cols[0]
        
        print(f"\nUsing columns: {airline_col} and {rating_col}")
        
        # Group by airline and calculate average rating
        airline_avg_ratings = airline_df.groupby(airline_col)[rating_col].agg(['mean', 'count']).reset_index()
        airline_avg_ratings.columns = ['airline', 'avg_rating', 'review_count']
        
        # Filter airlines with minimum number of reviews
        min_reviews = 5
        filtered = airline_avg_ratings[airline_avg_ratings['review_count'] >= min_reviews]
        
        print(f"\nFiltered to {len(filtered)} airlines with >= {min_reviews} reviews")
        print(f"\nTop 10 airlines by average rating:")
        top_10 = filtered.nlargest(10, 'avg_rating')
        print(top_10.to_string(index=False))
        
        # Prepare data for Top-K algorithm
        topk_data = [(row['avg_rating'], row['airline'], row['review_count']) 
                     for _, row in filtered.iterrows()]
        
        print(f"\nPrepared {len(topk_data)} (rating, airline, count) tuples for Top-K algorithm")
        print(f"Sample entries: {topk_data[:3]}")
        
        return topk_data


if __name__ == "__main__":
    print("=" * 80)
    print("CLEANED DATA LOADER - EXAMPLES")
    print("=" * 80)
    print("\nThis script demonstrates how to load cleaned datasets")
    print("and prepare them for use with custom data structures.\n")
    
    try:
        # Run all examples
        example_1_load_all_datasets()
        example_2_load_specific_dataset()
        example_3_get_dataset_info()
        example_4_prepare_for_data_structures()
        topk_data = example_5_filter_and_prepare()
        
        print("\n" + "=" * 80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nNext steps:")
        print("  1. Use load_cleaned_data() to load datasets in your algorithms")
        print("  2. Integrate with your custom data structures (heap, priority_queue, etc.)")
        print("  3. Implement Top-K algorithms using the prepared data")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("\n⚠️  Please run the EDA/explore.ipynb notebook first to generate cleaned datasets!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
