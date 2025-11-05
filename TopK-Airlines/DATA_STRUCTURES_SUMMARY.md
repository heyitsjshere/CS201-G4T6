# Data Structures Summary - Quick Reference

## Problem 1: Predictive Search (Autocomplete)

| Data Structure | Time (Search) | Space | Pros | Cons | Recommendation |
|---------------|---------------|-------|------|------|----------------|
| **Trie** | O(m + k) | O(ALPHABET × N × M) | Fastest prefix matching | High memory | ⭐ Primary |
| **Ternary Search Tree** | O(m + k) | O(N × M) | Good balance | More complex | ⭐ Secondary |
| **Sorted Array** | O(log n + m + k) | O(n) | Simple, low memory | Slower queries | Baseline |

---

## Problem 2: Filter by Rating

| Data Structure | Time (Range Query) | Space | Pros | Cons | Recommendation |
|---------------|-------------------|-------|------|------|----------------|
| **AVL Tree** | O(log n + k) | O(n) | Always balanced | Complex rotations | ⭐ Primary |
| **Red-Black Tree** | O(log n + k) | O(n) | Balanced, fast inserts | Slightly taller | ⭐ Primary |
| **BST** | O(n) worst, O(log n + k) avg | O(n) | Simple | Can be unbalanced | Baseline |
| **Sorted Array** | O(log n + k) | O(n) | Simple, cache-friendly | Slow inserts | Comparison |

---

## Problem 3: Sort by Rating

| Data Structure | Time (Sort) | Space | Pros | Cons | Recommendation |
|---------------|-------------|-------|------|------|----------------|
| **Tree In-order** | O(n) | O(n) | Already sorted | Need traversal | ⭐ Primary |
| **Timsort** | O(n log n) | O(n) | Fast, optimized | Standard sort | ⭐ Secondary |
| **Quick Sort** | O(n log n) avg | O(log n) | In-place | O(n²) worst | Comparison |
| **Merge Sort** | O(n log n) | O(n) | Stable, guaranteed | Extra memory | Comparison |

---

## Recommended Implementation Plan

### Phase 1: Problem 1 (Autocomplete)
1. **Trie** - Main implementation
2. **Ternary Search Tree** - Comparison
3. **Sorted Array** - Baseline

### Phase 2: Problem 2 (Filter)
1. **AVL Tree** - Already implemented
2. **Red-Black Tree** - Already implemented  
3. **BST** - Baseline comparison
4. **Sorted Array** - Additional comparison

### Phase 3: Problem 3 (Sort)
1. **Tree In-order Traversal** - From existing trees
2. **Timsort (Python sorted())** - Baseline
3. **Quick Sort** - Custom implementation
4. **Merge Sort** - Custom implementation

---

## Key Metrics to Measure

### Time Metrics:
- Build/Insert time
- Query/Search time
- Sort time

### Space Metrics:
- Total memory usage
- Memory overhead
- Peak memory

### Additional:
- Number of comparisons
- Cache performance
- Scalability (different dataset sizes)

