# Frontend Setup and Usage Guide

## Overview

This project now includes a web-based frontend for comparing data structure performance across three problems:
1. **Predictive Search (Autocomplete)** - Compare Trie vs Ternary Search Tree
2. **Filter by Rating** - Compare AVL Tree vs Red-Black Tree vs BST
3. **Sort by Rating** - Compare Tree In-order vs Quick Sort vs Merge Sort vs Timsort

## Setup Instructions

### 1. Install Dependencies

```bash
cd "CS201-G4T6/TopK-Airlines"
pip install -r requirements.txt
```

### 2. Build Required Data Structures

Before running the frontend, you need to build the data structures:

```bash
# Build rating-based trees (AVL, RB, BST, Trie)
python examples/load_all_datasets.py

# Build autocomplete structures (String Trie, Ternary Search Tree)
python src/loaders/load_autocomplete_structures.py
```

### 3. Start the Flask Server

```bash
python src/api/app.py
```

The server will start on `http://localhost:3000`

### 4. Open the Frontend

Open your browser and navigate to:
```
http://localhost:3000
```

## Features

### Problem 1: Predictive Search (Autocomplete)

- **Data Structures Available:**
  - Trie (Prefix Tree)
  - Ternary Search Tree

- **How to Use:**
  1. Select a dataset (Airline, Airport, Lounge, or Seat)
  2. Choose a data structure using the toggle buttons
  3. Start typing in the search box (e.g., "Sin" for Singapore Airlines)
  4. View autocomplete suggestions and performance metrics

- **Metrics Displayed:**
  - Time (milliseconds)
  - Number of comparisons
  - Memory usage (bytes)
  - Number of results

### Problem 2: Filter by Overall Rating

- **Data Structures Available:**
  - AVL Tree
  - Red-Black Tree
  - BST (Binary Search Tree)

- **How to Use:**
  1. Select a dataset
  2. Choose a data structure
  3. Set minimum and maximum rating values
  4. Click "Apply Filter"
  5. View filtered results and performance metrics

- **Metrics Displayed:**
  - Time (milliseconds)
  - Number of comparisons
  - Memory usage (bytes)
  - Number of results returned

### Problem 3: Sort by Overall Rating

- **Algorithms Available:**
  - Tree In-order (using existing tree structure)
  - Quick Sort
  - Merge Sort
  - Timsort (Python's built-in)

- **How to Use:**
  1. Select a dataset
  2. Choose a sorting algorithm
  3. Select sort order (Ascending or Descending)
  4. Set result limit (for performance)
  5. Click "Sort Data"
  6. View sorted results and performance metrics

- **Metrics Displayed:**
  - Time (milliseconds)
  - Number of comparisons
  - Memory usage (bytes)
  - Number of items sorted

## Performance Metrics Explained

### Time (ms)
- Execution time in milliseconds
- Lower is better
- Includes all processing time for the operation

### Comparisons
- Number of key comparisons made during the operation
- Important for understanding algorithm efficiency
- Lower is generally better (but depends on data structure)

### Memory (bytes/KB)
- Memory usage of the data structure
- Approximate memory footprint
- Lower is better for space efficiency

### Results Count
- Number of items returned/processed
- Useful for verifying correctness

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /api/datasets` - List available datasets
- `POST /api/autocomplete` - Perform autocomplete search
- `POST /api/filter` - Filter by rating range
- `POST /api/sort` - Sort data
- `GET /api/structure-info` - Get available structures for a dataset

## Troubleshooting

### "Autocomplete structures not available"
- Run: `python src/loaders/load_autocomplete_structures.py`
- This builds the Trie and Ternary Search Tree structures

### "Trees not available"
- Run: `python examples/load_all_datasets.py`
- This builds all the rating-based tree structures

### Port 3000 already in use
- The application will automatically try ports 3001-3009
- Or modify `src/api/app.py` and change the port:
  ```python
  app.run(debug=True, port=3001)  # Use different port
  ```

### CORS errors
- Make sure `flask-cors` is installed: `pip install flask-cors`
- The app already includes CORS configuration

## Project Structure

```
TopK-Airlines/
├── src/
│   ├── api/
│   │   └── app.py              # Flask backend API
│   ├── data_structures/
│   │   ├── string_trie.py      # NEW: String-based Trie for autocomplete
│   │   ├── ternary_search_tree.py  # NEW: TST for autocomplete
│   │   ├── avl_tree.py         # Existing (for filtering)
│   │   ├── red_black_tree.py   # Existing (for filtering)
│   │   └── binary_search_tree.py  # Existing (for filtering)
│   ├── algorithms/
│   │   └── sorting.py          # NEW: Sorting algorithms with metrics
│   ├── loaders/
│   │   └── load_autocomplete_structures.py  # NEW: Loader for autocomplete
│   └── utils/
│       └── performance_tracker.py  # NEW: Performance tracking utilities
├── frontend/
│   └── index.html              # Frontend interface
└── requirements.txt            # Updated dependencies
```

## Next Steps

1. **Compare Performance:**
   - Try different data structures for the same operation
   - Compare metrics side-by-side
   - Test with different datasets

2. **Analyze Results:**
   - Which structure is fastest?
   - Which uses least memory?
   - How do comparisons vary?

3. **Experiment:**
   - Try different search prefixes
   - Test various rating ranges
   - Sort different dataset sizes

## Notes

- The frontend uses debouncing for autocomplete (300ms delay)
- Results are limited to 50 items for display (full results are processed)
- Memory usage is approximate (measured in bytes)
- Comparison counts are tracked where possible (some algorithms use estimates)

