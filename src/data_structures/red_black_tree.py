"""
Red-Black Tree implementation for storing airline data.
Nodes are ordered by overall_rating with self-balancing properties.
"""


class Color:
    """Colors for Red-Black Tree nodes."""
    RED = 0
    BLACK = 1


class RBNode:
    """Node in a Red-Black Tree."""
    
    def __init__(self, rating, data, color=Color.RED):
        """
        Initialize a Red-Black Tree node.
        
        Args:
            rating (float): Overall rating used as the key
            data (dict): Complete row data from the dataset
            color (int): Node color (RED or BLACK)
        """
        self.rating = rating
        self.data = data
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    """Red-Black Tree (self-balancing BST) for storing records ordered by rating."""
    
    def __init__(self):
        """Initialize an empty Red-Black Tree."""
        self.NIL = RBNode(None, None, Color.BLACK)  # Sentinel node
        self.root = self.NIL
        self.size = 0
    
    def insert(self, rating, data):
        """
        Insert a new node into the Red-Black Tree.
        
        Args:
            rating (float): Overall rating (key)
            data (dict): Complete row data
        """
        new_node = RBNode(rating, data)
        new_node.left = self.NIL
        new_node.right = self.NIL
        
        parent = None
        current = self.root
        
        # Find the position to insert
        while current != self.NIL:
            parent = current
            if new_node.rating <= current.rating:
                current = current.left
            else:
                current = current.right
        
        new_node.parent = parent
        
        if parent is None:
            self.root = new_node
        elif new_node.rating <= parent.rating:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self.size += 1
        self._fix_insert(new_node)
    
    def _fix_insert(self, node):
        """Fix Red-Black Tree properties after insertion."""
        while node.parent and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._rotate_left(node.parent.parent)
        
        self.root.color = Color.BLACK
    
    def _rotate_left(self, x):
        """Perform left rotation."""
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def _rotate_right(self, y):
        """Perform right rotation."""
        x = y.left
        y.left = x.right
        
        if x.right != self.NIL:
            x.right.parent = y
        
        x.parent = y.parent
        
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        
        x.right = y
        y.parent = x
    
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
        if node == self.NIL:
            return
        
        if rating < node.rating:
            self._search_recursive(node.left, rating, results)
        elif rating > node.rating:
            self._search_recursive(node.right, rating, results)
        else:
            results.append(node.data)
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
        if node == self.NIL:
            return
        
        if min_rating < node.rating:
            self._range_search(node.left, min_rating, max_rating, results)
        
        if min_rating <= node.rating <= max_rating:
            results.append(node.data)
        
        if max_rating > node.rating:
            self._range_search(node.right, min_rating, max_rating, results)
    
    def _inorder_traversal(self, node, result):
        """Inorder traversal to get all nodes."""
        if node != self.NIL:
            self._inorder_traversal(node.left, result)
            result.append(node.data)
            self._inorder_traversal(node.right, result)
    
    def get_height(self):
        """Get the height of the tree."""
        return self._get_height_recursive(self.root)
    
    def _get_height_recursive(self, node):
        """Recursively calculate tree height."""
        if node == self.NIL:
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
            
        Time Complexity: O(log n + m) - balanced tree with m results
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
        if node == self.NIL:
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
            
        Time Complexity: O(log n + m) best case for rating filter, O(n) overall
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
        """String representation of the Red-Black Tree."""
        return f"RedBlackTree(size={self.size}, height={self.get_height()}, balanced=True)"
