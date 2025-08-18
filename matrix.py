"""
EGDI Geo-Assessment Matrix for Offshore Wind Development
=========================================================

A simplified feature comparison tool for geological assessment of offshore windfarm sites.
Users can select two geological features and compare their characteristics, constraints, 
and foundation assessments.

Data Sources:
- geological_data.csv: Main geological features with basic data and foundation assessments
- reference-geological-constraints.csv: Complete definitions and geological constraints
- reference-engineering-constraints.csv: Engineering constraints for each feature
"""

import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="EGDI - Geo-Assessment Matrix",
    page_icon="🌊",
    layout="wide"
)

# Data loading functions
@st.cache_data
def load_geological_data():
    """Load main geological data from CSV file."""
    try:
        return pd.read_csv("geological_data.csv")
    except FileNotFoundError:
        st.error("geological_data.csv not found. Please ensure the data file is in the correct location.")
        return pd.DataFrame()
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV file: {e}")
        return pd.DataFrame()

@st.cache_data
def load_constraint_data():
    """Load constraint data from CSV files with encoding handling."""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    geo_constraints = pd.DataFrame()
    eng_constraints = pd.DataFrame()
    
    # Try different encodings for geological constraints
    for encoding in encodings:
        try:
            geo_constraints = pd.read_csv("reference-geological-constraints.csv", encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    
    # Try different encodings for engineering constraints
    for encoding in encodings:
        try:
            eng_constraints = pd.read_csv("reference-engineering-constraints.csv", encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    
    return geo_constraints, eng_constraints

# Load all data
geological_data = load_geological_data()
geo_constraints_data, eng_constraints_data = load_constraint_data()

# Extract geological features list
if not geological_data.empty:
    GEOLOGICAL_FEATURES = sorted(geological_data['Geological_Feature'].dropna().unique().tolist())
    FOUNDATION_TYPES = ["Piles", "Suction Caisson", "GBS", "Cables"]
else:
    GEOLOGICAL_FEATURES = ["No features available"]
    FOUNDATION_TYPES = ["Piles", "Suction Caisson", "GBS", "Cables"]

# Styling
st.markdown("""
<style>
    /* Header styles */
    .main-header {
        background-color: #1e4d5b;
        color: white;
        padding: 1rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
    }
    
    .nav-links {
        float: right;
        margin-top: -0.5rem;
    }
    
    .nav-links a {
        color: white;
        text-decoration: none;
        margin-left: 2rem;
    }
    
    /* Section headers */
    .section-header {
        background-color: #1e4d5b;
        color: white;
        padding: 0.5rem;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
    
    /* Feature headers */
    .foundation-header {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .cables-header {
        background-color: #a0916a;
        color: white;
    }
    
    .pipelines-header {
        background-color: #c4949c;
        color: white;
    }
    
    /* Content containers */
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
    
    /* Constraint pills */
    .constraint-pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        margin: 0.1rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        text-align: center;
    }
    
    .geo-constraint-pill {
        background-color: #e3f2fd;
        border: 1px solid #2196f3;
        color: #1976d2;
    }
    
    .eng-constraint-pill {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        color: #f57c00;
    }
    
    .constraints-container {
        margin: 0.5rem 0;
        line-height: 1.8;
    }
    
    .constraint-subheading {
        font-weight: bold;
        margin: 0.8rem 0 0.5rem 0;
        color: #1e4d5b;
        font-size: 0.95rem;
    }
    
    .constraint-subheading:first-child {
        margin-top: 0;
    }
    
    /* Global resets */
    p {
        margin-bottom: 0.5rem !important;
        margin-top: 0rem !important;
    }
    
    .stSelectbox, .stSelectbox > label, .stSelectbox > div {
        margin-top: 0rem !important;
        margin-bottom: 0rem !important;
    }
    
    .stButton > button {
        text-align: center !important;
    }
    
    .stColumn .stButton {
        margin-top: 1rem !important;
    }
    
    /* Tooltip system */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #555;
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        line-height: 1.4;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #555 transparent transparent transparent;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def create_tooltip(text, tooltip_content):
    """Create a tooltip with hover functionality."""
    return f'<span class="tooltip">{text}<span class="tooltiptext">{tooltip_content}</span></span>'

def get_complete_feature_data(feature_name):
    """Get complete feature data combining main data with enhanced definitions."""
    if geological_data.empty or feature_name == "No features match criteria":
        return None
    
    # Get main feature data
    feature_data = geological_data[geological_data['Geological_Feature'] == feature_name]
    if feature_data.empty:
        return None
    
    # Convert to dictionary to preserve all columns
    complete_data = feature_data.iloc[0].to_dict()
    
    # Enhance with complete definition from constraints file
    if not geo_constraints_data.empty:
        first_col = geo_constraints_data.columns[0]
        constraint_row = geo_constraints_data[geo_constraints_data[first_col] == feature_name]
        if not constraint_row.empty and 'Definition ' in geo_constraints_data.columns:
            definition = constraint_row['Definition '].iloc[0]
            if pd.notna(definition) and str(definition).strip():
                complete_data['Definition'] = str(definition).strip()
    
    # Enhanced engineering comments for key features
    enhanced_comments = {
        'Seamount': 'Unsuitable for all infrastructure types due to typically deep water settings, steep slopes, extremely strong lithologies, and associated hazards (e.g., seismic activity).',
    }
    
    if feature_name in enhanced_comments:
        complete_data['Comments'] = enhanced_comments[feature_name]
    
    return pd.Series(complete_data)

def get_assessment(feature_data, foundation_type):
    """Get foundation constraint assessment."""
    if feature_data is None:
        return "Data not available"
    
    assessment_columns = {
        "Piles": "Piles_Assessment",
        "Suction Caisson": "Suction_Caisson_Assessment", 
        "GBS": "GBS_Assessment",
        "Cables": "Cables_Assessment"
    }
    
    col_name = assessment_columns.get(foundation_type)
    if col_name and col_name in feature_data:
        return feature_data[col_name] if pd.notna(feature_data[col_name]) else "No assessment available"
    return "Assessment not available"

def get_constraints_for_feature(feature_name, constraints_data):
    """Extract constraints marked with 'x' for a geological feature."""
    if constraints_data.empty:
        return []
    
    # Find feature row using first column
    first_col = constraints_data.columns[0]
    feature_row = constraints_data[constraints_data[first_col] == feature_name]
    if feature_row.empty:
        return []
    
    # Extract constraints from columns 4+ (metadata in first 4)
    constraints = []
    constraint_columns = constraints_data.columns[4:]
    
    for col in constraint_columns:
        try:
            if not pd.isna(feature_row[col].iloc[0]) and str(feature_row[col].iloc[0]).strip().lower() == 'x':
                clean_name = col.strip()
                if clean_name and clean_name not in ['Unknown', 'Potentially unsuitable', 'Requires individual WTG siting investigation']:
                    constraints.append(clean_name)
        except (IndexError, KeyError):
            continue
    
    return constraints

# Main application layout
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>EGDI - Geo-Assessment Matrix</h2>
        <div class="nav-links">
            <a href="https://www.europe-geology.eu/" target="_blank">EGDI</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

# Left panel - Feature selection
with col1:
    st.header("Geological Comparison")
    st.write("Compare two geological features and their engineering constraints for offshore windfarm development.")
    
    st.subheader("Feature Selection")
    
    geological_feature_1 = st.selectbox("**Geological Feature 1**", GEOLOGICAL_FEATURES, key="feature1")
    geological_feature_2 = st.selectbox("**Geological Feature 2**", GEOLOGICAL_FEATURES, 
                                       index=1 if len(GEOLOGICAL_FEATURES) > 1 else 0, key="feature2")
    
    if st.button("Reset Selection", use_container_width=True):
        for key in ["feature1", "feature2"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# Right panel - Comparison display
with col2:
    # Feature headers
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown(f'<div class="foundation-header cables-header">{geological_feature_1}</div>', unsafe_allow_html=True)
    
    with col_f2:
        st.markdown(f'<div class="foundation-header pipelines-header">{geological_feature_2}</div>', unsafe_allow_html=True)
    
    # Get complete feature data
    feature_data_1 = get_complete_feature_data(geological_feature_1)
    feature_data_2 = get_complete_feature_data(geological_feature_2)
    
    # Geological Characteristics
    st.markdown(f'<div class="section-header">{create_tooltip("Geological Characteristics", "Key geological characteristics for both selected features")}</div>', 
                unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        if feature_data_1 is not None:
            st.markdown(f"""
            <div class="section-container">
                <p><strong>Setting:</strong> {feature_data_1['Setting']}</p>
                <p><strong>Process:</strong> {feature_data_1['Process']}</p>
                <p><strong>Constraint Type:</strong> {feature_data_1['Constraint_Type']}</p>
                <p><strong>Dominant Constraint:</strong> {feature_data_1['Dominant_Constraint']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-container"><p><strong>No data available for Feature 1</strong></p></div>', unsafe_allow_html=True)
    
    with col_c2:
        if feature_data_2 is not None:
            st.markdown(f"""
            <div class="section-container">
                <p><strong>Setting:</strong> {feature_data_2['Setting']}</p>
                <p><strong>Process:</strong> {feature_data_2['Process']}</p>
                <p><strong>Constraint Type:</strong> {feature_data_2['Constraint_Type']}</p>
                <p><strong>Dominant Constraint:</strong> {feature_data_2['Dominant_Constraint']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-container"><p><strong>No data available for Feature 2</strong></p></div>', unsafe_allow_html=True)
    
    # Constraints Analysis
    st.markdown(f'<div class="section-header">{create_tooltip("Constraints Analysis", "Geological and engineering constraints for both features")}</div>', 
                unsafe_allow_html=True)
    
    col_cc1, col_cc2 = st.columns(2)
    
    with col_cc1:
        geo_constraints_1 = get_constraints_for_feature(geological_feature_1, geo_constraints_data)
        eng_constraints_1 = get_constraints_for_feature(geological_feature_1, eng_constraints_data)
        
        constraints_content = '<div class="constraint-subheading">Geological Constraints</div>'
        if geo_constraints_1:
            geo_pills = ' '.join([f'<span class="constraint-pill geo-constraint-pill">{c}</span>' for c in geo_constraints_1])
            constraints_content += f'<div class="constraints-container">{geo_pills}</div>'
        else:
            constraints_content += '<p style="font-style: italic; color: #6c757d;">No geological constraints identified</p>'
        
        constraints_content += '<div class="constraint-subheading">Engineering Constraints</div>'
        if eng_constraints_1:
            eng_pills = ' '.join([f'<span class="constraint-pill eng-constraint-pill">{c}</span>' for c in eng_constraints_1])
            constraints_content += f'<div class="constraints-container">{eng_pills}</div>'
        else:
            constraints_content += '<p style="font-style: italic; color: #6c757d;">No engineering constraints identified</p>'
        
        st.markdown(f'<div class="constraints-card">{constraints_content}</div>', unsafe_allow_html=True)
    
    with col_cc2:
        geo_constraints_2 = get_constraints_for_feature(geological_feature_2, geo_constraints_data)
        eng_constraints_2 = get_constraints_for_feature(geological_feature_2, eng_constraints_data)
        
        constraints_content = '<div class="constraint-subheading">Geological Constraints</div>'
        if geo_constraints_2:
            geo_pills = ' '.join([f'<span class="constraint-pill geo-constraint-pill">{c}</span>' for c in geo_constraints_2])
            constraints_content += f'<div class="constraints-container">{geo_pills}</div>'
        else:
            constraints_content += '<p style="font-style: italic; color: #6c757d;">No geological constraints identified</p>'
        
        constraints_content += '<div class="constraint-subheading">Engineering Constraints</div>'
        if eng_constraints_2:
            eng_pills = ' '.join([f'<span class="constraint-pill eng-constraint-pill">{c}</span>' for c in eng_constraints_2])
            constraints_content += f'<div class="constraints-container">{eng_pills}</div>'
        else:
            constraints_content += '<p style="font-style: italic; color: #6c757d;">No engineering constraints identified</p>'
        
        st.markdown(f'<div class="constraints-card">{constraints_content}</div>', unsafe_allow_html=True)
    
    # Foundation Assessment Comparison
    st.markdown(f'<div class="section-header">{create_tooltip("Foundation Assessment Comparison", "Constraint levels for all foundation types for both features")}</div>', 
                unsafe_allow_html=True)
    
    col_fa1, col_fa2 = st.columns(2)
    
    with col_fa1:
        if feature_data_1 is not None:
            foundation_content = ""
            for foundation_type in FOUNDATION_TYPES:
                assessment = get_assessment(feature_data_1, foundation_type)
                foundation_content += f"<p><strong>{foundation_type}:</strong> {assessment}</p>"
            st.markdown(f'<div class="section-container">{foundation_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-container"><p><strong>No assessment data available</strong></p></div>', unsafe_allow_html=True)
    
    with col_fa2:
        if feature_data_2 is not None:
            foundation_content = ""
            for foundation_type in FOUNDATION_TYPES:
                assessment = get_assessment(feature_data_2, foundation_type)
                foundation_content += f"<p><strong>{foundation_type}:</strong> {assessment}</p>"
            st.markdown(f'<div class="section-container">{foundation_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-container"><p><strong>No assessment data available</strong></p></div>', unsafe_allow_html=True)
    
    # Feature Definitions
    st.markdown(f'<div class="section-header">{create_tooltip("Feature Definitions", "Scientific descriptions of both geological features")}</div>', 
                unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        if feature_data_1 is not None:
            definition_text = feature_data_1['Definition'] if pd.notna(feature_data_1['Definition']) else "No definition available"
            st.markdown(f'<div class="section-container"><p>{definition_text}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-container"><p>No definition available</p></div>', unsafe_allow_html=True)
    
    with col_d2:
        if feature_data_2 is not None:
            definition_text = feature_data_2['Definition'] if pd.notna(feature_data_2['Definition']) else "No definition available"
            st.markdown(f'<div class="section-container"><p>{definition_text}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-container"><p>No definition available</p></div>', unsafe_allow_html=True)
    
    # Engineering Comments
    st.markdown(f'<div class="section-header">{create_tooltip("Engineering Comments", "Practical guidance and recommendations for offshore wind development")}</div>', 
                unsafe_allow_html=True)
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        if feature_data_1 is not None:
            comments_text = feature_data_1['Comments'] if pd.notna(feature_data_1['Comments']) else "No comments available"
            st.markdown(f'<div class="section-container"><p>{comments_text}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-container"><p>No engineering comments available</p></div>', unsafe_allow_html=True)
    
    with col_e2:
        if feature_data_2 is not None:
            comments_text = feature_data_2['Comments'] if pd.notna(feature_data_2['Comments']) else "No comments available"
            st.markdown(f'<div class="section-container"><p>{comments_text}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-container"><p>No engineering comments available</p></div>', unsafe_allow_html=True)
    
    # Download Report button
    st.markdown("<br>", unsafe_allow_html=True)
    col_empty, col_download = st.columns([3, 1])
    with col_download:
        if st.button("Download Report", use_container_width=True):
            st.info("Report generation feature coming soon!")