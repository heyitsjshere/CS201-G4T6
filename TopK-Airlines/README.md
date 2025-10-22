# TopK-Airlines Project

## Overview
The TopK-Airlines project is designed to experiment with various data structures and algorithms to efficiently maintain and retrieve the top-K airlines based on average ratings. This project aims to provide insights into the performance of different data structures when handling dynamic data.

## Project Structure
```
TopK-Airlines
├── src
│   ├── data_structures
│   ├── algorithms
│   └── utils
├── experiments
├── tests
├── data
└── results
```

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/TopK-Airlines.git
   cd TopK-Airlines
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running Experiments
To run the experiments, execute the following command:
```bash
python -m experiments.run_experiments
```
This will load the sample data, perform operations on the data structures, and save the results to `results/results.csv`.

## Guidelines
- Ensure that the data files are placed in the `data` directory.
- Modify the `run_experiments.py` script to customize the experiments as needed.
- Use the `tests` directory to add and run unit tests for your implementations.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.