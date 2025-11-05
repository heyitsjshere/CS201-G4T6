"""
Binary Search Tree (BST) implementation for storing airline data.
Nodes are ordered by overall_rating.
"""


class BSTNode:
    """Node in a Binary Search Tree."""
    
    def __init__(self, rating, data):
        """
        Initialize a BST node.
        
        Args:
            rating (float): Overall rating used as the key
            data (dict): Complete row data from the dataset
        """
        self.rating = rating
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree for storing records ordered by rating."""
    
    def __init__(self):
        """Initialize an empty BST."""
        self.root = None
        self.size = 0
    
    def insert(self, rating, data):
        """
        Insert a new node into the BST.
        
        Args:
            rating (float): Overall rating (key)
            data (dict): Complete row data
        """
        if self.root is None:
            self.root = BSTNode(rating, data)
            self.size += 1
        else:
            self._insert_recursive(self.root, rating, data)
    
    def _insert_recursive(self, node, rating, data):
        """Recursively insert a node."""
        if rating <= node.rating:
            if node.left is None:
                node.left = BSTNode(rating, data)
                self.size += 1
            else:
                self._insert_recursive(node.left, rating, data)
        else:
            if node.right is None:
                node.right = BSTNode(rating, data)
                self.size += 1
            else:
                self._insert_recursive(node.right, rating, data)
    
    def search(self, rating):
        """
        Search for nodes with a specific rating.
        
        Args:
            rating (float): Rating to search for
            
        Returns:
            list: All nodes with the given rating
        """
        results = []
        self._search_recursive(self.root, rating, results)
        return results
    
    def _search_recursive(self, node, rating, results):
        """Recursively search for nodes."""
        if node is None:
            return
        
        if rating < node.rating:
            self._search_recursive(node.left, rating, results)
        elif rating > node.rating:
            self._search_recursive(node.right, rating, results)
        else:
            results.append(node.data)
            # Check both sides for duplicate ratings
            self._search_recursive(node.left, rating, results)
            self._search_recursive(node.right, rating, results)
    
    def get_top_k(self, k):
        """
        Get the top K highest rated records.
        
        Args:
            k (int): Number of top records to retrieve
            
        Returns:
            list: Top K records sorted by rating (descending)
        """
        all_nodes = []
        self._inorder_traversal(self.root, all_nodes)
        # Sort in descending order and return top k
        all_nodes.sort(key=lambda x: x['overall_rating'], reverse=True)
        return all_nodes[:k]
    
    def get_range(self, min_rating, max_rating):
        """
        Get all records within a rating range.
        
        Args:
            min_rating (float): Minimum rating (inclusive)
            max_rating (float): Maximum rating (inclusive)
            
        Returns:
            list: All records within the range
        """
        results = []
        self._range_search(self.root, min_rating, max_rating, results)
        return results
    
    def _range_search(self, node, min_rating, max_rating, results):
        """Recursively search for nodes in range."""
        if node is None:
            return
        
        if min_rating < node.rating:
            self._range_search(node.left, min_rating, max_rating, results)
        
        if min_rating <= node.rating <= max_rating:
            results.append(node.data)
        
        if max_rating > node.rating:
            self._range_search(node.right, min_rating, max_rating, results)
    
    def _inorder_traversal(self, node, result):
        """Inorder traversal to get all nodes."""
        if node is not None:
            self._inorder_traversal(node.left, result)
            result.append(node.data)
            self._inorder_traversal(node.right, result)
    
    def get_height(self):
        """Get the height of the tree."""
        return self._get_height_recursive(self.root)
    
    def _get_height_recursive(self, node):
        """Recursively calculate tree height."""
        if node is None:
            return 0
        return 1 + max(self._get_height_recursive(node.left), 
                      self._get_height_recursive(node.right))
    
    def get_size(self):
        """Get the number of nodes in the tree."""
        return self.size
    
    def filter_by_rating(self, min_rating=None, max_rating=None):
        """
        Filter records by rating range (uses indexed tree structure).
        
        Args:
            min_rating (float): Minimum rating (inclusive), None for no lower bound
            max_rating (float): Maximum rating (inclusive), None for no upper bound
            
        Returns:
            list: Filtered records
            
        Time Complexity: O(n) worst case (unbalanced), O(log n + m) best case
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
        results = []
        self._filter_by_field_recursive(self.root, field_name, value, min_value, 
                                       max_value, condition, results)
        return results
    
    def _filter_by_field_recursive(self, node, field_name, value, min_value, 
                                   max_value, condition, results):
        """Recursively filter nodes by field value."""
        if node is None:
            return
        
        # Traverse entire tree (inorder)
        self._filter_by_field_recursive(node.left, field_name, value, min_value, 
                                       max_value, condition, results)
        
        # Check if node matches filter
        if field_name in node.data:
            field_value = node.data[field_name]
            
            if condition == 'equals' and field_value == value:
                results.append(node.data)
            elif condition == 'range' and min_value <= field_value <= max_value:
                results.append(node.data)
            elif condition == 'contains' and value and str(value).lower() in str(field_value).lower():
                results.append(node.data)
            elif condition == 'greater_than' and field_value > value:
                results.append(node.data)
            elif condition == 'less_than' and field_value < value:
                results.append(node.data)
        
        self._filter_by_field_recursive(node.right, field_name, value, min_value, 
                                       max_value, condition, results)
    
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
            
        Time Complexity: O(n) for most efficient ordering
        Space Complexity: O(m) where m is number of results
        """
        # Start with rating filter if present (uses tree structure)
        if 'rating' in filters:
            min_rating = filters['rating'].get('min', float('-inf'))
            max_rating = filters['rating'].get('max', float('inf'))
            results = self.filter_by_rating(min_rating, max_rating)
        else:
            # Get all records
            results = []
            self._inorder_traversal(self.root, results)
        
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
        """String representation of the BST."""
        return f"BinarySearchTree(size={self.size}, height={self.get_height()})"
