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

- Compare 86+ geological features
- Interactive constraint visualization  
- Foundation assessments for 4 foundation types
- Professional UI with responsive design

## Data Files

**Critical**: Feature names must be identical across all CSV files.

- `data/geological_data.csv` - Master feature database
- `data/reference-geological-constraints.csv` - Geological constraints & definitions
- `data/reference-engineering-constraints.csv` - Engineering constraints

### Updating Data
1. Update `geological_data.csv` first (authoritative source)
2. Update both constraint files with identical names
3. Ensure exact character matching (case-sensitive)
4. Test constraint loading

## Tech Stack
- Streamlit + Pandas
- Multi-encoding CSV support
- Cached data loading
- Clean, documented codebase

See `CLAUDE.md` for detailed documentation.
