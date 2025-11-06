"""
Flask API for frontend data structure comparison interface.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
from pathlib import Path
import time
import json
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_cleaned_data
from utils.tree_persistence import load_trees
from data_structures.string_trie import StringTrie
from data_structures.ternary_search_tree import TernarySearchTree
from data_structures.sorted_array import SortedArray
from algorithms.sorting import SortingAlgorithms

app = Flask(__name__, static_folder='../../frontend', static_url_path='')
CORS(app)

# Global cache for loaded data structures
# Note: These are cleared on server restart
_loaded_trees = {}
_loaded_autocomplete = {}
_sorting_algo = SortingAlgorithms()


def get_name_field(dataset_name):
    """Get the name field for a dataset."""
    field_map = {
        'airline': 'airline_name',
        'airport': 'airport_name',
        'lounge': 'lounge_name',
        'seat': 'airline_name'
    }
    return field_map.get(dataset_name, 'name')


def load_dataset_trees(dataset_name):
    """Load trees for a dataset (lazy loading)."""
    if dataset_name not in _loaded_trees:
        try:
            trees = load_trees(dataset_name)
            _loaded_trees[dataset_name] = trees
        except Exception as e:
            print(f"Error loading trees for {dataset_name}: {e}")
            return None
    return _loaded_trees[dataset_name]


def load_autocomplete_structures(dataset_name):
    """Load autocomplete structures for a dataset (lazy loading)."""
    if dataset_name not in _loaded_autocomplete:
        try:
            # Try to load from saved structures
            autocomplete = load_trees(f"{dataset_name}_autocomplete")
            _loaded_autocomplete[dataset_name] = autocomplete
        except:
            # Build on the fly if not saved
            try:
                from loaders.load_autocomplete_structures import load_autocomplete_structures
                structures, _ = load_autocomplete_structures(dataset_name)
                _loaded_autocomplete[dataset_name] = structures
            except Exception as e:
                print(f"Error loading autocomplete for {dataset_name}: {e}")
                return None
    return _loaded_autocomplete[dataset_name]


@app.route('/')
def index():
    """Serve the frontend."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    """Get list of available datasets."""
    return jsonify({
        'datasets': ['airline', 'airport', 'lounge', 'seat'],
        'success': True
    })


@app.route('/api/autocomplete', methods=['POST'])
def autocomplete():
    """Autocomplete endpoint."""
    data = request.json
    prefix = data.get('prefix', '')
    dataset = data.get('dataset', 'airline')
    structure_type = data.get('structure', 'Trie')
    max_results = data.get('max_results', 10)
    
    if not prefix:
        return jsonify({
            'results': [],
            'metrics': {
                'time_ms': 0,
                'comparisons': 0,
                'memory_bytes': 0,
                'results_count': 0
            },
            'success': True
        })
    
    # Load autocomplete structures
    structures = load_autocomplete_structures(dataset)
    if not structures:
        return jsonify({
            'error': f'Autocomplete structures not available for {dataset}',
            'success': False
        }), 404
    
    # Get the requested structure
    if structure_type not in structures:
        return jsonify({
            'error': f'Structure {structure_type} not available',
            'success': False
        }), 404
    
    structure = structures[structure_type]
    
    # Perform search - fetch all results (no limit for autocomplete)
    # We'll deduplicate by name below to get unique items
    # Use a very high limit to effectively get all results
    search_max_results = 100000  # High enough to get all records
    results, metrics = structure.search_prefix(prefix, search_max_results)
    
    # Extract name field for display
    name_field = get_name_field(dataset)
    formatted_results = []
    name_to_ratings = {}  # Track all ratings for each name to calculate average
    
    # Collect all results and group by name
    for result in results:
        name = result.get(name_field, '')
        # Normalize name for comparison (lowercase, strip)
        normalized_name = name.lower().strip() if name else ''
        
        if normalized_name:
            rating = result.get('overall_rating', 0)
            # Ensure rating is a float
            try:
                rating = float(rating) if rating else 0.0
            except (ValueError, TypeError):
                rating = 0.0
            
            if normalized_name not in name_to_ratings:
                name_to_ratings[normalized_name] = {
                    'original_name': name,  # Keep original casing for display
                    'ratings': [],
                    'first_data': result  # Keep first record's data
                }
            if rating > 0:  # Only add valid ratings
                name_to_ratings[normalized_name]['ratings'].append(rating)
    
    # Calculate average rating for each unique name
    for normalized_name, info in name_to_ratings.items():
        ratings = info['ratings']
        if ratings:
            # Ensure we use float division to preserve decimals
            avg_rating = float(sum(ratings)) / float(len(ratings))
        else:
            avg_rating = 0.0
        
        formatted_results.append({
            'name': info['original_name'],
            'rating': round(avg_rating, 2),  # Average rating rounded to 2 decimals
            'data': info['first_data']
        })
    
    return jsonify({
        'results': formatted_results,
        'metrics': metrics,
        'success': True
    })


@app.route('/api/autocomplete/search', methods=['POST'])
def autocomplete_search():
    """Search for all rows matching a specific name (after autocomplete selection)."""
    data = request.json
    search_name = data.get('name', '')
    dataset = data.get('dataset', 'airline')
    structure_type = data.get('structure', 'Trie')
    
    if not search_name:
        return jsonify({
            'results': [],
            'metrics': {
                'time_ms': 0,
                'comparisons': 0,
                'memory_bytes': 0,
                'results_count': 0
            },
            'success': True
        })
    
    import time
    start_time = time.perf_counter()
    
    # Load autocomplete structures
    structures = load_autocomplete_structures(dataset)
    if not structures:
        return jsonify({
            'error': f'Autocomplete structures not available for {dataset}',
            'success': False
        }), 404
    
    # Get the requested structure
    if structure_type not in structures:
        return jsonify({
            'error': f'Structure {structure_type} not available',
            'success': False
        }), 404
    
    structure = structures[structure_type]
    
    # Search for exact name match - get all results matching the name
    # We'll search for the exact name as a prefix to get all records
    search_max_results = 100000
    results, metrics = structure.search_prefix(search_name.lower().strip(), search_max_results)
    
    # Filter to exact name match (case-insensitive)
    name_field = get_name_field(dataset)
    exact_matches = []
    for result in results:
        result_name = result.get(name_field, '')
        if result_name.lower().strip() == search_name.lower().strip():
            exact_matches.append(result)
    
    elapsed = (time.perf_counter() - start_time) * 1000
    
    return jsonify({
        'results': exact_matches,
        'metrics': {
            'time_ms': elapsed,
            'comparisons': metrics.get('comparisons', 0),
            'memory_bytes': metrics.get('memory_bytes', 0),
            'results_count': len(exact_matches)
        },
        'success': True
    })


@app.route('/api/filter', methods=['POST'])
def filter_by_rating():
    """Filter by rating endpoint."""
    # Start timing immediately to capture all overhead (loading, processing, serialization)
    start_time = time.perf_counter()
    
    try:
        data = request.json
        if not data:
            elapsed = (time.perf_counter() - start_time) * 1000
            return jsonify({
                'error': 'No data provided',
                'success': False,
                'metrics': {
                    'time_ms': elapsed,
                    'comparisons': 0,
                    'memory_bytes': 0,
                    'results_count': 0
                }
            }), 400
            
        dataset = data.get('dataset', 'airline')
        min_rating = data.get('min_rating', 0.0)
        max_rating = data.get('max_rating', 10.0)
        structure_type = data.get('structure', 'AVL')
        limit = data.get('limit', None)  # Optional limit
        
        # Load trees (this may take time if not already loaded)
        trees = load_dataset_trees(dataset)
        if not trees:
            elapsed = (time.perf_counter() - start_time) * 1000
            return jsonify({
                'error': f'Trees not available for {dataset}',
                'success': False,
                'metrics': {
                    'time_ms': elapsed,
                    'comparisons': 0,
                    'memory_bytes': 0,
                    'results_count': 0
                }
            }), 404
        
        # Map structure names
        structure_map = {
            'AVL': 'AVL',
            'Red-Black': 'Red-Black',
            'BST': 'BST',
            'Trie': 'Trie',
            'HashMap': 'HashMap'
        }
        
        actual_structure_name = structure_map.get(structure_type, structure_type)
        if actual_structure_name not in trees:
            elapsed = (time.perf_counter() - start_time) * 1000
            return jsonify({
                'error': f'Structure {structure_type} not available. Available structures: {list(trees.keys())}',
                'success': False,
                'metrics': {
                    'time_ms': elapsed,
                    'comparisons': 0,
                    'memory_bytes': 0,
                    'results_count': 0
                }
            }), 404
        
        tree = trees[actual_structure_name]
        
        # Perform range query with comparison tracking
        comparisons = 0
        
        # Create a wrapper to track comparisons
        class ComparisonTracker:
            def __init__(self):
                self.count = 0
            
            def add(self, n=1):
                self.count += n
        
        tracker = ComparisonTracker()
        
        # Monkey-patch comparison tracking for range search
        original_range_search = None
        if hasattr(tree, '_range_search'):
            original_range_search = tree._range_search
            
            # Check if tree uses NIL sentinel (Red-Black tree) or None (AVL/BST)
            uses_nil = hasattr(tree, 'NIL')
            
            def tracked_range_search(node, min_rating, max_rating, results):
                # Handle both NIL sentinel (Red-Black) and None (AVL/BST)
                if uses_nil:
                    if node == tree.NIL:
                        return
                else:
                    if node is None:
                        return
                
                tracker.add(1)
                if min_rating < node.rating:
                    tracked_range_search(node.left, min_rating, max_rating, results)
                if min_rating <= node.rating <= max_rating:
                    results.append(node.data)
                    tracker.add(1)
                if max_rating > node.rating:
                    tracked_range_search(node.right, min_rating, max_rating, results)
            
            # Temporarily replace method
            tree._range_search = tracked_range_search
        
        # Perform query
        # HashMap doesn't have _range_search, so skip monkey-patching for it
        if structure_type == 'HashMap':
            # HashMap uses filter_by_rating directly, which tracks comparisons internally
            # Reset comparisons before query to get accurate count for this query only
            if hasattr(tree, 'reset_comparisons'):
                tree.reset_comparisons()
            if hasattr(tree, 'filter_by_rating'):
                results = tree.filter_by_rating(min_rating, max_rating)
                # Get comparisons from HashMap's internal counter
                comparisons = tree.get_total_comparisons() if hasattr(tree, 'get_total_comparisons') else len(results) * 2
            else:
                results = []
        elif hasattr(tree, 'get_range'):
            results = tree.get_range(min_rating, max_rating)
        elif hasattr(tree, 'filter_by_rating'):
            results = tree.filter_by_rating(min_rating, max_rating)
        else:
            results = []
        
        # Restore original method
        if original_range_search:
            tree._range_search = original_range_search
        
        # Use tracked comparisons if available, otherwise estimate
        if structure_type != 'HashMap':
            comparisons = tracker.count if tracker.count > 0 else len(results) * 2  # Estimate
        
        # Apply limit if specified (this is part of the processing time)
        if limit and limit > 0:
            results = results[:limit]
        
        # Get memory usage (approximate) - still part of processing
        try:
            from utils.performance_tracker import estimate_memory_usage_tree
            if hasattr(tree, 'root'):
                memory_usage = estimate_memory_usage_tree(tree.root)
            else:
                memory_usage = sys.getsizeof(tree) if hasattr(sys, 'getsizeof') else 0
        except:
            memory_usage = sys.getsizeof(tree) if hasattr(sys, 'getsizeof') else 0
        
        # Calculate elapsed time after all processing (including limit, memory calculation)
        # This captures the full user-perceived time
        elapsed = (time.perf_counter() - start_time) * 1000
        
        return jsonify({
            'results': results,
            'count': len(results),
            'metrics': {
                'time_ms': elapsed,
                'comparisons': comparisons,
                'memory_bytes': memory_usage,
                'results_count': len(results)
            },
            'success': True
        })
    except Exception as e:
        import traceback
        elapsed = (time.perf_counter() - start_time) * 1000
        print(f"Error in filter_by_rating: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'success': False,
            'metrics': {
                'time_ms': elapsed,
                'comparisons': 0,
                'memory_bytes': 0,
                'results_count': 0
            }
        }), 500


@app.route('/api/sort', methods=['POST'])
def sort_data():
    """Sort data endpoint."""
    data = request.json
    dataset = data.get('dataset', 'airline')
    structure_type = data.get('structure', 'AVL')
    sort_algorithm = data.get('algorithm', 'tree_inorder')
    reverse = data.get('reverse', False)
    limit = data.get('limit', 1000)  # Limit results for performance
    
    # Get data to sort
    if sort_algorithm == 'tree_inorder':
        # Use tree structure
        trees = load_dataset_trees(dataset)
        if not trees:
            return jsonify({
                'error': f'Trees not available for {dataset}',
                'success': False
            }), 404
        
        structure_map = {
            'AVL': 'AVL',
            'Red-Black': 'Red-Black',
            'BST': 'BST'
        }
        
        actual_structure_name = structure_map.get(structure_type, structure_type)
        if actual_structure_name not in trees:
            return jsonify({
                'error': f'Structure {structure_type} not available',
                'success': False
            }), 404
        
        tree = trees[actual_structure_name]
        sorted_data, metrics = _sorting_algo.tree_inorder_sort(tree, reverse=reverse)
    else:
        # Load dataset and sort
        df = load_cleaned_data(dataset)
        data_list = df.to_dict('records')
        
        if limit:
            data_list = data_list[:limit]
        
        if sort_algorithm == 'quicksort':
            sorted_data, metrics = _sorting_algo.quicksort(data_list, reverse=reverse)
        elif sort_algorithm == 'mergesort':
            sorted_data, metrics = _sorting_algo.mergesort(data_list, reverse=reverse)
        elif sort_algorithm == 'timsort':
            sorted_data, metrics = _sorting_algo.timsort(data_list, reverse=reverse)
        else:
            return jsonify({
                'error': f'Unknown algorithm: {sort_algorithm}',
                'success': False
            }), 400
    
    # Limit results
    if limit:
        sorted_data = sorted_data[:limit]
    
    return jsonify({
        'results': sorted_data,
        'count': len(sorted_data),
        'metrics': metrics,
        'success': True
    })


@app.route('/api/structure-info', methods=['GET'])
def get_structure_info():
    """Get information about available data structures."""
    dataset = request.args.get('dataset', 'airline')
    
    trees = load_dataset_trees(dataset)
    autocomplete = load_autocomplete_structures(dataset)
    
    info = {
        'dataset': dataset,
        'filter_structures': list(trees.keys()) if trees else [],
        'autocomplete_structures': list(autocomplete.keys()) if autocomplete else [],
        'sort_algorithms': ['tree_inorder', 'quicksort', 'mergesort', 'timsort']
    }
    
    return jsonify(info)


def find_free_port(start_port=3000, max_attempts=10):
    """Find a free port starting from start_port."""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None


if __name__ == '__main__':
    import socket
    import sys
    
    # Try to find an available port
    default_port = 3000
    port = find_free_port(default_port)
    
    if port is None:
        print("ERROR: Could not find an available port in range 3000-3009")
        print("Please close other applications using these ports or manually specify a port.")
        sys.exit(1)
    
    if port != default_port:
        print(f"WARNING: Port {default_port} is in use, using port {port} instead")
    
    print("=" * 80)
    print("Starting Flask API Server")
    print("=" * 80)
    print("\nAvailable endpoints:")
    print("  GET  /api/datasets - List available datasets")
    print("  POST /api/autocomplete - Autocomplete search")
    print("  POST /api/filter - Filter by rating")
    print("  POST /api/sort - Sort data")
    print("  GET  /api/structure-info - Get structure information")
    print(f"\nFrontend: http://localhost:{port}")
    print("=" * 80)
    
    try:
        app.run(debug=True, port=port, host='127.0.0.1', use_reloader=False)
    except OSError as e:
        if "Permission denied" in str(e) or "access" in str(e).lower():
            print(f"\nERROR: Cannot bind to port {port}")
            print(f"   Error: {e}")
            print("\nSolutions:")
            print(f"   1. Close other applications using port {port}")
            print("   2. Run as administrator (Windows)")
            print("   3. Try a different port: python src/api/app.py --port 5001")
            print("   4. Check if another Flask server is running")
        else:
            raise

