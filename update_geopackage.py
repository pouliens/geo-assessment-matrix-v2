#!/usr/bin/env python3
"""
Update GeoPackage from CSV files
===============================

This script updates the GeoPackage when CSV files are modified.
Useful for maintaining data updates workflow.

Usage:
    python update_geopackage.py
"""

import sqlite3
import pandas as pd
from pathlib import Path
import sys

# Configuration constants
DATA_DIR = "data"
GEOPACKAGE_PATH = f"{DATA_DIR}/geological_data.gpkg"
CSV_FILES = {
    'geological_features': f'{DATA_DIR}/geological_data.csv',
    'geological_constraints': f'{DATA_DIR}/reference-geological-constraints.csv', 
    'engineering_constraints': f'{DATA_DIR}/reference-engineering-constraints.csv'
}
CONSTRAINT_HEADER_ROWS = 0  # Constraint CSVs now have simple structure: header in row 1, data from row 2

def update_geopackage_from_csvs():
    """Update existing GeoPackage with latest CSV data."""
    
    # Check if GeoPackage exists
    if not Path(GEOPACKAGE_PATH).exists():
        print(f"[ERROR] {GEOPACKAGE_PATH} not found!")
        print("Run create_geopackage.py first to create the initial GeoPackage.")
        return False
    
    # Check if CSV files exist
    for table_name, file_path in CSV_FILES.items():
        if not Path(file_path).exists():
            print(f"[ERROR] {file_path} not found!")
            return False
    
    try:
        # Connect to GeoPackage
        with sqlite3.connect(GEOPACKAGE_PATH) as conn:
            
            # Update each table
            for table_name, file_path in CSV_FILES.items():
                print(f"Updating {table_name} from {file_path}...")
                
                # Read CSV with encoding handling
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                df = None
                
                for encoding in encodings:
                    try:
                        # All CSV files now have simple structure: header in row 1, data from row 2
                        df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                
                if df is None:
                    print(f"[ERROR] Could not read {file_path} with any supported encoding")
                    continue
                
                # Clean column names
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                
                # Replace table data
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                
                print(f"  + Updated {len(df)} rows in {table_name}")
            
            # Update timestamp in gpkg_contents
            conn.execute('''
                UPDATE gpkg_contents 
                SET last_change = datetime('now','localtime')
                WHERE data_type = 'attributes'
            ''')
            
            conn.commit()
        
        print(f"\n[SUCCESS] GeoPackage updated successfully!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to update GeoPackage: {e}")
        return False

if __name__ == "__main__":
    print("EGDI Geo-Assessment Matrix - GeoPackage Updater")
    print("=" * 50)
    
    if update_geopackage_from_csvs():
        print("\n[INFO] You can now restart your Streamlit app to see the changes.")
    else:
        print("\n[FAILED] Update failed!")
        sys.exit(1)