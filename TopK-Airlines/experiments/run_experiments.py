# Contents of /TopK-Airlines/TopK-Airlines/experiments/run_experiments.py

import pandas as pd
import numpy as np
from src.utils.data_loader import load_data
from src.data_structures.heap import Heap
from src.data_structures.priority_queue import PriorityQueue
from src.data_structures.hash_table import HashTable
from src.algorithms.topk import TopK

def main():
    # Load sample data
    data = load_data('data/skytrax_sample.csv')
    
    # Initialize data structures
    heap = Heap()
    priority_queue = PriorityQueue()
    hash_table = HashTable()
    top_k = TopK()

    # Placeholder for experiment results
    results = []

    # Randomly insert and delete airlines from the data structures
    for airline in data['airline']:
        # Example operations
        heap.insert(airline)
        priority_queue.enqueue(airline)
        hash_table.insert(airline, data['rating'].iloc[0])  # Assuming rating is available

        # Measure time for operations (placeholder)
        # Here you would implement timing logic for each operation

    # Write results to CSV
    results_df = pd.DataFrame(results, columns=['Operation', 'Time'])
    results_df.to_csv('results/results.csv', index=False)

if __name__ == "__main__":
    main()