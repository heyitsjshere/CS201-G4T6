"""
AVL Tree (Self-Balancing BST) implementation for storing airline data.
Nodes are ordered by overall_rating with automatic balancing.
"""


class AVLNode:
    """Node in an AVL Tree."""
    
    def __init__(self, rating, data):
        """
        Initialize an AVL node.
        
        Args:
            rating (float): Overall rating used as the key
            data (dict): Complete row data from the dataset
        """
        self.rating = rating
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """AVL Tree (self-balancing BST) for storing records ordered by rating."""
    
    def __init__(self):
        """Initialize an empty AVL Tree."""
        self.root = None
        self.size = 0
    
    def _get_height(self, node):
        """Get height of a node."""
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node):
        """Get balance factor of a node."""
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _rotate_right(self, y):
        """Perform right rotation."""
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        
        return x
    
    def _rotate_left(self, x):
        """Perform left rotation."""
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y
    
    def insert(self, rating, data):
        """
        Insert a new node into the AVL Tree.
        
        Args:
            rating (float): Overall rating (key)
            data (dict): Complete row data
        """
        self.root = self._insert_recursive(self.root, rating, data)
        self.size += 1
    
    def _insert_recursive(self, node, rating, data):
        """Recursively insert and balance."""
        # Standard BST insertion
        if node is None:
            return AVLNode(rating, data)
        
        if rating <= node.rating:
            node.left = self._insert_recursive(node.left, rating, data)
        else:
            node.right = self._insert_recursive(node.right, rating, data)
        
        # Update height
        node.height = 1 + max(self._get_height(node.left), 
                             self._get_height(node.right))
        
        # Get balance factor
        balance = self._get_balance(node)
        
        # Left-Left Case
        if balance > 1 and rating <= node.left.rating:
            return self._rotate_right(node)
        
        # Right-Right Case
        if balance < -1 and rating > node.right.rating:
            return self._rotate_left(node)
        
        # Left-Right Case
        if balance > 1 and rating > node.left.rating:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right-Left Case
        if balance < -1 and rating <= node.right.rating:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
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
        return self._get_height(self.root)
    
    def get_size(self):
        """Get the number of nodes in the tree."""
        return self.size
    
    def __str__(self):
        """String representation of the AVL Tree."""
        return f"AVLTree(size={self.size}, height={self.get_height()}, balanced=True)"
