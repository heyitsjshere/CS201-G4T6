"""
HashMap implementation for storing records indexed by overall rating.
Uses hash table with buckets for efficient exact lookups, but requires scanning for range queries.
"""

import sys


class HashMap:
    """
    HashMap (Hash Table) for storing records indexed by rating.
    Uses chaining to handle collisions.
    """
    
    def __init__(self, initial_capacity=16, load_factor=0.75):
        """
        Initialize an empty HashMap.

        Args:
            initial_capacity (int): Initial number of buckets
            load_factor (float): Load factor threshold for resizing
        """
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        self.comparisons = 0
        self._cached_memory = None  # Cached memory calculation
        self._memory_dirty = True  # Flag to track if cache needs update
    
    def _hash(self, key):
        """
        Hash function for rating keys.
        Converts float rating to integer hash.
        
        Args:
            key (float): Rating value
            
        Returns:
            int: Hash value
        """
        # Convert rating to integer (multiply by 10 to preserve 1 decimal place)
        # This allows us to use integer hashing
        if key is None:
            return 0
        int_key = int(float(key) * 10)
        return hash(int_key) % self.capacity
    
    def _resize(self):
        """Resize the hash table when load factor is exceeded."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        # Rehash all existing items
        for bucket in old_buckets:
            for rating, data_list in bucket:
                for data in data_list:
                    self._insert_internal(rating, data)
    
    def _insert_internal(self, rating, data):
        """Internal insert method without resize check."""
        index = self._hash(rating)
        bucket = self.buckets[index]
        
        # Check if this rating already exists in the bucket
        found = False
        for i, (existing_rating, data_list) in enumerate(bucket):
            self.comparisons += 1
            if existing_rating == rating:
                # Add to existing list
                data_list.append(data)
                found = True
                break
        
        if not found:
            # Create new entry for this rating
            bucket.append((rating, [data]))
            self.size += 1
    
    def insert(self, rating, data):
        """
        Insert a record into the HashMap.
        
        Args:
            rating (float): Overall rating (key)
            data (dict): Complete row data
        """
        if rating is None:
            return
        
        # Check if resize is needed
        if (self.size / self.capacity) >= self.load_factor:
            self._resize()

        self._insert_internal(rating, data)
        self._memory_dirty = True  # Mark memory cache as dirty after insert
    
    def get_range(self, min_rating, max_rating):
        """
        Get all records within a rating range.
        
        Args:
            min_rating (float): Minimum rating (inclusive)
            max_rating (float): Maximum rating (inclusive)
            
        Returns:
            list: All records within the range
            
        Time Complexity: O(n) - must scan all buckets and entries
        Space Complexity: O(m) where m is number of results
        """
        results = []
        
        # Iterate through all buckets
        for bucket in self.buckets:
            for rating, data_list in bucket:
                self.comparisons += 1
                if min_rating <= rating <= max_rating:
                    results.extend(data_list)
                    self.comparisons += len(data_list)
        
        return results
    
    def filter_by_rating(self, min_rating=None, max_rating=None):
        """
        Filter records by rating range.
        
        Args:
            min_rating (float): Minimum rating (inclusive), None for no lower bound
            max_rating (float): Maximum rating (inclusive), None for no upper bound
            
        Returns:
            list: Filtered records
            
        Time Complexity: O(n) - must scan all buckets
        Space Complexity: O(m) where m is number of results
        """
        if min_rating is None:
            min_rating = float('-inf')
        if max_rating is None:
            max_rating = float('inf')
        
        return self.get_range(min_rating, max_rating)
    
    def get_size(self):
        """Get the total number of records in the HashMap."""
        total = 0
        for bucket in self.buckets:
            for rating, data_list in bucket:
                total += len(data_list)
        return total
    
    def get_height(self):
        """HashMap doesn't have a height concept, return 0."""
        return 0
    
    def get_total_comparisons(self):
        """Get total number of comparisons made."""
        return self.comparisons
    
    def get_memory_usage(self):
        """Get actual memory usage in bytes using sys.getsizeof with caching."""
        if self._memory_dirty or self._cached_memory is None:
            self._cached_memory = self._calculate_memory()
            self._memory_dirty = False
        return self._cached_memory

    def _calculate_memory(self):
        """Calculate actual memory usage of the HashMap."""
        # Size of the HashMap object itself
        memory = sys.getsizeof(self)

        # Size of the buckets list
        memory += sys.getsizeof(self.buckets)

        # Size of each bucket and its contents
        for bucket in self.buckets:
            memory += sys.getsizeof(bucket)

            # Size of each (rating, data_list) tuple in the bucket
            for rating, data_list in bucket:
                memory += sys.getsizeof(rating)
                memory += sys.getsizeof(data_list)

                # Size of each data item in the list
                for data in data_list:
                    memory += sys.getsizeof(data)
                    # Add size of dict contents
                    if isinstance(data, dict):
                        for key, value in data.items():
                            memory += sys.getsizeof(key) + sys.getsizeof(value)

        return memory
    
    def reset_comparisons(self):
        """Reset comparison counter."""
        self.comparisons = 0
    
    def __str__(self):
        """String representation of the HashMap."""
        return f"HashMap(capacity={self.capacity}, size={self.get_size()}, load_factor={self.size/self.capacity:.2f})"

