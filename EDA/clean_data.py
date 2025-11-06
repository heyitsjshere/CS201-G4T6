#!/usr/bin/env python3
"""
Data cleaning script extracted from explore.ipynb.
This script can be run directly without Jupyter notebook.

Usage:
    python EDA/clean_data.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


def clean_dataset(df, dataset_name):
    """
    Clean a dataset by removing null values based on thresholds.
    
    Rules:
    1. Drop columns with >40% null values
    2. Drop rows with null values in columns that have 10-40% null values
    3. Drop rows with null values in columns that have <10% null values
    """
    original_shape = df.shape
    print(f"\n{'=' * 80}")
    print(f"CLEANING DATASET: {dataset_name}")
    print(f"{'=' * 80}")
    print(f"Original shape: {original_shape[0]:,} rows × {original_shape[1]} columns\n")
    
    # drop columns with >40% null values
    null_percentages = df.isnull().sum() / len(df) * 100
    columns_to_drop_high = null_percentages[null_percentages > 40].index.tolist()
    
    if columns_to_drop_high:
        print(f"Dropping {len(columns_to_drop_high)} columns with >40% null values:")
        for col in columns_to_drop_high:
            print(f"  - {col}: {null_percentages[col]:.2f}% null")
        df = df.drop(columns=columns_to_drop_high)
    
    # drop rows with null values in columns that have 10-40% null values
    null_percentages = df.isnull().sum() / len(df) * 100
    columns_medium = null_percentages[(null_percentages >= 10) & (null_percentages <= 40)].index.tolist()
    
    if columns_medium:
        print(f"\nDropping rows with null values in {len(columns_medium)} columns (10-40% nulls):")
        for col in columns_medium:
            print(f"  - {col}: {null_percentages[col]:.2f}% null")
        df = df.dropna(subset=columns_medium)
    

    # drop rows with null values in columns that have <10% null values
    null_percentages = df.isnull().sum() / len(df) * 100
    columns_low = null_percentages[(null_percentages > 0) & (null_percentages < 10)].index.tolist()
    
    if columns_low:
        print(f"\nDropping rows with null values in {len(columns_low)} columns (<10% nulls):")
        for col in columns_low:
            print(f"  - {col}: {null_percentages[col]:.2f}% null")
        df = df.dropna(subset=columns_low)
    else:
        print("\nNo columns with <10% null values found.")
    
    # final check
    final_shape = df.shape
    rows_removed = original_shape[0] - final_shape[0]
    cols_removed = original_shape[1] - final_shape[1]
    
    print(f"\nFinal shape: {final_shape[0]:,} rows × {final_shape[1]} columns")
    print(f"Removed: {rows_removed:,} rows ({rows_removed/original_shape[0]*100:.2f}%) and {cols_removed} columns")
    print(f"Remaining null values: {df.isnull().sum().sum()}")
    
    return df


def main():
    """Main function to clean all datasets."""
    # set up paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    cleaned_dir = data_dir / 'cleaned'
    
    # create cleaned directory if it doesn't exist
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("DATA CLEANING SCRIPT")
    print("=" * 80)
    print(f"\nData directory: {data_dir.absolute()}")
    print(f"Output directory: {cleaned_dir.absolute()}\n")
    
    # check for CSV files
    csv_files = list(data_dir.glob('*.csv'))
    
    if not csv_files:
        print("ERROR: No CSV files found in data directory!")
        print(f"\nExpected files:")
        print("  - airline.csv")
        print("  - airport.csv")
        print("  - lounge.csv")
        print("  - seat.csv")
        print(f"\nPlease ensure these files are in: {data_dir.absolute()}")
        return False
    
    print(f"Found {len(csv_files)} CSV file(s):")
    for file in csv_files:
        print(f"  - {file.name}")
    
    # load and clean each dataset
    cleaned_dataframes = {}
    
    for csv_file in csv_files:
        dataset_name = csv_file.stem
        
        try:
            # load dataset
            print(f"\n{'=' * 80}")
            print(f"Loading: {dataset_name}")
            print(f"{'=' * 80}")
            df = pd.read_csv(csv_file)
            print(f"Loaded {len(df):,} rows")
            
            # clean dataset
            cleaned_df = clean_dataset(df, dataset_name)
            cleaned_dataframes[dataset_name] = cleaned_df
            
            # save cleaned dataset
            output_file = cleaned_dir / f"{dataset_name}_cleaned.csv"
            cleaned_df.to_csv(output_file, index=False)
            print(f"\nSaved cleaned dataset to: {output_file.name}")
            
        except Exception as e:
            print(f"\nERROR: Error processing {dataset_name}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # save summary
    if cleaned_dataframes:
        summary_file = cleaned_dir / 'cleaning_summary.txt'
        with open(summary_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("DATA CLEANING SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            
            for name, df in cleaned_dataframes.items():
                f.write(f"Dataset: {name}\n")
                f.write("-" * 80 + "\n")
                f.write(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns\n")
                f.write(f"Columns: {', '.join(df.columns)}\n")
                f.write(f"Memory: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB\n")
                f.write(f"Missing values: {df.isnull().sum().sum()}\n\n")
        
        print("\n" + "=" * 80)
        print("CLEANING COMPLETE!")
        print("=" * 80)
        print(f"\nCleaned {len(cleaned_dataframes)} dataset(s):")
        for name, df in cleaned_dataframes.items():
            print(f"  {name}: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"\nSaved to: {cleaned_dir.absolute()}")
        return True
    else:
        print("\nERROR: No datasets were cleaned successfully.")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

