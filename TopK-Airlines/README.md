# TopK-Airlines Project

CS201 Data Structures & Algorithms - Skytrax Dataset Analysis

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

### 3. Start the Application

**Option 1: Quick Start (Recommended for first-time setup)**
```bash
python start_frontend.py
```

This will:
- Check dependencies
- Build required data structures (if needed)
- Start the Flask server
- Open browser to `http://localhost:3000`

**Option 2: Direct Start (If everything is already set up)**
```bash
python src/api/app.py
```

This starts the Flask server directly without prerequisite checks.

### 4. Use the Frontend
- Select a dataset (Airline, Airport, Lounge, Seat)
- Toggle between different data structures
- View real-time performance metrics (time, comparisons, memory)

## Manual Setup

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

### 3. Build Data Structures

**Build rating-based trees:**
```bash
python examples/load_all_datasets.py
```

**Build autocomplete structures:**
```bash
python src/loaders/load_autocomplete_structures.py
```

### 4. Start Flask Server
```bash
python src/api/app.py
```

### 5. Access Frontend
Open browser to: `http://localhost:3000`

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

## Project Structure

```
TopK-Airlines/
├── src/
│   ├── api/                    # Flask backend API
│   │   └── app.py
│   ├── data_structures/        # Data structure implementations
│   │   ├── string_trie.py      # NEW: String-based Trie for autocomplete
│   │   ├── ternary_search_tree.py  # NEW: TST for autocomplete
│   │   ├── avl_tree.py
│   │   ├── red_black_tree.py
│   │   └── binary_search_tree.py
│   ├── algorithms/
│   │   └── sorting.py          # NEW: Sorting algorithms with metrics
│   ├── loaders/                # Data loaders
│   └── utils/                  # Utilities
├── frontend/
│   └── index.html              # Frontend interface
├── analysis/                   # Analysis scripts
├── tests/                      # Test files
└── data/                       # Data files
```

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

## Troubleshooting

### Port Permission Errors

If you see "An attempt was made to access a socket in a way forbidden by its access permissions":

1. **Automatic Fix**: The application now automatically tries ports 3000-3009 and will use the first available one
2. **Manual Fix**: Find what's using the port:
   ```bash
   # Windows
   netstat -ano | findstr :3000
   
   # Linux/Mac
   lsof -i :3000
   ```
3. **Run as Administrator** (Windows): Right-click terminal → "Run as administrator"
4. **Use Different Port**: The app will automatically detect and use an available port

See `TROUBLESHOOTING.md` for more detailed solutions.

## Documentation

- `STEP_BY_STEP_GUIDE.md` - Detailed step-by-step guide
- `DATA_STRUCTURES_ANALYSIS.md` - Analysis of data structures for each problem
- `DATA_STRUCTURES_SUMMARY.md` - Quick reference table
- `FRONTEND_SETUP.md` - Frontend setup and usage guide

## Contributors
CS201 G4T6