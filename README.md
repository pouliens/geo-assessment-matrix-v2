# EGDI Geo-Assessment Matrix

Geological feature comparison tool for offshore wind development. Compare two features side-by-side with constraints analysis and foundation recommendations.

## Quick Start

```bash
# Using uv (recommended)
uv venv
source .venv/Scripts/activate  # Windows
uv pip install -r requirements.txt
streamlit run matrix.py

# Using pip
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
streamlit run matrix.py
```

App opens at `http://localhost:8501`

## Docker

```bash
# Local development
docker build -t geo-matrix .
docker run -p 8501:80 geo-matrix

# Production deployment via GitLab CI/CD
# Automatically deploys to Kubernetes
# Access: http://egdi-geo-assessment-matrix-3512-main.kube-idev.bgslcdevops.test/
```

## Features

- **Compare 86 geological features** side-by-side
- **Interactive constraint analysis** with descriptive constraint names
- **Foundation assessments** for Piles, Suction Caisson, GBS, and Cables
- **Professional responsive UI** with clean design
- **Single GeoPackage data source** for improved performance

## Data Storage

**Single GeoPackage file**: `data/geological_data.gpkg` contains all geological data in SQLite format.

### Data Tables
- `geological_features` - Master feature database (86 features)
- `geological_constraints` - Geological constraints & definitions (73 features)
- `engineering_constraints` - Engineering constraints (73 features)

### Updating Data

**Option 1: CSV Workflow (Recommended)**
```bash
# 1. Edit CSV files (maintains data editing workflow)
# 2. Update GeoPackage from CSV files
python update_geopackage.py
```

**Option 2: Direct Database Editing**
```bash
# Connect to GeoPackage with SQLite tools
sqlite3 data/geological_data.gpkg
```

**Critical**: Feature names must be identical across all data tables.

### Initial Setup
```bash
# Convert CSV files to GeoPackage (one-time setup)
python create_geopackage.py
```

## Tech Stack
- **Streamlit** + **Pandas** + **SQLite** (built-in)
- **GeoPackage** single-file data storage (no additional dependencies)
- **Cached data loading** with `@st.cache_data` for optimal performance
- **Configuration-driven** design for easy maintenance
- **Docker-ready** with multi-stage deployment

## Data Migration (2025 September)
✅ **Successfully migrated from CSV files to GeoPackage**
- Improved performance with SQLite queries
- Maintained CSV editing workflow for data updates
- Enhanced constraint display with proper descriptive names
- Single-file deployment simplifies Docker containers

## Production Ready
- 📊 **Data integrity** with proper constraint relationships
- 🚀 **Docker deployment** tested and verified
