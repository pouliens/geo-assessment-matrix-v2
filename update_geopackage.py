#!/usr/bin/env python3
"""
Update OGC-compliant GeoPackage from CSV files
===============================================

This script updates the GeoPackage when CSV files are modified while
maintaining full OGC GeoPackage specification compliance. It ensures all
required metadata tables are present and properly configured.

The script will:
1. Verify GeoPackage compliance (application_id, metadata tables)
2. Update data tables from CSV files
3. Register updated tables in gpkg_contents
4. Maintain timestamps and metadata

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

def ensure_geopackage_compliance(conn):
    """Ensure GeoPackage has all required metadata tables."""

    # Set the GeoPackage application_id (required for valid GeoPackage)
    # 0x47503130 = 'GP10' in ASCII (GeoPackage version 1.0)
    conn.execute('PRAGMA application_id = 0x47503130')

    # Create gpkg_spatial_ref_sys if missing
    conn.execute('''
        CREATE TABLE IF NOT EXISTS gpkg_spatial_ref_sys (
            srs_name TEXT NOT NULL,
            srs_id INTEGER NOT NULL PRIMARY KEY,
            organization TEXT NOT NULL,
            organization_coordsys_id INTEGER NOT NULL,
            definition TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Add default spatial reference systems (required by GeoPackage spec)
    conn.execute('''
        INSERT OR IGNORE INTO gpkg_spatial_ref_sys
        (srs_name, srs_id, organization, organization_coordsys_id, definition, description)
        VALUES
        ('Undefined cartesian SRS', -1, 'NONE', -1, 'undefined', 'undefined cartesian coordinate reference system'),
        ('Undefined geographic SRS', 0, 'NONE', 0, 'undefined', 'undefined geographic coordinate reference system'),
        ('WGS 84 geodetic', 4326, 'EPSG', 4326, 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]', 'longitude/latitude coordinates in decimal degrees on the WGS 84 spheroid')
    ''')

    # Create gpkg_contents if missing
    conn.execute('''
        CREATE TABLE IF NOT EXISTS gpkg_contents (
            table_name TEXT NOT NULL PRIMARY KEY,
            data_type TEXT NOT NULL,
            identifier TEXT UNIQUE,
            description TEXT DEFAULT '',
            last_change DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
            min_x REAL,
            min_y REAL,
            max_x REAL,
            max_y REAL,
            srs_id INTEGER,
            CONSTRAINT fk_gc_r_srs_id FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys(srs_id)
        )
    ''')

    # Create gpkg_geometry_columns if missing (optional but good for compliance)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS gpkg_geometry_columns (
            table_name TEXT NOT NULL,
            column_name TEXT NOT NULL,
            geometry_type_name TEXT NOT NULL,
            srs_id INTEGER NOT NULL,
            z TINYINT NOT NULL,
            m TINYINT NOT NULL,
            CONSTRAINT pk_geom_cols PRIMARY KEY (table_name, column_name),
            CONSTRAINT fk_gc_tn FOREIGN KEY (table_name) REFERENCES gpkg_contents(table_name),
            CONSTRAINT fk_gc_srs FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys(srs_id)
        )
    ''')

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

            # Ensure GeoPackage has all required metadata tables
            print("Ensuring GeoPackage compliance...")
            ensure_geopackage_compliance(conn)
            
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

                # Ensure table is registered in gpkg_contents
                conn.execute('''
                    INSERT OR REPLACE INTO gpkg_contents
                    (table_name, data_type, identifier, description, last_change)
                    VALUES (?, 'attributes', ?, ?, datetime('now','localtime'))
                ''', (table_name, table_name, f'EGDI {table_name.replace("_", " ").title()}'))
            
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