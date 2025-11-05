#!/usr/bin/env python3
"""
Quick start script for the frontend application.
This script checks prerequisites and starts the Flask server.
"""

import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    required = ['flask', 'flask_cors', 'pandas', 'numpy']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("ERROR: Missing required packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    
    return True

def check_cleaned_data():
    """Check if cleaned data files exist."""
    cleaned_dir = Path(__file__).parent / 'data' / 'cleaned'
    required_files = ['airline_cleaned.csv', 'airport_cleaned.csv', 
                      'lounge_cleaned.csv', 'seat_cleaned.csv']
    
    if not cleaned_dir.exists():
        return False
    
    existing_files = [f for f in required_files if (cleaned_dir / f).exists()]
    
    if len(existing_files) < len(required_files):
        return False
    
    return True

def check_data_structures():
    """Check if data structures have been built."""
    trees_dir = Path(__file__).parent / 'data' / 'trees'
    
    if not trees_dir.exists():
        print("WARNING: Data structures directory not found.")
        return False
    
    # Check for at least one tree file
    tree_files = list(trees_dir.glob('*.pkl'))
    if not tree_files:
        print("WARNING: No tree files found. Building data structures...")
        return False
    
    print(f"Found {len(tree_files)} tree files")
    return True

def build_data_structures():
    """Build required data structures."""
    print("\n" + "=" * 80)
    print("Building Data Structures")
    print("=" * 80)
    
    scripts = [
        ('examples/load_all_datasets.py', 'Rating-based trees'),
        ('src/loaders/load_autocomplete_structures.py', 'Autocomplete structures')
    ]
    
    for script, description in scripts:
        script_path = Path(__file__).parent / script
        if script_path.exists():
            print(f"\nBuilding {description}...")
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    print(f"SUCCESS: {description} built successfully")
                else:
                    print(f"WARNING: Building {description}: {result.stderr[:200]}")
            except subprocess.TimeoutExpired:
                print(f"WARNING: Timeout building {description}")
            except Exception as e:
                print(f"WARNING: Error building {description}: {e}")
        else:
            print(f"WARNING: Script not found: {script}")

def main():
    """Main function."""
    print("=" * 80)
    print("Frontend Application Startup")
    print("=" * 80)
    
    # Check dependencies
    print("\n[1] Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("SUCCESS: All dependencies installed")
    
    # Check cleaned data
    print("\n[2] Checking cleaned data files...")
    if not check_cleaned_data():
        print("ERROR: Cleaned data files not found!")
        print("\nYou need to clean the raw data first:")
        print("   1. Place raw CSV files (airline.csv, airport.csv, etc.) in data/ directory")
        print("   2. Run: python EDA/clean_data.py")
        print("\n   See README.md for detailed instructions.")
        sys.exit(1)
    print("SUCCESS: Cleaned data files found")
    
    # Check data structures
    print("\n[3] Checking data structures...")
    if not check_data_structures():
        print("\nWARNING: Building data structures (this may take a few minutes)...")
        build_data_structures()
    
    # Start Flask server
    print("\n[4] Starting Flask server...")
    print("=" * 80)
    
    # Check for available port
    import socket
    
    def find_free_port(start_port=3000, max_attempts=10):
        """Find a free port starting from start_port."""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('127.0.0.1', port))
                    return port
            except OSError:
                continue
        return None
    
    port = find_free_port(3000)
    
    if port is None:
        print("ERROR: Could not find an available port in range 3000-3009")
        print("\nSolutions:")
        print("   1. Close other applications using these ports")
        print("   2. Check if another Flask/Python server is running")
        print("   3. On Windows, run as administrator")
        print("   4. Manually specify a port: python src/api/app.py")
        sys.exit(1)
    
    if port != 3000:
        print(f"WARNING: Port 3000 is in use, using port {port} instead")
    
    print(f"\nFrontend will be available at: http://localhost:{port}")
    print(f"API endpoints available at: http://localhost:{port}/api/")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80)
    
    # Import and run Flask app
    try:
        from src.api.app import app
        # Update the port in the app
        app.config['PORT'] = port
        app.run(debug=True, port=port, host='127.0.0.1')
    except KeyboardInterrupt:
        print("\n\nServer stopped. Goodbye!")
    except OSError as e:
        if "Permission denied" in str(e) or "access" in str(e).lower():
            print(f"\nERROR: Cannot bind to port {port}")
            print(f"   Error: {e}")
            print("\nSolutions:")
            print(f"   1. Close other applications using port {port}")
            print("   2. On Windows, try running as administrator")
            print("   3. Check if another Flask server is running")
            print("   4. Try a different port manually:")
            print(f"      python src/api/app.py")
            print("\n   To find what's using the port (Windows):")
            print(f"      netstat -ano | findstr :{port}")
            print("\n   To find what's using the port (Linux/Mac):")
            print(f"      lsof -i :{port}")
        else:
            print(f"\nERROR: Error starting server: {e}")
            import traceback
            traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

