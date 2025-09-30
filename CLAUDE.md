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
- `data/geological_data.csv` - Master feature database (authoritative source)
- `data/reference-geological-constraints.csv` - Complete definitions & geological constraints  
- `data/reference-engineering-constraints.csv` - Engineering constraints
- `Dockerfile` - Container deployment

### Data Integration
Multi-source CSV files with automatic encoding detection (UTF-8, Latin-1, CP1252, ISO-8859-1).

## Critical Requirements

**Feature Name Consistency**: Names must be identical across all three CSV files.

### Adding/Updating Features
1. Update `geological_data.csv` first (master reference)
2. Update both constraint files with identical names
3. Ensure exact character matching (case-sensitive)
4. Test constraint loading

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

### geological_data.csv (Master)
- `Geological_Feature` - Feature names
- `Setting`, `Process`, `Constraint_Type`, `Dominant_Constraint`
- `*_Assessment` - Foundation constraint levels
- `Definition`, `Comments`

### Constraint Files
- Feature names in first column
- Constraint indicators marked with 'x'
- Complete definitions with citations

## Common Issues
- **Missing Constraints**: Feature names don't match exactly
- **Encoding Errors**: Handled automatically with multi-encoding support
- **Case Sensitivity**: Names must match exactly

## Performance
- `@st.cache_data` decorators for data loading
- Single load at startup
- CSS optimizations for smooth interactions