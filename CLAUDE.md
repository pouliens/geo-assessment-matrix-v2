# EGDI Geo-Assessment Matrix for Offshore Wind Development

## Project Overview

The EGDI Geo-Assessment Matrix is a **simplified feature comparison tool** for offshore windfarm development that enables engineers and developers to compare two geological features side-by-side. The tool provides comprehensive geological assessments, constraints analysis, and foundation recommendations to support optimal site selection and foundation design.

## Key Features

- **Feature-to-Feature Comparison**: Select and compare any two geological features from 86+ available options
- **Comprehensive Data Display**: Geological characteristics, constraints analysis, foundation assessments, definitions, and engineering comments
- **Interactive Constraint Pills**: Visual representation of geological and engineering constraints with color-coded categories
- **Professional UI**: Clean, consistent interface with equal-height cards and left-border styling for easy scanning
- **Complete Definitions**: Full scientific descriptions with proper citations from research literature
- **Foundation Assessment**: Constraint levels for all four foundation types (Piles, Suction Caisson, GBS, Cables)

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas for CSV data manipulation and multi-source data integration
- **Styling**: Custom CSS with responsive design and professional styling
- **Data Sources**: Multi-file CSV architecture for comprehensive geological data
- **Deployment**: Local development server (easily deployable to cloud platforms)

## Architecture

### File Structure
```
geo-assessment-matrix-v2/
├── matrix.py                                  # Main Streamlit application (564 lines, cleaned & refactored)
├── geological_data.csv                        # Main geological features database (86 features)
├── reference-geological-constraints.csv       # Complete definitions and geological constraints
├── reference-engineering-constraints.csv     # Engineering constraints for each feature
├── CLAUDE.md                                 # This comprehensive documentation
├── README.md                                 # Basic project information
└── T5.2a _FINAL_Geo-Assessment_Matrix_D5.4_2025_v2.xlsx  # Original Excel source
```

### Data Architecture

The application uses a **multi-source data integration approach** to provide comprehensive geological information:

#### 1. **Primary Data Source: `geological_data.csv`**
- **Purpose**: Main geological features database with foundation assessments
- **Contents**: 86 geological features with basic metadata and constraint assessments
- **Key Columns**:
  - `Geological_Feature`: Feature name (e.g., "Peat (organic-rich)", "Seamount")
  - `Setting`: Geological environment (Glacial, Marine, Coastal, etc.)
  - `Process`: Formation process (Lithology, Relief, Structure, etc.)
  - `Constraint_Type`: Primary constraint category
  - `Dominant_Constraint`: Main geological constraint
  - `Piles_Assessment`: Constraint level for driven steel tube foundations
  - `Suction_Caisson_Assessment`: Constraint level for suction caisson foundations
  - `GBS_Assessment`: Constraint level for gravity-based structures
  - `Cables_Assessment`: Constraint level for subsea cables
  - `Definition`: Basic feature definition (often truncated)
  - `Comments`: Engineering comments (often truncated)

#### 2. **Enhanced Definitions: `reference-geological-constraints.csv`**
- **Purpose**: Complete scientific definitions with proper citations
- **Encoding**: Latin-1 (handles special characters like degree symbols)
- **Key Columns**:
  - Column 0: `Geological feature inventory` (feature names)
  - `Definition `: Complete scientific descriptions with citations
  - Columns 4+: Geological constraint indicators (marked with 'x')
- **Usage**: Provides full-length definitions that replace truncated ones from main data

#### 3. **Engineering Constraints: `reference-engineering-constraints.csv`**
- **Purpose**: Engineering-specific constraints for infrastructure planning
- **Encoding**: Latin-1 (handles special characters)
- **Structure**: Similar to geological constraints with 'x' markers indicating applicable constraints
- **Columns**: 30 engineering constraint categories covering installation, operation, and maintenance considerations

### Data Loading Process

The application implements a **robust multi-encoding data loading system**:

```python
@st.cache_data
def load_constraint_data():
    """Load constraint data from CSV files with encoding handling."""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    # Try multiple encodings until successful
    for encoding in encodings:
        try:
            geo_constraints = pd.read_csv("reference-geological-constraints.csv", encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    
    return geo_constraints, eng_constraints
```

### Data Integration Workflow

1. **Load Main Data**: `geological_data.csv` provides core feature information and assessments
2. **Enhance Definitions**: Extract complete definitions from `reference-geological-constraints.csv`
3. **Extract Constraints**: Parse both geological and engineering constraints from reference files
4. **Merge Data**: Combine all sources into complete feature profiles
5. **Apply Enhancements**: Add manually curated content for key features

## User Interface Components

### Left Panel (Feature Selection)
- **Geological Feature 1**: Primary feature selector
- **Geological Feature 2**: Secondary feature selector  
- **Reset Selection**: Clear all selections and start over

### Right Panel (Comparison Display)
1. **Feature Headers**: Color-coded headers for visual distinction
2. **Geological Characteristics**: Setting, Process, Constraint Type, Dominant Constraint
3. **Constraints Analysis**: Combined card with geological (blue) and engineering (orange) constraint pills
4. **Foundation Assessment Comparison**: Constraint levels for all foundation types
5. **Feature Definitions**: Complete scientific descriptions with citations
6. **Engineering Comments**: Practical guidance and recommendations

## Constraint System

### Constraint Pills
Visual indicators using color-coded pills for easy constraint identification:

- **Geological Constraints** (Blue Pills): `#e3f2fd` background, `#2196f3` border
  - Examples: "Spatial soil variability", "Strong bedrock at/near seabed", "Deep water"
  
- **Engineering Constraints** (Orange Pills): `#fff3e0` background, `#ff9800` border  
  - Examples: "Cable/pipeline abrasion", "Seabed preparation required", "Poor drivability"

### Foundation Assessment Levels
- **Higher Constraint**: Significant engineering challenges requiring special consideration
- **Moderate Constraint**: Some engineering considerations needed
- **Lower Constraint**: Minimal geological constraints

## Styling & UI Design

### Design Principles
- **Consistent Containers**: All sections use `.section-container` styling with left borders
- **Equal Heights**: Cards in the same row maintain consistent heights
- **Professional Color Scheme**: Primary blue (`#1e4d5b`) for headers and accents
- **Responsive Layout**: Adapts to different screen sizes
- **Visual Hierarchy**: Clear section separation with styled headers

### CSS Architecture
```css
/* Content containers - consistent styling for all sections */
.section-container, .constraints-card {
    background-color: #f8f9fa;
    border-left: 3px solid #1e4d5b;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 0 5px 5px 0;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}
```

## Key Functions

### Data Loading Functions
- `load_geological_data()`: Load main CSV with error handling
- `load_constraint_data()`: Load constraint files with multi-encoding support

### Data Processing Functions  
- `get_complete_feature_data()`: Merge data from multiple sources for complete feature profiles
- `get_assessment()`: Extract foundation constraint assessments
- `get_constraints_for_feature()`: Parse constraint indicators from reference files

### UI Helper Functions
- `create_tooltip()`: Generate interactive help tooltips
- **Removed unused functions**: `get_complexity_level()`, `filter_geological_features()`, `get_foundation_header_class()`

## Data Update Process

### Updating Geological Features
1. **Main Data**: Edit `geological_data.csv` to add/modify features
2. **Complete Definitions**: Update `reference-geological-constraints.csv` for full scientific descriptions
3. **Engineering Constraints**: Modify `reference-engineering-constraints.csv` for constraint indicators
4. **Enhanced Comments**: Add entries to the `enhanced_comments` dictionary in `matrix.py` for key features

### File Encoding Notes
- `geological_data.csv`: Multiple encoding support (UTF-8, Latin-1, CP1252, ISO-8859-1)
- `reference-geological-constraints.csv`: Multiple encoding support (UTF-8, Latin-1, CP1252, ISO-8859-1)
- `reference-engineering-constraints.csv`: Multiple encoding support (UTF-8, Latin-1, CP1252, ISO-8859-1)

**Important**: All data loading functions now include robust encoding detection to handle special characters automatically.

### Critical Data Consistency Requirements

**ESSENTIAL**: Feature names must be **identical** across all three CSV files for constraints to load properly.

#### Adding New Features
To add a new geological feature:

1. Add a row to `geological_data.csv` with all required columns - **this is the authoritative source for feature names**
2. Add corresponding rows to both constraint reference files using the **exact same feature name**
3. Mark applicable constraints with 'x' in constraint columns
4. Test the application to ensure proper loading and display
5. Consider adding enhanced engineering comments for significant features

#### Updating Existing Features
When modifying feature names:

1. **geological_data.csv is the master reference** - update the name here first
2. Update the **identical name** in both constraint reference files:
   - `reference-geological-constraints.csv`
   - `reference-engineering-constraints.csv`
3. Ensure exact character-by-character matching (spaces, punctuation, capitalization)
4. Test constraint loading to verify the update worked

#### Common Issues and Fixes
- **Missing Constraints**: Check that feature names match exactly across all files
- **Encoding Errors**: The application now handles multiple encodings automatically
- **Partial Matches**: The constraint matching uses exact matching first, then fallback matching
- **Case Sensitivity**: Feature name matching is case-sensitive

## Performance Optimizations

- **Streamlit Caching**: `@st.cache_data` decorators for efficient data loading
- **Single Data Load**: All CSV files loaded once at startup
- **Minimal Recomputation**: Direct feature comparison without filtering overhead
- **CSS Optimizations**: Efficient styling for smooth user interactions

## Development & Maintenance

### Code Quality
- **Clean Architecture**: 509 lines of well-documented, maintainable code
- **Robust Encoding Support**: Multi-encoding CSV loading with automatic fallback
- **Error Handling**: Graceful handling of missing files and encoding issues
- **Type Safety**: Proper null checks and data validation
- **Documentation**: Comprehensive docstrings and comments

### Best Practices Implemented
- **DRY Principle**: Reusable functions and consistent styling
- **Single Responsibility**: Each function has a clear, focused purpose  
- **Consistent Naming**: Descriptive variable and function names
- **Modular CSS**: Organized styling with logical groupings

### Testing Guidelines
1. Test with different geological features to ensure data completeness
2. Verify constraint pills display correctly for various features
3. Check foundation assessments load properly for all foundation types
4. Test encoding handling with features containing special characters
5. Validate responsive design across different screen sizes

## Deployment

### Local Development
```bash
streamlit run matrix.py
```

### Production Deployment
The application can be deployed to:
- **Streamlit Cloud**: Direct GitHub integration with automatic updates
- **Docker**: Containerized deployment for consistent environments
- **Cloud Platforms**: AWS, Azure, GCP with container services
- **Traditional Servers**: Python environment with Streamlit installation

### Environment Requirements
```
streamlit>=1.28.0
pandas>=2.0.0
```

## Research Attribution

This work was supported by:
- **UKRI** under the UK Government's Horizon Europe Guarantee (grant number 10067926)
- **GSEU Project** (European Union's Horizon Europe programme, grant agreement No 101075609)
- **Comprehensive Literature Review** including peer-reviewed research papers
- **Industry Best Practices** from offshore wind development projects

The geological assessment matrix incorporates research from numerous academic institutions, industry partners, and offshore wind development projects across European waters.

## Future Enhancements

### Data Improvements
- [ ] Complete engineering comments for all 86 geological features
- [ ] Regional data variations for different European waters
- [ ] Integration with real-time geological databases
- [ ] Seasonal and environmental condition factors

### Feature Additions
- [ ] PDF report generation for selected comparisons
- [ ] Advanced search and filtering capabilities within features
- [ ] Data visualization charts for constraint analysis
- [ ] Multi-project comparison and history tracking
- [ ] Integration with GIS mapping systems

### Technical Enhancements
- [ ] API development for programmatic access
- [ ] Machine learning insights for foundation recommendations
- [ ] Real-time collaboration features for team assessments
- [ ] Mobile-responsive design improvements
- [ ] Advanced analytics and usage tracking

## Contributing

When updating the application:

1. **Data Updates**: Follow the multi-file data architecture and test all encodings
2. **Code Changes**: Maintain existing function signatures and comprehensive documentation  
3. **Styling Updates**: Use consistent CSS classes and maintain visual hierarchy
4. **Testing**: Verify all features display correctly and constraints load properly
5. **Documentation**: Update this CLAUDE.md file with any significant changes

## Support

### Common Issues
- **Encoding Errors**: Ensure constraint files use Latin-1 encoding for special characters
- **Missing Data**: Check all three CSV files are present and properly formatted
- **Display Issues**: Verify CSS classes are applied correctly and containers have equal heights
- **Performance**: Monitor data loading times and consider additional caching if needed

### Data Quality Assurance
- Regular validation of geological data accuracy and completeness
- Updates based on new research and industry developments
- Consistency checks for constraint assessments across all foundation types
- User feedback integration for continuous improvement

This comprehensive tool represents a significant advancement in making complex geological research accessible for practical offshore wind development applications, providing engineers and developers with the detailed information needed for informed decision-making.