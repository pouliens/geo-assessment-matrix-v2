# EGDI Geo-Assessment Matrix

## Overview
Streamlit application for comparing geological features in offshore wind development. Compares two features side-by-side with constraints analysis and foundation recommendations.

The application uses a simplified data architecture with a single CSV file (`geological_data.csv`) as the source of truth, converted to a GeoPackage for efficient querying.

## Key Features
- Compare 86 geological features side-by-side
- Interactive constraint visualization (geological and engineering)
- Foundation assessment for 4 foundation types (Piles, Suction Caisson, GBS, Cables)
- Professional UI with dark mode support
- Academic references displayed separately for clean definitions

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
**Recommended Workflow (CSV-based)**
1. Update `data/geological_data.csv` - the master data source with all feature details
2. (Optional) Update constraint CSV files: `reference-geological-constraints.csv` and `reference-engineering-constraints.csv`
3. Regenerate GeoPackage: `python create_geopackage.py`
4. Test the application: `streamlit run matrix.py`

**Alternative: Direct Database Updates**
1. Connect to `data/geological_data.gpkg` with SQLite tools (e.g., DB Browser for SQLite)
2. Update tables directly with SQL
3. Ensure exact name matching (case-sensitive) across all tables

**Best Practices**
- Keep feature names consistent across all data sources
- Use the `References` column for academic citations (cleaner than inline citations)
- Test locally before deploying
- The `geological_data.csv` file is the single source of truth for feature data

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
Contains 86 geological features with the following columns:
- `Geological_Feature` - Unique feature name (primary identifier)
- `Setting` - Geological setting (e.g., Sediments, Glacial, Marine, Coastal, Solid Earth)
- `Constraint_Type` - Type of constraint (e.g., Lithology, Relief, Structure, Geohazard)
- `Definition` - Detailed description of the geological feature
- `Piles_Assessment` - Constraint level for pile foundations
- `Suction_Caisson_Assessment` - Constraint level for suction caisson foundations
- `GBS_Assessment` - Constraint level for gravity-based structures
- `Cables_Assessment` - Constraint level for cables
- `Dominant_Constraint` - Primary engineering constraint for this feature
- `Comments` - Engineering guidance and practical considerations
- `References` - Academic references and citations

**Note**: The `Process` column has been removed to simplify the data structure.

### Constraint Tables
- Feature names in first column (must match `geological_features` exactly)
- Constraint indicators marked with 'x'
- `geological_constraints` - Geological constraint matrix (86 features)
- `engineering_constraints` - Engineering constraint matrix (86 features)

**Important**: All three tables contain the same 86 geological features with consistent naming.

## Common Issues
- **Case Sensitivity**: Feature names must match exactly across all tables
- **GeoPackage Sync**: Always run `python create_geopackage.py` or `python update_geopackage.py` after CSV changes
- **Character Encoding**: CSV files should use UTF-8 encoding (latin-1 fallback supported)

## Code Quality & Best Practices

### Python & Streamlit Standards
- **Type Hints**: All functions include type hints for parameters and return values
- **Docstrings**: Comprehensive docstrings following Google style for all functions
- **Configuration**: Constants defined at module level for easy maintenance
- **Error Handling**: Graceful error handling with user-friendly messages
- **Caching**: `@st.cache_data` decorators for efficient data loading
- **Separation of Concerns**: Clear separation between data loading, business logic, and UI rendering

### Code Organization
- **Helper Functions**: Modular functions for data retrieval, formatting, and rendering
- **DRY Principle**: Reusable functions avoid code duplication
- **Constants**: Foundation types, column mappings, and paths defined as constants
- **Theme Support**: CSS designed for both light and dark modes

### Data Architecture
- **Single Source of Truth**: CSV files are the master data source
- **Consistent Naming**: Feature names matched across all three data files (86 features)
- **Efficient Storage**: SQLite-based GeoPackage for fast querying
- **Automatic Conversion**: Scripts to regenerate GeoPackage from CSV files

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