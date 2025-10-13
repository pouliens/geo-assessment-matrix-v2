"""
EGDI Geo-Assessment Matrix for Offshore Wind Development
=========================================================

A simplified feature comparison tool for geological assessment of offshore windfarm sites.
Users can select two geological features and compare their characteristics, constraints,
and foundation assessments.

Data Sources:
- data/geological_data.gpkg: Single GeoPackage containing all geological data:
  * geological_features: Main geological features with basic data and foundation assessments
  * geological_constraints: Complete definitions and geological constraints
  * engineering_constraints: Engineering constraints for each feature
"""

import streamlit as st
import pandas as pd
import sqlite3
from typing import Optional, List, Tuple

# Configuration constants
GEOPACKAGE_PATH = "data/geological_data.gpkg"  # Single data source file
FOUNDATION_TYPES = ["Piles", "Suction Caisson", "GBS", "Cables"]  # Available foundation types
FOUNDATION_COLUMN_MAP = {  # Maps foundation types to database column names
    "Piles": "Piles_Assessment",
    "Suction Caisson": "Suction_Caisson_Assessment",
    "GBS": "GBS_Assessment",
    "Cables": "Cables_Assessment"
}

# Page configuration
st.set_page_config(
    page_title="EGDI - Geo-Assessment Matrix",
    page_icon="🌊",
    layout="wide"
)

# Data loading functions
@st.cache_data
def load_geological_data() -> pd.DataFrame:
    """Load main geological data from GeoPackage.

    Returns:
        DataFrame containing geological features with all attributes
    """
    try:
        with sqlite3.connect(GEOPACKAGE_PATH) as conn:
            # Explicitly quote "References" as it's a SQL reserved keyword
            df = pd.read_sql_query('''
                SELECT
                    Geological_Feature, Setting, Constraint_Type, Definition,
                    Piles_Assessment, Suction_Caisson_Assessment, GBS_Assessment, Cables_Assessment,
                    Dominant_Constraint, Comments, "References"
                FROM geological_features
            ''', conn)
        return df
    except FileNotFoundError:
        st.error(f"{GEOPACKAGE_PATH} not found. Please ensure the data file is in the correct location.")
        return pd.DataFrame()
    except sqlite3.DatabaseError as e:
        st.error(f"Database error loading geological data: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading geological data from GeoPackage: {e}")
        return pd.DataFrame()

@st.cache_data
def load_constraint_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load constraint data from GeoPackage.

    Returns:
        Tuple of (geological_constraints, engineering_constraints) DataFrames
    """
    try:
        with sqlite3.connect(GEOPACKAGE_PATH) as conn:
            geo_constraints = pd.read_sql_query("SELECT * FROM geological_constraints", conn)
            eng_constraints = pd.read_sql_query("SELECT * FROM engineering_constraints", conn)
        return geo_constraints, eng_constraints
    except sqlite3.DatabaseError as e:
        st.error(f"Database error loading constraint data: {e}")
        return pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading constraint data from GeoPackage: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Load all data
geological_data = load_geological_data()
geo_constraints_data, eng_constraints_data = load_constraint_data()

# Extract geological features list
if not geological_data.empty:
    GEOLOGICAL_FEATURES = sorted(geological_data['Geological_Feature'].dropna().unique().tolist())
else:
    GEOLOGICAL_FEATURES = ["No features available"]

# Styling - Theme-aware colors
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
        transition: opacity 0.2s ease, text-decoration 0.2s ease;
    }

    .nav-links a:hover {
        opacity: 0.8;
        text-decoration: underline;
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
        margin: 0rem 0;
        color: white;
    }

    .cables-header {
        background-color: #a0916a;
    }

    .pipelines-header {
        background-color: #c4949c;
    }

    /* Content containers - theme aware */
    .section-container, .constraints-card {
        background-color: rgba(128, 128, 128, 0.1);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 5px 5px 0;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    /* Color-coded left borders for each feature */
    .section-container:has(.feature-label-1),
    .constraints-card:has(.feature-label-1) {
        border-left: 3px solid #a0916a;
    }

    .section-container:has(.feature-label-2),
    .constraints-card:has(.feature-label-2) {
        border-left: 3px solid #c4949c;
    }

    /* Feature context labels */
    .feature-label {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.25rem 0.5rem;
        margin: -1rem -1rem 0.75rem -1rem;
        border-radius: 0 5px 0 0;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .feature-label-1 {
        background-color: #a0916a;
    }

    .feature-label-2 {
        background-color: #c4949c;
    }

    /* Constraint pills - theme aware */
    .constraint-pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        margin: 0.2rem 0.1rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        text-align: center;
    }

    .geo-constraint-pill {
        background-color: rgba(33, 150, 243, 0.15);
        border: 1px solid #2196f3;
        color: #2196f3;
    }

    .eng-constraint-pill {
        background-color: rgba(255, 152, 0, 0.15);
        border: 1px solid #ff9800;
        color: #ff9800;
    }

    /* Dark mode adjustments */
    [data-theme="dark"] .geo-constraint-pill {
        background-color: rgba(33, 150, 243, 0.25);
        color: #64b5f6;
    }

    [data-theme="dark"] .eng-constraint-pill {
        background-color: rgba(255, 152, 0, 0.25);
        color: #ffb74d;
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

    [data-theme="dark"] .constraint-subheading {
        color: #64b5f6;
    }

    .constraint-subheading:first-child {
        margin-top: 0;
    }

    /* References card styling - subtle and less prominent */
    .references-card {
        background-color: rgba(128, 128, 128, 0.05);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 5px 5px 0;
        border-left: 3px solid rgba(128, 128, 128, 0.3);
        font-size: 0.85rem;
        line-height: 1.6;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    [data-theme="dark"] .references-card {
        background-color: rgba(128, 128, 128, 0.08);
    }

    /* Color-coded left borders for reference cards - match other cards */
    .references-card:has(.feature-label-1) {
        border-left: 3px solid #a0916a;
    }

    .references-card:has(.feature-label-2) {
        border-left: 3px solid #c4949c;
    }

    .references-card .feature-label {
        opacity: 0.8;
    }

    .references-card p {
        color: rgba(100, 100, 100, 1);
        margin: 0.25rem 0 !important;
        font-size: 0.85rem;
    }

    [data-theme="dark"] .references-card p {
        color: rgba(180, 180, 180, 0.85);
    }

    /* Compact references subheading */
    .references-subheading {
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: rgba(128, 128, 128, 0.75);
        margin-top: 0 !important;
        margin-bottom: 0.4rem !important;
    }

    [data-theme="dark"] .references-subheading {
        color: rgba(180, 180, 180, 0.6);
    }

    /* Global resets */
    p {
        margin-bottom: 0.5rem !important;
        margin-top: 0rem !important;
    }

    .stSelectbox, .stSelectbox > label, .stSelectbox > div {
        margin-top: 0rem !important;
        margin-bottom: 0rem !important;
        cursor: pointer !important;
    }

    .stSelectbox > div > div {
        cursor: pointer !important;
    }

    .stSelectbox select {
        cursor: pointer !important;
    }

    .stSelectbox [data-baseweb="select"] {
        cursor: pointer !important;
    }

    .stButton > button {
        text-align: center !important;
    }

    .stButton > button > p, .stButton button p, .stButton p {
        margin-bottom: 0 !important;
        margin-top: 0 !important;
    }

    .stColumn .stButton {
        margin-top: 1rem !important;
    }

    /* Tooltip system - theme aware */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: rgba(64, 64, 64, 0.95);
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
        border-color: rgba(64, 64, 64, 0.95) transparent transparent transparent;
    }

    /* Terms Modal */
    .terms-modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.4);
    }

    .terms-modal:target {
        display: block;
    }

    .terms-modal-content {
        background-color: white;
        color: #262730;
        margin: 10% auto;
        padding: 30px 40px;
        border-radius: 8px;
        width: 80%;
        max-width: 700px;
        max-height: 70vh;
        overflow-y: auto;
        position: relative;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        line-height: 1.6;
    }

    [data-theme="dark"] .terms-modal-content {
        background-color: #262730;
        color: #fafafa;
    }

    .terms-modal-content h3 {
        color: #1e4d5b;
    }

    [data-theme="dark"] .terms-modal-content h3 {
        color: #64b5f6;
    }

    .terms-modal-content p {
        color: inherit;
    }

    .terms-close {
        position: absolute;
        right: 20px;
        top: 15px;
        font-size: 24px;
        font-weight: bold;
        text-decoration: none !important;
        color: #666;
        cursor: pointer;
    }

    .terms-close:hover {
        color: #000;
        text-decoration: none !important;
    }

    [data-theme="dark"] .terms-close {
        color: #999;
    }

    [data-theme="dark"] .terms-close:hover {
        color: #fafafa;
        text-decoration: none !important;
    }

    .terms-modal-background {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def create_tooltip(text: str, tooltip_content: str) -> str:
    """Create a tooltip with hover functionality.

    Args:
        text: The visible text to display
        tooltip_content: The content to show on hover

    Returns:
        HTML string with tooltip markup
    """
    return f'<span class="tooltip">{text}<span class="tooltiptext">{tooltip_content}</span></span>'

def format_references(references_text) -> Optional[str]:
    """Format references for display.

    Args:
        references_text: References text from the References column

    Returns:
        Formatted references string, or None if no references
    """
    if pd.isna(references_text) or not str(references_text).strip():
        return None
    return str(references_text).strip()

def get_complete_feature_data(feature_name: str) -> Optional[pd.Series]:
    """Get complete feature data for a geological feature.

    Args:
        feature_name: Name of the geological feature

    Returns:
        Series with feature data, or None if not found
    """
    if geological_data.empty or feature_name == "No features match criteria":
        return None

    # Get feature data
    feature_data = geological_data[geological_data['Geological_Feature'] == feature_name]
    if feature_data.empty:
        return None

    return feature_data.iloc[0]

def get_assessment(feature_data: Optional[pd.Series], foundation_type: str) -> str:
    """Get foundation constraint assessment for a specific foundation type.

    Args:
        feature_data: Series containing feature data
        foundation_type: Type of foundation (Piles, Suction Caisson, GBS, or Cables)

    Returns:
        Assessment string
    """
    if feature_data is None:
        return "Data not available"

    col_name = FOUNDATION_COLUMN_MAP.get(foundation_type)
    if col_name and col_name in feature_data:
        return feature_data[col_name] if pd.notna(feature_data[col_name]) else "No assessment available"
    return "Assessment not available"

def get_constraints_for_feature(feature_name: str, constraints_data: pd.DataFrame) -> List[str]:
    """Extract constraints marked with 'x' for a geological feature.

    Args:
        feature_name: Name of the geological feature
        constraints_data: DataFrame containing constraint information

    Returns:
        List of constraint names that apply to this feature
    """
    if constraints_data.empty:
        return []

    # Find feature row using first column (exact match required)
    first_col = constraints_data.columns[0]
    feature_row = constraints_data[constraints_data[first_col] == feature_name]

    if feature_row.empty:
        return []

    # Extract constraints from all columns except the first (which is the feature name)
    constraints = []
    constraint_columns = constraints_data.columns[1:]  # All columns except first are constraints

    for col in constraint_columns:
        try:
            cell_value = feature_row[col].iloc[0]
            if not pd.isna(cell_value) and str(cell_value).strip().lower() == 'x':
                clean_name = col.strip()
                # Exclude meta-columns that aren't actual constraints
                if clean_name and clean_name not in ['Unknown', 'Potentially unsuitable', 'Requires individual WTG siting investigation']:
                    constraints.append(clean_name)
        except (IndexError, KeyError):
            continue

    return constraints

def render_geological_characteristics_card(feature_name: str, feature_data: Optional[pd.Series], feature_label_class: str) -> str:
    """Render a geological characteristics card with definition.

    Args:
        feature_name: Name of the geological feature
        feature_data: Series containing feature data
        feature_label_class: CSS class for feature label (e.g., 'feature-label-1')

    Returns:
        HTML string for the card
    """
    if feature_data is None:
        return f'''<div class="section-container">
            <div class="feature-label {feature_label_class}">{feature_name}</div>
            <p><strong>No data available</strong></p>
        </div>'''

    # Get definition
    definition_text = feature_data['Definition'] if pd.notna(feature_data['Definition']) else "No definition available"

    # Build HTML content
    content = f'''<div class="section-container">
        <div class="feature-label {feature_label_class}">{feature_name}</div>
        <p><strong>Setting:</strong> {feature_data['Setting']}</p>
        <p><strong>Constraint Type:</strong> {feature_data['Constraint_Type']}</p>
        <p><strong>Dominant Constraint:</strong> {feature_data['Dominant_Constraint']}</p>
        <p><strong>Definition:</strong> {definition_text}</p>
    </div>'''

    return content

# Main application layout
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>EGDI - Geo-Assessment Matrix</h2>
        <div class="nav-links">
            <a href="https://www.data.gov.uk/dataset/c109cb6c-a32e-482b-a4e4-131d24a76f7f/the-geo-assessment-matrix-pan-european-catalogue-of-key-parameters-for-offshore-wind-farm-sitin" target="_blank">Data</a>
            <a href="https://www.geologicalservice.eu/upload/content/1691/gseu_d5-3_pan-european-catalogue-of-key-parameters-for-offshore-windfarm-siting_v1.pdf" target="_blank">Methodology</a>
            <a href="#termsModal" style="color: white; text-decoration: none;">Terms of Use</a>
            <a href="https://www.europe-geology.eu/" style="margin-right: 2rem" target="_blank">EGDI</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Terms of Use Modal
st.markdown("""
<div id="termsModal" class="terms-modal">
    <a href="#" class="terms-modal-background"></a>
    <div class="terms-modal-content">
        <a href="#" class="terms-close">&times;</a>
        <h3 style="margin-top: 0;">Terms of Use</h3>
        <p>The copyright of materials derived from the British Geological Survey's work is vested in the Natural Environment Research Council [NERC]. No part of this work may be reproduced or transmitted in any form or by any means, or stored in a retrieval system of any nature, without the prior permission of the copyright holder, via the BGS Intellectual Property Rights Manager.</p>
        <p>Use by customers of information provided by the BGS, is at the customer's own risk. In view of the disparate sources of information at BGS's disposal, including such material donated to BGS, that BGS accepts in good faith as being accurate, the Natural Environment Research Council (NERC) gives no warranty, expressed or implied, as to the quality or accuracy of the information supplied, or to the information's suitability for any use.</p>
        <p>NERC/BGS accepts no liability whatever in respect of loss, damage, injury or other occurence however caused.</p>
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
        card_html = render_geological_characteristics_card(geological_feature_1, feature_data_1, 'feature-label-1')
        st.markdown(card_html, unsafe_allow_html=True)

    with col_c2:
        card_html = render_geological_characteristics_card(geological_feature_2, feature_data_2, 'feature-label-2')
        st.markdown(card_html, unsafe_allow_html=True)

    # Constraints Analysis
    st.markdown(f'<div class="section-header">{create_tooltip("Constraints Analysis", "Geological and engineering constraints for both features")}</div>',
                unsafe_allow_html=True)

    col_cc1, col_cc2 = st.columns(2)

    with col_cc1:
        geo_constraints_1 = get_constraints_for_feature(geological_feature_1, geo_constraints_data)
        eng_constraints_1 = get_constraints_for_feature(geological_feature_1, eng_constraints_data)

        constraints_content = f'<div class="feature-label feature-label-1">{geological_feature_1}</div>'
        constraints_content += '<div class="constraint-subheading">Geological Constraints</div>'
        if geo_constraints_1:
            geo_pills = ' '.join([f'<span class="constraint-pill geo-constraint-pill">{c}</span>' for c in geo_constraints_1])
            constraints_content += f'<div class="constraints-container">{geo_pills}</div>'
        else:
            constraints_content += '<p style="font-style: italic; opacity: 0.6;">No geological constraints identified</p>'

        constraints_content += '<div class="constraint-subheading">Engineering Constraints</div>'
        if eng_constraints_1:
            eng_pills = ' '.join([f'<span class="constraint-pill eng-constraint-pill">{c}</span>' for c in eng_constraints_1])
            constraints_content += f'<div class="constraints-container">{eng_pills}</div>'
        else:
            constraints_content += '<p style="font-style: italic; opacity: 0.6;">No engineering constraints identified</p>'

        st.markdown(f'<div class="constraints-card">{constraints_content}</div>', unsafe_allow_html=True)

    with col_cc2:
        geo_constraints_2 = get_constraints_for_feature(geological_feature_2, geo_constraints_data)
        eng_constraints_2 = get_constraints_for_feature(geological_feature_2, eng_constraints_data)

        constraints_content = f'<div class="feature-label feature-label-2">{geological_feature_2}</div>'
        constraints_content += '<div class="constraint-subheading">Geological Constraints</div>'
        if geo_constraints_2:
            geo_pills = ' '.join([f'<span class="constraint-pill geo-constraint-pill">{c}</span>' for c in geo_constraints_2])
            constraints_content += f'<div class="constraints-container">{geo_pills}</div>'
        else:
            constraints_content += '<p style="font-style: italic; opacity: 0.6;">No geological constraints identified</p>'

        constraints_content += '<div class="constraint-subheading">Engineering Constraints</div>'
        if eng_constraints_2:
            eng_pills = ' '.join([f'<span class="constraint-pill eng-constraint-pill">{c}</span>' for c in eng_constraints_2])
            constraints_content += f'<div class="constraints-container">{eng_pills}</div>'
        else:
            constraints_content += '<p style="font-style: italic; opacity: 0.6;">No engineering constraints identified</p>'

        st.markdown(f'<div class="constraints-card">{constraints_content}</div>', unsafe_allow_html=True)

    # Foundation Assessment Comparison
    st.markdown(f'<div class="section-header">{create_tooltip("Foundation Assessment Comparison", "Constraint levels for all foundation types for both features")}</div>',
                unsafe_allow_html=True)

    col_fa1, col_fa2 = st.columns(2)

    with col_fa1:
        if feature_data_1 is not None:
            foundation_content = f'<div class="feature-label feature-label-1">{geological_feature_1}</div>'
            for foundation_type in FOUNDATION_TYPES:
                assessment = get_assessment(feature_data_1, foundation_type)
                foundation_content += f"<p><strong>{foundation_type}:</strong> {assessment}</p>"
            st.markdown(f'<div class="section-container">{foundation_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-container"><div class="feature-label feature-label-1">{geological_feature_1}</div><p><strong>No assessment data available</strong></p></div>', unsafe_allow_html=True)

    with col_fa2:
        if feature_data_2 is not None:
            foundation_content = f'<div class="feature-label feature-label-2">{geological_feature_2}</div>'
            for foundation_type in FOUNDATION_TYPES:
                assessment = get_assessment(feature_data_2, foundation_type)
                foundation_content += f"<p><strong>{foundation_type}:</strong> {assessment}</p>"
            st.markdown(f'<div class="section-container">{foundation_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-container"><div class="feature-label feature-label-2">{geological_feature_2}</div><p><strong>No assessment data available</strong></p></div>', unsafe_allow_html=True)

    # Engineering Comments
    st.markdown(f'<div class="section-header">{create_tooltip("Engineering Comments", "Practical guidance and recommendations for offshore wind development")}</div>',
                unsafe_allow_html=True)

    col_e1, col_e2 = st.columns(2)

    with col_e1:
        if feature_data_1 is not None:
            comments_text = feature_data_1['Comments'] if pd.notna(feature_data_1['Comments']) else "No comments available"
            st.markdown(f'<div class="section-container"><div class="feature-label feature-label-1">{geological_feature_1}</div><p>{comments_text}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-container"><div class="feature-label feature-label-1">{geological_feature_1}</div><p>No engineering comments available</p></div>', unsafe_allow_html=True)

    with col_e2:
        if feature_data_2 is not None:
            comments_text = feature_data_2['Comments'] if pd.notna(feature_data_2['Comments']) else "No comments available"
            st.markdown(f'<div class="section-container"><div class="feature-label feature-label-2">{geological_feature_2}</div><p>{comments_text}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-container"><div class="feature-label feature-label-2">{geological_feature_2}</div><p>No engineering comments available</p></div>', unsafe_allow_html=True)

    # References Section
    st.markdown(f'<div class="section-header">{create_tooltip("References", "Academic references and citations for both features")}</div>',
                unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        if feature_data_1 is not None:
            references_text = format_references(feature_data_1.get('References'))
            if references_text:
                st.markdown(f'<div class="references-card"><div class="feature-label feature-label-1">{geological_feature_1}</div><p>{references_text}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="references-card"><div class="feature-label feature-label-1">{geological_feature_1}</div><p style="font-style: italic; opacity: 0.5;">No references available</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="references-card"><div class="feature-label feature-label-1">{geological_feature_1}</div><p style="font-style: italic; opacity: 0.5;">No references available</p></div>', unsafe_allow_html=True)

    with col_r2:
        if feature_data_2 is not None:
            references_text = format_references(feature_data_2.get('References'))
            if references_text:
                st.markdown(f'<div class="references-card"><div class="feature-label feature-label-2">{geological_feature_2}</div><p>{references_text}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="references-card"><div class="feature-label feature-label-2">{geological_feature_2}</div><p style="font-style: italic; opacity: 0.5;">No references available</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="references-card"><div class="feature-label feature-label-2">{geological_feature_2}</div><p style="font-style: italic; opacity: 0.5;">No references available</p></div>', unsafe_allow_html=True)
