# EGDI Geo-Assessment Matrix

## Overview
Streamlit application for comparing geological features in offshore wind development. Compares two features side-by-side with constraints analysis and foundation recommendations.

## Key Features
- Compare 86+ geological features
- Interactive constraint visualization
- Foundation assessment for 4 foundation types
- Professional UI with responsive design

## Architecture

### Files
- `matrix.py` - Main Streamlit application
- `data/geological_data.gpkg` - Single GeoPackage containing all geological data
- `create_geopackage.py` - Convert CSV files to GeoPackage
- `update_geopackage.py` - Update GeoPackage from CSV files
- `Dockerfile` - Container deployment

### Data Integration
Single GeoPackage (SQLite-based) containing three tables:
- `geological_features` - Master feature database
- `geological_constraints` - Complete definitions & geological constraints  
- `engineering_constraints` - Engineering constraints

## Critical Requirements

**Feature Name Consistency**: Names must be identical across all three data tables.

### Adding/Updating Features
**Option 1: CSV Workflow (Traditional)**
1. Update `geological_data.csv` first (master reference)
2. Update both constraint CSV files with identical names
3. Run `python update_geopackage.py` to sync GeoPackage
4. Test constraint loading

**Option 2: Direct Database Updates**
1. Connect to `data/geological_data.gpkg` with SQLite tools
2. Update tables directly with SQL
3. Ensure exact character matching (case-sensitive)

## Development

### Setup
```bash
uv venv
source .venv/Scripts/activate  # Windows
uv pip install -r requirements.txt
streamlit run matrix.py
```

### Docker
```bash
# Local development
docker build -t geo-matrix .
docker run -p 8501:80 geo-matrix

# Production deployment
# Uses GitLab CI/CD pipeline with Kubernetes
# Runs on port 80 inside container
# Access via: http://project-name-id-branch.kube-idev.bgslcdevops.test/
```

### Testing
- Verify constraint pills display correctly
- Test encoding with special characters
- Check foundation assessments load properly

## Data Structure

### geological_features table (Master)
- `Geological_Feature` - Feature names
- `Setting`, `Process`, `Constraint_Type`, `Dominant_Constraint`
- `*_Assessment` - Foundation constraint levels
- `Definition`, `Comments`

### Constraint Tables
- Feature names in first column
- Constraint indicators marked with 'x'
- Complete definitions with citations
- `geological_constraints` - Geological constraint matrix
- `engineering_constraints` - Engineering constraint matrix

## Common Issues
- **Missing Constraints**: 46 features have mismatched names between main CSV and constraint CSVs
- **Case Sensitivity**: Names must match exactly
- **GeoPackage Sync**: Remember to run `update_geopackage.py` after CSV changes
- **Data Inconsistency**: Constraint files have 72 features vs 86 in main file (known issue)

## Performance
- `@st.cache_data` decorators for data loading
- Single GeoPackage file for faster queries
- SQLite-based data access
- CSS optimizations for smooth interactions

## Migration Notes
- Migrated from CSV files to single GeoPackage (2024)
- CSV files maintained for data editing workflow
- Use `create_geopackage.py` for fresh conversion
- Use `update_geopackage.py` for incremental updates