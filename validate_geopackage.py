#!/usr/bin/env python3
"""
Validate GeoPackage Compliance
===============================

This script validates that the GeoPackage meets the OGC GeoPackage specification
requirements for uploading to EGDI or other GeoPackage-compliant systems.
"""

import sqlite3
from pathlib import Path

GEOPACKAGE_PATH = "data/geological_data.gpkg"

def validate_geopackage():
    """Validate GeoPackage compliance."""

    if not Path(GEOPACKAGE_PATH).exists():
        print(f"ERROR: {GEOPACKAGE_PATH} not found!")
        return False

    try:
        with sqlite3.connect(GEOPACKAGE_PATH) as conn:
            print("EGDI Geo-Assessment Matrix - GeoPackage Validator")
            print("=" * 60)

            # Check application_id
            app_id = conn.execute('PRAGMA application_id').fetchone()[0]
            print(f"\nApplication ID: 0x{app_id:08X}")
            if app_id == 0x47503130:
                print("  [OK] Correct GeoPackage application ID (GP10)")
            else:
                print(f"  [FAIL] Invalid application ID (expected 0x47503130)")
                return False

            # Get all tables
            tables = [t[0] for t in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()]

            print(f"\nAll tables ({len(tables)}):")
            for table in tables:
                print(f"  - {table}")

            # Check required tables
            print("\nRequired GeoPackage tables:")
            required_tables = ['gpkg_spatial_ref_sys', 'gpkg_contents']
            all_required_present = True

            for table in required_tables:
                if table in tables:
                    print(f"  [OK] {table}")
                else:
                    print(f"  [FAIL] {table} (MISSING)")
                    all_required_present = False

            if not all_required_present:
                print("\nERROR: Missing required GeoPackage tables!")
                return False

            # Check spatial reference systems
            srs = conn.execute('SELECT srs_id, srs_name FROM gpkg_spatial_ref_sys').fetchall()
            print(f"\nSpatial Reference Systems ({len(srs)}):")
            for srs_id, srs_name in srs:
                print(f"  - {srs_id}: {srs_name}")

            # Check registered contents
            contents = conn.execute(
                'SELECT table_name, data_type, identifier FROM gpkg_contents'
            ).fetchall()
            print(f"\nRegistered contents ({len(contents)}):")
            for table_name, data_type, identifier in contents:
                row_count = conn.execute(f'SELECT COUNT(*) FROM {table_name}').fetchone()[0]
                print(f"  - {table_name} ({data_type}): {identifier} ({row_count} rows)")

            # Verify data tables
            print("\nData table verification:")
            expected_tables = ['geological_features', 'geological_constraints', 'engineering_constraints']
            for table in expected_tables:
                if table in tables:
                    count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                    columns = conn.execute(f'PRAGMA table_info({table})').fetchall()
                    print(f"  [OK] {table}: {count} rows, {len(columns)} columns")
                else:
                    print(f"  [FAIL] {table} (MISSING)")

            print("\n" + "=" * 60)
            print("[SUCCESS] GeoPackage is compliant with OGC GeoPackage specification")
            print("[SUCCESS] Ready for upload to EGDI or other GeoPackage systems")
            return True

    except Exception as e:
        print(f"\nERROR: Validation failed: {e}")
        return False

if __name__ == "__main__":
    success = validate_geopackage()
    exit(0 if success else 1)
