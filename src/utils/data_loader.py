import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Union


def load_data_from_csv(file_path):
    """Load a single CSV file into a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None


def load_cleaned_data(dataset_name: Optional[str] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Load cleaned datasets from the cleaned_data directory.
    
    Args:
        dataset_name: Name of a specific dataset to load (e.g., 'airline', 'airport', 'lounge', 'seat')
                     If None, loads all cleaned datasets.
    
    Returns:
        If dataset_name is provided: A single DataFrame
        If dataset_name is None: A dictionary of DataFrames with dataset names as keys
    
    Examples:
        # Load a specific dataset
        airline_df = load_cleaned_data('airline')
        
        # Load all datasets
        all_data = load_cleaned_data()
        airline_df = all_data['airline']
        airport_df = all_data['airport']
    """
    # Get the path to the cleaned data directory
    current_dir = Path(__file__).parent
    cleaned_data_dir = current_dir / '../../data/cleaned'
    
    if not cleaned_data_dir.exists():
        raise FileNotFoundError(
            f"Cleaned data directory not found at {cleaned_data_dir.absolute()}.\n"
            "Please run the EDA/explore.ipynb notebook first to generate cleaned datasets."
        )
    
    # If specific dataset requested
    if dataset_name:
        file_path = cleaned_data_dir / f"{dataset_name}_cleaned.csv"
        if not file_path.exists():
            raise FileNotFoundError(
                f"Cleaned dataset '{dataset_name}' not found at {file_path}.\n"
                f"Available datasets: {[f.stem.replace('_cleaned', '') for f in cleaned_data_dir.glob('*_cleaned.csv')]}"
            )
        
        print(f"Loading cleaned dataset: {dataset_name}")
        df = pd.read_csv(file_path)
        print(f"Loaded {dataset_name}: {df.shape[0]:,} rows × {df.shape[1]} columns")
        return df
    
    # Load all cleaned datasets
    cleaned_files = list(cleaned_data_dir.glob('*_cleaned.csv'))
    
    if not cleaned_files:
        raise FileNotFoundError(
            f"No cleaned datasets found in {cleaned_data_dir.absolute()}.\n"
            "Please run the EDA/explore.ipynb notebook first to generate cleaned datasets."
        )
    
    dataframes = {}
    print("Loading all cleaned datasets...")
    print("=" * 80)
    
    for file_path in cleaned_files:
        dataset_name = file_path.stem.replace('_cleaned', '')
        df = pd.read_csv(file_path)
        dataframes[dataset_name] = df
        print(f"Loaded {dataset_name}: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    print("=" * 80)
    print(f"Successfully loaded {len(dataframes)} cleaned datasets")
    
    return dataframes


def get_dataset_info(dataset_name: str) -> Dict[str, any]:
    """
    Get information about a cleaned dataset without loading all the data.
    
    Args:
        dataset_name: Name of the dataset (e.g., 'airline', 'airport', 'lounge', 'seat')
    
    Returns:
        Dictionary containing dataset information (columns, row count, etc.)
    """
    current_dir = Path(__file__).parent
    cleaned_data_dir = current_dir / '../../data/cleaned'
    file_path = cleaned_data_dir / f"{dataset_name}_cleaned.csv"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset '{dataset_name}' not found at {file_path}")
    
    # Read just the first few rows to get structure
    df_sample = pd.read_csv(file_path, nrows=5)
    
    # Get total row count
    with open(file_path, 'r') as f:
        row_count = sum(1 for _ in f) - 1  # Subtract header row
    
    return {
        'name': dataset_name,
        'path': str(file_path),
        'columns': list(df_sample.columns),
        'dtypes': dict(df_sample.dtypes),
        'row_count': row_count,
        'column_count': len(df_sample.columns)
    }


def preprocess_data(data):
    """Placeholder for additional data preprocessing steps."""
    # This function can be expanded based on specific requirements
    return data


def get_airline_data(file_path):
    """Legacy function - Load and preprocess airline data from a specific file."""
    data = load_data_from_csv(file_path)
    if data is not None:
        processed_data = preprocess_data(data)
        return processed_data
    return None


if __name__ == "__main__":
    """
    Test the data loader by running this file directly.
    Usage: python src/utils/data_loader.py
    """
    print("\n" + "=" * 80)
    print("TESTING DATA LOADER")
    print("=" * 80)
    
    try:
        # Test loading all datasets
        print("\nAttempting to load all cleaned datasets...")
        datasets = load_cleaned_data()
        
        print("\n" + "=" * 80)
        print("SUCCESS! All datasets loaded successfully!")
        print("=" * 80)
        
        print("\nDataset Summary:")
        print("-" * 80)
        for name, df in datasets.items():
            print(f"  {name:15} | {df.shape[0]:,} rows × {df.shape[1]:2} columns | {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
        
        print("\n" + "=" * 80)
        print("DATA LOADER IS WORKING CORRECTLY!")
        print("=" * 80)
        print("\nYou can now use load_cleaned_data() in your code:")
        print("  from src.utils.data_loader import load_cleaned_data")
        print("  data = load_cleaned_data('airline')")
        print("\n")
        
    except FileNotFoundError as e:
        print("\n" + "=" * 80)
        print("ERROR: Cleaned data not found!")
        print("=" * 80)
        print(f"\n{e}")
        print("\nAction Required:")
        print("  1. Open and run: EDA/explore.ipynb")
        print("  2. Execute all cells to generate cleaned datasets")
        print("  3. Then run this file again")
        print("\n")
    except Exception as e:
        print("\n" + "=" * 80)
        print("ERROR: UNEXPECTED ERROR")
        print("=" * 80)
        print(f"\n{e}")
        import traceback
        traceback.print_exc()
        print("\n")