# EGDI Geo-Assessment Matrix for Offshore Wind Development

A simplified feature comparison tool for geological assessment of offshore windfarm sites. Compare two geological features side-by-side with comprehensive data, constraints analysis, and foundation recommendations.

## Quick Start

```bash
streamlit run matrix.py
```

## Key Features

- **Feature-to-Feature Comparison**: Compare any two of 86+ geological features
- **Comprehensive Data**: Geological characteristics, constraints, foundation assessments
- **Interactive Constraint Pills**: Visual representation with color-coded categories
- **Professional UI**: Clean, responsive design with equal-height cards

## Data Files

### Critical: Feature Name Consistency

**ESSENTIAL**: Feature names must be identical across all three CSV files for constraints to load properly.

### File Structure
- **`geological_data.csv`** - Master reference for all feature names and foundation assessments
- **`reference-geological-constraints.csv`** - Complete definitions and geological constraints
- **`reference-engineering-constraints.csv`** - Engineering constraints for each feature

### Updating Data

1. **geological_data.csv is the authoritative source** - update feature names here first
2. Update the identical name in both constraint reference files
3. Ensure exact character-by-character matching (spaces, punctuation, capitalization)
4. Test the application to verify constraints load properly

### Common Issues
- **Missing Constraints**: Feature names don't match exactly across files
- **Encoding Errors**: Now handled automatically with multi-encoding support
- **Case Sensitivity**: Feature name matching is case-sensitive

## Technical Details

- **Framework**: Streamlit with Pandas
- **Encoding Support**: Automatic detection (UTF-8, Latin-1, CP1252, ISO-8859-1)
- **Caching**: Optimized data loading with `@st.cache_data`
- **Code Quality**: 509 lines of clean, documented code

For comprehensive documentation, see `CLAUDE.md`.
