# Data Structures Analysis for Frontend Features

This document lists potential data structures for each of the 3 problems, with time and space complexity analysis for performance comparison.

---

## Problem 1: Predictive Search (Autocomplete)

**Requirement:** As user types "Sin", suggest "Singapore Airlines" (prefix matching)

**What we need:** Fast prefix matching on string names (airline_name, airport_name, lounge_name, seat descriptions)

### Recommended Data Structures:

#### 1. **Trie (Prefix Tree)** ⭐ RECOMMENDED
- **Time Complexity:** 
  - Insert: O(m) where m = length of string
  - Search prefix: O(m + k) where k = number of results
- **Space Complexity:** O(ALPHABET_SIZE * N * M) where N = number of strings, M = average length
- **Pros:** 
  - Fastest for prefix matching
  - Efficient for autocomplete
  - Can limit results to top K matches
- **Cons:** 
  - Higher memory usage (each character = node)
  - More complex implementation
- **Best for:** Real-time autocomplete where speed matters most

#### 2. **Ternary Search Tree (TST)**
- **Time Complexity:** 
  - Insert: O(m log n) average
  - Search prefix: O(m + k) where k = number of results
- **Space Complexity:** O(N * M) - more space-efficient than Trie
- **Pros:** 
  - Better space efficiency than Trie
  - Still fast for prefix matching
  - Combines benefits of BST and Trie
- **Cons:** 
  - More complex than Trie
  - Slightly slower than Trie for exact prefix matching
- **Best for:** When you need Trie benefits but want better space efficiency

#### 3. **Sorted Array with Binary Search**
- **Time Complexity:** 
  - Build: O(n log n) to sort
  - Search prefix: O(log n + m + k) where m = prefix length, k = results
- **Space Complexity:** O(n) - just the array
- **Pros:** 
  - Simple implementation
  - Low memory overhead
  - Good cache locality
- **Cons:** 
  - Slower than Trie for prefix matching
  - Need to scan linearly after finding first match
  - Insertion is O(n) if unsorted
- **Best for:** Small datasets or when memory is constrained

#### 4. **Binary Search Tree (BST)**
- **Time Complexity:** 
  - Insert: O(log n) average, O(n) worst case
  - Search prefix: O(n) worst case (need to traverse tree)
- **Space Complexity:** O(n)
- **Pros:** 
  - Dynamic (easy to add/remove)
  - Simple structure
- **Cons:** 
  - Not optimized for prefix matching
  - Need full tree traversal to find all prefixes
  - Unbalanced trees can be slow
- **Best for:** Not recommended for prefix matching specifically

#### 5. **Hash Table with Prefix Hashing**
- **Time Complexity:** 
  - Insert: O(m) average
  - Search prefix: O(n) - need to check all keys
- **Space Complexity:** O(n)
- **Pros:** 
  - O(1) average lookup for exact matches
- **Cons:** 
  - Not good for prefix matching
  - Would need to hash all possible prefixes (wasteful)
- **Best for:** Not recommended - use for exact matches only

#### 6. **Inverted Index (for text search)**
- **Time Complexity:** 
  - Build: O(n * m)
  - Search prefix: O(1) to find matches, O(k) to retrieve
- **Space Complexity:** O(n * m) - stores all prefixes
- **Pros:** 
  - Very fast lookups
  - Can handle fuzzy matching
- **Cons:** 
  - High memory usage (stores all prefixes)
  - Complex implementation
- **Best for:** Search engines, but overkill for simple autocomplete

---

## Problem 2: Filter by Overall Rating

**Requirement:** Filter records by rating range (e.g., show all with rating >= 4.0)

**What we need:** Efficient range queries on numeric ratings

### Recommended Data Structures:

#### 1. **AVL Tree** ⭐ RECOMMENDED
- **Time Complexity:** 
  - Insert: O(log n)
  - Range query: O(log n + k) where k = number of results in range
  - Search: O(log n)
- **Space Complexity:** O(n)
- **Pros:** 
  - Always balanced (guaranteed O(log n))
  - Efficient range queries
  - Already implemented in your codebase
- **Cons:** 
  - More complex rotations than BST
  - Slightly slower inserts than Red-Black
- **Best for:** When you need guaranteed balanced tree performance

#### 2. **Red-Black Tree** ⭐ RECOMMENDED
- **Time Complexity:** 
  - Insert: O(log n)
  - Range query: O(log n + k) where k = number of results
  - Search: O(log n)
- **Space Complexity:** O(n)
- **Pros:** 
  - Always balanced
  - Faster inserts than AVL (fewer rotations)
  - Already implemented in your codebase
- **Cons:** 
  - Slightly taller than AVL (2*log(n+1) vs 1.44*log(n+2))
- **Best for:** When you need balanced tree with faster inserts

#### 3. **Binary Search Tree (BST)**
- **Time Complexity:** 
  - Insert: O(log n) average, O(n) worst case (unbalanced)
  - Range query: O(n) worst case, O(log n + k) best case
  - Search: O(log n) average, O(n) worst case
- **Space Complexity:** O(n)
- **Pros:** 
  - Simple implementation
  - Already implemented
- **Cons:** 
  - Can become unbalanced (bad worst case)
  - Performance degrades with sorted input
- **Best for:** Comparison baseline, not recommended for production

#### 4. **Sorted Array**
- **Time Complexity:** 
  - Build: O(n log n) to sort
  - Range query: O(log n + k) - binary search to find start, then linear scan
  - Insert: O(n) - need to shift elements
- **Space Complexity:** O(n)
- **Pros:** 
  - Very simple
  - Excellent cache locality
  - Fast range queries if already sorted
- **Cons:** 
  - Slow inserts/deletes
  - Need to rebuild if data changes
- **Best for:** Static data that doesn't change often

#### 5. **Segment Tree**
- **Time Complexity:** 
  - Build: O(n)
  - Range query: O(log n)
  - Update: O(log n)
- **Space Complexity:** O(4*n) ≈ O(n)
- **Pros:** 
  - Very fast range queries
  - Can handle range updates efficiently
- **Cons:** 
  - More complex implementation
  - Overkill for simple filtering
  - Not good for retrieving full records
- **Best for:** Range queries on aggregated data (sums, min, max)

#### 6. **B-Tree**
- **Time Complexity:** 
  - Insert: O(log n)
  - Range query: O(log n + k)
  - Search: O(log n)
- **Space Complexity:** O(n)
- **Pros:** 
  - Optimized for disk access (good for large datasets)
  - Always balanced
- **Cons:** 
  - More complex than AVL/RB trees
  - Overkill for in-memory operations
- **Best for:** Very large datasets or database systems

#### 7. **Hash Table (for exact matches only)**
- **Time Complexity:** 
  - Insert: O(1) average
  - Range query: O(n) - cannot do range queries efficiently
- **Space Complexity:** O(n)
- **Pros:** 
  - O(1) exact lookups
- **Cons:** 
  - Cannot do range queries
- **Best for:** Not suitable for this problem

---

## Problem 3: Sort by Overall Rating

**Requirement:** Sort displayed data by rating (ascending/descending)

**What we need:** Efficient sorting of current results/data

### Recommended Data Structures:

#### 1. **Already Sorted Tree (In-order Traversal)** ⭐ RECOMMENDED
- **Time Complexity:** 
  - Get sorted list: O(n) - in-order traversal
  - Reverse: O(1) - just reverse the list
- **Space Complexity:** O(n) for result list
- **Pros:** 
  - If data is already in AVL/RB/BST tree, in-order traversal gives sorted order
  - Very efficient
  - No need to re-sort
- **Cons:** 
  - Need to traverse tree each time
- **Best for:** When data is already in a tree structure

#### 2. **Heap (Min/Max Heap)**
- **Time Complexity:** 
  - Build: O(n)
  - Extract all: O(n log n)
  - Get min/max: O(1)
- **Space Complexity:** O(n)
- **Pros:** 
  - O(1) to get min/max
  - Good for top-K queries
- **Cons:** 
  - Need to extract all elements to get full sorted list
  - Not ideal for full sorting
- **Best for:** When you only need top-K or min/max, not full sort

#### 3. **Quick Sort on Array**
- **Time Complexity:** 
  - Sort: O(n log n) average, O(n²) worst case
  - Reverse: O(n) - just reverse array
- **Space Complexity:** O(log n) - recursion stack
- **Pros:** 
  - Fast average case
  - In-place sorting
  - Simple implementation
- **Cons:** 
  - O(n²) worst case
  - Not stable
- **Best for:** General-purpose sorting, good average performance

#### 4. **Merge Sort on Array**
- **Time Complexity:** 
  - Sort: O(n log n) worst case
  - Reverse: O(n)
- **Space Complexity:** O(n) - needs temporary array
- **Pros:** 
  - Guaranteed O(n log n)
  - Stable sort
- **Cons:** 
  - Extra memory needed
- **Best for:** When you need guaranteed performance and stability

#### 5. **Timsort (Python's built-in sort)**
- **Time Complexity:** 
  - Sort: O(n log n) worst case, O(n) best case (already sorted)
  - Reverse: O(n)
- **Space Complexity:** O(n)
- **Pros:** 
  - Very fast for partially sorted data
  - Stable sort
  - Optimized implementation
- **Cons:** 
  - More complex algorithm
- **Best for:** Default choice in Python, very efficient

#### 6. **Counting Sort (if ratings are discrete)**
- **Time Complexity:** 
  - Sort: O(n + k) where k = range of values
- **Space Complexity:** O(n + k)
- **Pros:** 
  - Very fast if range is small (e.g., ratings 1-10)
- **Cons:** 
  - Only works for discrete values
  - High memory if range is large
- **Best for:** When ratings are limited integers (e.g., 1-10 scale)

#### 7. **Radix Sort (for fixed precision)**
- **Time Complexity:** 
  - Sort: O(d * n) where d = number of digits
- **Space Complexity:** O(n + k)
- **Pros:** 
  - Fast for fixed-width numbers
- **Cons:** 
  - Only works for fixed-width numeric data
- **Best for:** When you have many records with fixed-precision ratings

---

## Recommended Implementation Strategy

### For Problem 1 (Autocomplete):
**Primary:** Trie - Best for prefix matching
**Comparison:** Ternary Search Tree, Sorted Array

### For Problem 2 (Filter by Rating):
**Primary:** AVL Tree and Red-Black Tree - Already implemented, efficient
**Comparison:** BST (baseline), Sorted Array

### For Problem 3 (Sort by Rating):
**Primary:** In-order traversal of existing tree - Most efficient
**Comparison:** Quick Sort, Merge Sort, Timsort (Python's sorted())

---

## Performance Metrics to Track

### Time Metrics:
1. **Build/Insert time:** How long to create the data structure
2. **Query time:** How long to perform the operation
3. **Memory allocation time:** Time spent allocating memory

### Space Metrics:
1. **Memory usage:** Total memory consumed by data structure
2. **Memory overhead:** Extra memory beyond data itself
3. **Peak memory:** Maximum memory during operations

### Additional Metrics:
1. **Cache performance:** Cache hits/misses
2. **Scalability:** Performance as dataset size increases
3. **Comparison count:** Number of comparisons (for sorting)

---

## Implementation Priority

1. **Problem 1:** Implement Trie first (most important for autocomplete)
2. **Problem 2:** Use existing AVL/RB trees, compare with BST baseline
3. **Problem 3:** Use in-order traversal, compare with Python's sorted()

This gives you a good mix of:
- Different data structures (Trie, Trees, Arrays)
- Different complexity characteristics
- Real-world applicable structures
- Clear performance differences to showcase

