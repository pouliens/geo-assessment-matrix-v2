#!/usr/bin/env python3
"""
Convert CSV files to OGC-compliant GeoPackage for EGDI Geo-Assessment Matrix
=============================================================================

This script converts the three CSV data files into a single OGC GeoPackage file
that is fully compliant with the GeoPackage specification and ready for upload
to EGDI or other GeoPackage-compliant systems.

Data conversion:
- geological_data.csv -> geological_features table
- reference-geological-constraints.csv -> geological_constraints table
- reference-engineering-constraints.csv -> engineering_constraints table

The GeoPackage includes all required metadata tables:
- gpkg_spatial_ref_sys: Spatial reference system definitions
- gpkg_contents: Table registry and metadata
- gpkg_geometry_columns: Geometry column metadata (optional)

Output: data/geological_data.gpkg

Usage:
    python create_geopackage.py
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

            # Set the GeoPackage application_id (required for valid GeoPackage)
            # 0x47503130 = 'GP10' in ASCII (GeoPackage version 1.0)
            conn.execute('PRAGMA application_id = 0x47503130')

            # Create required GeoPackage metadata tables
            # 1. gpkg_spatial_ref_sys - required even for non-spatial data
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

            # 2. gpkg_contents - required table listing all data tables
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

            # 3. gpkg_geometry_columns - optional but good to have for compliance
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

            # Register our tables in gpkg_contents (attributes, not features)
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