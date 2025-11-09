````markdown
# CS201-G4T6

CS201 Data Structures & Algorithms - Skytrax Dataset Analysis (TopK Airlines)

## Overview
Comparative analysis of tree data structures (BST, AVL, Red-Black, Trie) with filtering implementation and performance benchmarking. Now includes an interactive web frontend for comparing data structure performance across three problems:

1. **Predictive Search (Autocomplete)** - Compare Trie vs Ternary Search Tree
2. **Filter by Rating** - Compare AVL Tree vs Red-Black Tree vs BST  
3. **Sort by Rating** - Compare Tree In-order vs Quick Sort vs Merge Sort vs Timsort

## Quick Start (Frontend)

### 0. Prepare the Data (First Time Only)

**Important:** Before building data structures, you need cleaned data files.

1. **Place raw data files** in the `data/` directory:
   - `airline.csv`
   - `airport.csv`
   - `lounge.csv`
   - `seat.csv`

2. **Clean the data:**
   ```bash
   python EDA/clean_data.py
   ```

   This creates cleaned CSV files in `data/cleaned/` directory.

   > **Alternative:** Run `jupyter notebook EDA/explore.ipynb` and execute all cells

See `DATA_PREPARATION.md` for detailed instructions.

### 1. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Build Data Structures (First Time Only)

**Build rating-based trees:**
```bash
python examples/load_all_datasets.py
```

**Build autocomplete structures:**
```bash
python src/loaders/load_autocomplete_structures.py
```

### 4. Start the Flask Server
```bash
python src/api/app.py
```

Then open your browser to: `http://localhost:3000`

### 5. Use the Frontend
- Select a dataset (Airline, Airport, Lounge, Seat)
- Toggle between different data structures
- View real-time performance metrics (time, comparisons, memory)

## Command Line Usage

### Build Trees (First Time Only)
```bash
python src/loaders/load_airline_trees.py
```

### Run Filtering Tests
```bash
python tests/test_filtering.py
```

### Run Analysis
```bash
python analysis/tree_analysis.py
```

Results will be saved to: `results/filtering/airline/benchmark_results.csv`

## Features

### Interactive Frontend
- Real-time performance comparison
- Toggle between data structures
- Visual metrics display
- Multiple datasets support

### Performance Metrics
- **Time**: Execution time in milliseconds
- **Comparisons**: Number of key comparisons
- **Memory**: Memory usage in bytes/KB
- **Scalability**: Performance across different dataset sizes

### Data Structures Implemented
- **Autocomplete**: Trie, Ternary Search Tree
- **Filtering**: AVL Tree, Red-Black Tree, BST
- **Sorting**: Tree In-order, Quick Sort, Merge Sort, Timsort

## Virtual Environment Notes

- **Activate the virtual environment** before running any commands
- **Deactivate** when done: `deactivate` (Windows/Linux/Mac)
- The `venv` folder should be added to `.gitignore` (it's generated locally)
- If you encounter permission errors, try: `python -m pip install -r requirements.txt`


## Documentation

- `DATA_STRUCTURES_ANALYSIS.md` - Analysis of data structures for each problem
- `DATA_STRUCTURES_SUMMARY.md` - Quick reference table
- `FRONTEND_SETUP.md` - Frontend setup and usage guide

## Contributors
CS201 G4T6