"""
Trie (Prefix Tree) implementation for storing airline data.
Each level represents a digit of the rating (multiplied by 10 for precision).
For example: rating 4.5 -> path 4 -> 5
"""


class TrieNode:
    """Node in a Trie."""
    
    def __init__(self):
        """Initialize a Trie node."""
        self.children = {}  # digit -> TrieNode
        self.data_list = []  # List of records ending at this node
        self.is_end = False


class Trie:
    """
    Trie (Prefix Tree) for storing records indexed by rating.
    Ratings are converted to strings for trie traversal.
    """
    
    def __init__(self):
        """Initialize an empty Trie."""
        self.root = TrieNode()
        self.size = 0
    
    def _rating_to_key(self, rating):
        """
        Convert rating to a string key for trie.
        
        Args:
            rating (float): Rating value
            
        Returns:
            str: String representation with fixed precision
        """
        # Convert to string with 1 decimal place, remove decimal point
        # E.g., 4.5 -> "45", 3.0 -> "30", 10.0 -> "100"
        return f"{rating:.1f}".replace('.', '')
    
    def insert(self, rating, data):
        """
        Insert a new record into the Trie.
        
        Args:
            rating (float): Overall rating (key)
            data (dict): Complete row data
        """
        key = self._rating_to_key(rating)
        node = self.root
        
        # Traverse/create path for each digit
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        # Store data at the leaf
        node.is_end = True
        node.data_list.append(data)
        self.size += 1
    
    def search(self, rating):
        """
        Search for all records with a specific rating.
        
        Args:
            rating (float): Rating to search for
            
        Returns:
            list: All records with the given rating
        """
        key = self._rating_to_key(rating)
        node = self.root
        
        # Traverse the trie
        for char in key:
            if char not in node.children:
                return []
            node = node.children[char]
        
        if node.is_end:
            return node.data_list.copy()
        return []
    
    def search_prefix(self, rating_prefix):
        """
        Search for all records with ratings starting with a prefix.
        For example: 4.0 would match 4.0, 4.1, 4.2, ..., 4.9
        
        Args:
            rating_prefix (float): Rating prefix to search for
            
        Returns:
            list: All records matching the prefix
        """
        key = self._rating_to_key(rating_prefix)
        node = self.root
        
        # Traverse to the prefix node
        for char in key:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all records under this prefix
        results = []
        self._collect_all_records(node, results)
        return results
    
    def _collect_all_records(self, node, results):
        """Recursively collect all records from a node downwards."""
        if node.is_end:
            results.extend(node.data_list)
        
        for child in node.children.values():
            self._collect_all_records(child, results)
    
    def get_top_k(self, k):
        """
        Get the top K highest rated records.
        
        Args:
            k (int): Number of top records to retrieve
            
        Returns:
            list: Top K records sorted by rating (descending)
        """
        all_records = self.get_all_records()
        all_records.sort(key=lambda x: x['overall_rating'], reverse=True)
        return all_records[:k]
    
    def get_range(self, min_rating, max_rating):
        """
        Get all records within a rating range.
        
        Args:
            min_rating (float): Minimum rating (inclusive)
            max_rating (float): Maximum rating (inclusive)
            
        Returns:
            list: All records within the range
        """
        all_records = self.get_all_records()
        return [r for r in all_records 
                if min_rating <= r['overall_rating'] <= max_rating]
    
    def get_all_records(self):
        """
        Get all records stored in the trie.
        
        Returns:
            list: All records
        """
        results = []
        self._collect_all_records(self.root, results)
        return results
    
    def get_size(self):
        """Get the number of records in the trie."""
        return self.size
    
    def _get_height(self):
        """Calculate the maximum height of the trie."""
        return self._get_height_recursive(self.root)
    
    def _get_height_recursive(self, node):
        """Recursively calculate trie height."""
        if not node.children:
            return 0
        return 1 + max(self._get_height_recursive(child) 
                      for child in node.children.values())
    
    def get_height(self):
        """Get the height of the trie."""
        return self._get_height_recursive(self.root)
    
    def filter_by_rating(self, min_rating=None, max_rating=None):
        """
        Filter records by rating range.
        
        Args:
            min_rating (float): Minimum rating (inclusive), None for no lower bound
            max_rating (float): Maximum rating (inclusive), None for no upper bound
            
        Returns:
            list: Filtered records
            
        Time Complexity: O(n) - Trie must collect and filter all records
        Space Complexity: O(m) where m is number of results
        """
        if min_rating is None:
            min_rating = float('-inf')
        if max_rating is None:
            max_rating = float('inf')
        
        return self.get_range(min_rating, max_rating)
    
    def filter_by_field(self, field_name, value=None, min_value=None, max_value=None, 
                       condition='equals'):
        """
        Filter records by any non-indexed field (requires linear scan).
        
        Args:
            field_name (str): Field name to filter by (e.g., 'recommended', 'cabin_flown')
            value: Exact value to match (for condition='equals')
            min_value: Minimum value (for condition='range')
            max_value: Maximum value (for condition='range')
            condition (str): 'equals', 'range', 'contains', 'greater_than', 'less_than'
            
        Returns:
            list: Filtered records
            
        Time Complexity: O(n) - must scan all nodes
        Space Complexity: O(m) where m is number of results
        """
        all_records = self.get_all_records()
        results = []
        
        for record in all_records:
            if field_name not in record:
                continue
            
            field_value = record[field_name]
            
            if condition == 'equals' and field_value == value:
                results.append(record)
            elif condition == 'range' and min_value <= field_value <= max_value:
                results.append(record)
            elif condition == 'contains' and value and str(value).lower() in str(field_value).lower():
                results.append(record)
            elif condition == 'greater_than' and field_value > value:
                results.append(record)
            elif condition == 'less_than' and field_value < value:
                results.append(record)
        
        return results
    
    def filter_multi_criteria(self, filters):
        """
        Apply multiple filters simultaneously.
        
        Args:
            filters (dict): Dictionary of filter specifications
                Example: {
                    'rating': {'min': 4.0, 'max': 5.0},
                    'recommended': {'value': True},
                    'cabin_flown': {'value': 'Business Class'}
                }
        
        Returns:
            list: Records matching all filter criteria
            
        Time Complexity: O(n) - must scan all records
        Space Complexity: O(m) where m is number of results
        """
        # Start with rating filter if present
        if 'rating' in filters:
            min_rating = filters['rating'].get('min', float('-inf'))
            max_rating = filters['rating'].get('max', float('inf'))
            results = self.filter_by_rating(min_rating, max_rating)
        else:
            # Get all records
            results = self.get_all_records()
        
        # Apply additional filters sequentially
        for field, criteria in filters.items():
            if field == 'rating':
                continue  # Already applied
            
            if 'value' in criteria:
                results = [r for r in results if r.get(field) == criteria['value']]
            elif 'min' in criteria and 'max' in criteria:
                results = [r for r in results 
                          if criteria['min'] <= r.get(field, float('-inf')) <= criteria['max']]
        
        return results
    
    def __str__(self):
        """String representation of the Trie."""
        return f"Trie(size={self.size}, height={self.get_height()})"
