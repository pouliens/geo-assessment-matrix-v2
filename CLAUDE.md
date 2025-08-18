# EGDI Geo-Assessment Matrix for Offshore Wind Development

## Project Overview

The EGDI Geo-Assessment Matrix is a decision support tool for offshore windfarm development that helps engineers and developers assess geological constraints and compare foundation types. The tool enables users to explore geological features and their engineering implications for optimal site selection and foundation design.

This tool was developed to simplify windfarm foundation selection by providing:
- Real geological assessment data from comprehensive research
- Side-by-side comparison of foundation types
- Intelligent filtering of geological features
- Professional engineering guidance for offshore wind development

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas for CSV data manipulation
- **Data Source**: Geological assessment matrix CSV with 86+ geological features
- **Styling**: Custom CSS for professional UI/UX
- **Deployment**: Local development server (easily deployable to cloud platforms)

## Architecture

```
geo-assessment-matrix-v2/
├── matrix.py              # Main Streamlit application
├── geological_data.csv    # Geological assessment database
├── CLAUDE.md             # This documentation file
└── README.md             # Basic project information
```

### Data Structure

The `geological_data.csv` contains 86 geological features with the following key attributes:
- **Geological_Feature**: Name of the geological feature (e.g., "Peat (organic-rich)", "Glacifluvial delta")
- **Setting**: Geological environment (Sediments, Glacial, Marine, Fluvial, Coastal, Solid Earth, etc.)
- **Process**: Geological process (Lithology, Relief, Structure, Geohazard, etc.)
- **Constraint_Type**: Primary constraint category
- **Definition**: Scientific description of the geological feature
- **Foundation Assessments**: Constraint levels for each foundation type:
  - `Piles_Assessment`: Driven steel tube foundations
  - `Suction_Caisson_Assessment`: Large steel buckets with suction installation
  - `GBS_Assessment`: Gravity-based concrete structures
  - `Cables_Assessment`: Subsea power transmission cables
- **Dominant_Constraint**: Primary geological constraint
- **Comments**: Engineering guidance and recommendations

### Constraint Levels

The tool uses three constraint levels for foundation assessments:
- **Higher Constraint**: Significant engineering challenges, requires special consideration
- **Moderate Constraint**: Some engineering considerations needed
- **Lower Constraint**: Minimal geological constraints

## Key Features

### 1. Intelligent Filtering System
- **Hierarchical Filtering**: Setting → Process → Constraint Type → Geological Feature
- **Dynamic Updates**: Geological features filter automatically based on selected criteria
- **Real-time Results**: Instant updates when filter selections change

### 2. Foundation Comparison
- **Side-by-side Analysis**: Compare any two foundation types simultaneously
- **Constraint Assessment**: View specific constraint levels for each foundation type
- **Complexity Rating**: Automatic complexity assessment (High/Medium/Low/Unknown)

### 3. Professional Interface
- **Responsive Design**: Clean, professional layout optimized for engineering workflows
- **Interactive Tooltips**: Hover over labels for detailed explanations
- **Visual Indicators**: Color-coded foundation headers and constraint tags
- **Export Functionality**: Export selection data for reporting

### 4. Comprehensive Data
- **86 Geological Features**: From peat deposits to submarine canyons
- **12 Geological Settings**: Covering all offshore environments
- **7 Geological Processes**: Complete process categorization
- **Real Engineering Data**: Based on actual offshore wind research and case studies

## User Interface Components

### Left Panel (Filters)
1. **Setting & Process**: Geological environment and formation process selectors
2. **Type of Constraint**: Primary constraint category filter
3. **Geological Features**: Dynamically filtered feature selector
4. **Foundation Types**: Two foundation type selectors for comparison
5. **Action Buttons**: Reset filters and export functionality

### Right Panel (Results)
1. **Selection Tags**: Current filter selections displayed as tags
2. **Foundation Headers**: Color-coded headers for selected foundation types
3. **Geological Constraints**: Key characteristics and dominant constraints
4. **Engineering Significance**: Constraint assessments for each foundation type
5. **Complexity Assessment**: Overall complexity levels
6. **Engineering Comments**: Practical guidance and recommendations

## Usage Workflow

1. **Select Geological Setting**: Choose the environment (e.g., Marine, Glacial, Coastal)
2. **Choose Process**: Select the geological process (e.g., Lithology, Relief)
3. **Filter by Constraint**: Optionally filter by constraint type
4. **Pick Geological Feature**: Select from filtered list of geological features
5. **Compare Foundations**: Choose two foundation types for comparison
6. **Review Results**: Analyze constraint assessments and engineering guidance
7. **Export Data**: Export selection for reporting or further analysis

## Data Sources

The geological assessment matrix is based on research supported by:
- **UKRI** under the UK Government's Horizon Europe Guarantee (grant number 10067926)
- **GSEU Project** (European Union's Horizon Europe programme, grant agreement No 101075609)
- **Extensive Literature Review** including peer-reviewed research papers
- **Industry Best Practices** from offshore wind development projects

## Technical Implementation

### Core Functions

- `load_geological_data()`: CSV data loading with error handling
- `filter_geological_features()`: Dynamic feature filtering based on criteria
- `get_feature_data()`: Retrieve specific geological feature information
- `get_assessment()`: Extract constraint assessment for foundation types
- `get_complexity_level()`: Convert assessments to complexity ratings
- `create_tooltip()`: Generate interactive tooltips with hover functionality

### Performance Optimizations

- **Data Caching**: `@st.cache_data` decorator for efficient CSV loading
- **Minimal Recomputation**: Smart filtering to avoid unnecessary recalculations
- **Responsive UI**: CSS optimizations for smooth user interactions

### CSS Customizations

- **Reduced Spacing**: Optimized gap between labels and dropdowns
- **Professional Styling**: Consistent color scheme and typography
- **Interactive Elements**: Hover effects and tooltips
- **Responsive Layout**: Adapts to different screen sizes

## Development Guidelines

### Code Structure
- **Modular Functions**: Each function has a single responsibility
- **Clear Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Graceful handling of missing data and errors
- **Type Hints**: Improved code readability and maintenance

### Data Management
- **CSV Format**: Easy to edit and maintain geological data
- **Consistent Naming**: Standardized column names and values
- **Data Validation**: Built-in checks for data integrity

### UI/UX Principles
- **User-Centric Design**: Workflow optimized for engineering decision-making
- **Progressive Disclosure**: Information revealed as users make selections
- **Visual Hierarchy**: Clear information architecture and layout
- **Accessibility**: Proper labels and semantic markup

## Deployment Options

### Local Development
```bash
streamlit run matrix.py
```

### Cloud Deployment
The application can be deployed to:
- **Streamlit Cloud**: Direct GitHub integration
- **Heroku**: Container-based deployment
- **AWS/Azure/GCP**: Cloud platform deployment
- **Docker**: Containerized deployment

### Environment Requirements
```
streamlit>=1.28.0
pandas>=2.0.0
```

## Future Enhancements

### Data Expansion
- [ ] Additional geological features from new research
- [ ] Regional data variations (North Sea, Baltic Sea, etc.)
- [ ] Seasonal and environmental condition factors
- [ ] Integration with GIS data sources

### Functionality Improvements
- [ ] PDF report generation
- [ ] Advanced filtering and search capabilities
- [ ] Data visualization and charts
- [ ] Multi-project comparison features
- [ ] Integration with external geological databases

### Technical Enhancements
- [ ] API development for programmatic access
- [ ] Real-time data updates from research databases
- [ ] Advanced analytics and machine learning insights
- [ ] Mobile-responsive design improvements

## Contributing

When updating geological data or adding features:

1. **Data Updates**: Edit `geological_data.csv` following the established format
2. **Code Changes**: Maintain existing function signatures and documentation
3. **Testing**: Verify all filters and data display correctly
4. **Documentation**: Update this CLAUDE.md file with any significant changes

## Support and Maintenance

### Data Quality
- Regular validation of geological data accuracy
- Updates based on new research and industry developments
- Consistency checks for constraint assessments

### Technical Maintenance
- Streamlit version compatibility
- Performance monitoring and optimization
- Security updates for dependencies

### User Support
- Clear error messages and guidance
- Comprehensive tooltips and help text
- Professional documentation and examples

## Research Impact

This tool supports evidence-based decision making in offshore wind development by:
- **Reducing Risk**: Early identification of geological constraints
- **Optimizing Design**: Foundation type selection based on site conditions
- **Cost Efficiency**: Avoiding unsuitable geological features
- **Knowledge Transfer**: Sharing research insights with industry practitioners

The geological assessment matrix represents a significant advancement in making complex geological research accessible for practical offshore wind development applications.

## Acknowledgments

This work was supported by UKRI under the UK Government's Horizon Europe Guarantee (grant number 10067926) as part of the GSEU project (European Union's Horizon Europe programme, grant agreement No 101075609).

The comprehensive geological database incorporates research from numerous academic institutions, industry partners, and offshore wind development projects across European waters.