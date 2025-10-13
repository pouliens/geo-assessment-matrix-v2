#!/usr/bin/env python3
"""
Convert CSV files to GeoPackage for EGDI Geo-Assessment Matrix
============================================================

This script converts the three CSV data files into a single GeoPackage file:
- geological_data.csv -> geological_features table
- reference-geological-constraints.csv -> geological_constraints table  
- reference-engineering-constraints.csv -> engineering_constraints table

The GeoPackage file will be created at: data/geological_data.gpkg
"""

import sqlite3
import pandas as pd
import sys
from pathlib import Path

# Configuration constants
DATA_DIR = "data"
GEOPACKAGE_PATH = f"{DATA_DIR}/geological_data.gpkg"
CSV_FILES = {
    'geological_features': f'{DATA_DIR}/geological_data.csv',
    'geological_constraints': f'{DATA_DIR}/reference-geological-constraints.csv', 
    'engineering_constraints': f'{DATA_DIR}/reference-engineering-constraints.csv'
}
CONSTRAINT_HEADER_ROWS = 0  # Constraint CSVs now have simple structure: header in row 1, data from row 2

def try_read_csv_with_encodings(file_path, encodings=['utf-8', 'latin-1', 'cp1252', 'iso-8859-1'], skiprows=None, nrows=None, header='infer'):
    """Try to read CSV with multiple encodings."""
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding, skiprows=skiprows, nrows=nrows, header=header)
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading {file_path} with {encoding}: {e}")
            continue
    
    raise ValueError(f"Could not read {file_path} with any supported encoding")

def create_geopackage():
    """Create GeoPackage from CSV files."""
    
    # Check if CSV files exist
    for table_name, file_path in CSV_FILES.items():
        if not Path(file_path).exists():
            print(f"ERROR: {file_path} not found!")
            return False
    
    # Create GeoPackage
    try:
        # Remove existing GeoPackage if it exists
        if Path(GEOPACKAGE_PATH).exists():
            Path(GEOPACKAGE_PATH).unlink()
            print(f"Removed existing {GEOPACKAGE_PATH}")
        
        # Connect to new GeoPackage
        with sqlite3.connect(GEOPACKAGE_PATH) as conn:
            
            # Convert each CSV file to a table
            for table_name, file_path in CSV_FILES.items():
                print(f"Converting {file_path} to {table_name} table...")
                
                # Read CSV with encoding handling
                # All CSV files now have simple structure: header in row 1, data from row 2
                df = try_read_csv_with_encodings(file_path)
                
                # Clean column names (remove BOM, spaces, etc.)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                
                # Write to SQLite table
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                
                print(f"  + Added {len(df)} rows to {table_name}")
                print(f"  + Columns: {list(df.columns)[:5]}..." if len(df.columns) > 5 else f"  + Columns: {list(df.columns)}")
            
            # Add GeoPackage metadata tables for compatibility
            conn.execute('''
                CREATE TABLE IF NOT EXISTS gpkg_contents (
                    table_name TEXT NOT NULL PRIMARY KEY,
                    data_type TEXT NOT NULL,
                    identifier TEXT,
                    description TEXT,
                    last_change DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
                    min_x REAL,
                    min_y REAL,
                    max_x REAL,
                    max_y REAL,
                    srs_id INTEGER
                )
            ''')
            
            # Register our tables in gpkg_contents
            for table_name in CSV_FILES.keys():
                conn.execute('''
                    INSERT OR REPLACE INTO gpkg_contents 
                    (table_name, data_type, identifier, description)
                    VALUES (?, 'attributes', ?, ?)
                ''', (table_name, table_name, f'EGDI {table_name.replace("_", " ").title()}'))
            
            conn.commit()
        
        print(f"\n[SUCCESS] Successfully created {GEOPACKAGE_PATH}")
        print(f"   Tables: {', '.join(CSV_FILES.keys())}")
        
        # Verify the GeoPackage
        print("\n[INFO] Verifying GeoPackage contents:")
        verify_geopackage(GEOPACKAGE_PATH)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating GeoPackage: {e}")
        return False

def verify_geopackage(gpkg_path):
    """Verify GeoPackage contents."""
    try:
        with sqlite3.connect(gpkg_path) as conn:
            # List all tables
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            print(f"   All tables: {[t[0] for t in tables]}")
            
            # Check each data table
            for table_name in ['geological_features', 'geological_constraints', 'engineering_constraints']:
                count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
                print(f"   {table_name}: {count} rows, {len(columns)} columns")
        
    except Exception as e:
        print(f"[ERROR] Error verifying GeoPackage: {e}")

if __name__ == "__main__":
    print("EGDI Geo-Assessment Matrix - CSV to GeoPackage Converter")
    print("=" * 60)
    
    if create_geopackage():
        print("\n[SUCCESS] Conversion completed successfully!")
        print("\nNext steps:")
        print("1. Update matrix.py to use the GeoPackage")
        print("2. Test the application")
        print("3. Remove old CSV files if everything works")
    else:
        print("\n[FAILED] Conversion failed!")
        sys.exit(1)