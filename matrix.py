import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="EGDI - Geo-Assessment Matrix",
    page_icon="🌊",
    layout="wide"
)

# Load geological data
@st.cache_data
def load_geological_data():
    """Load geological data from CSV file with proper error handling."""
    try:
        df = pd.read_csv("geological_data.csv")
        return df
    except FileNotFoundError:
        st.error("geological_data.csv not found. Please ensure the data file is in the correct location.")
        return pd.DataFrame()
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV file: {e}")
        return pd.DataFrame()

# Load the data
geological_data = load_geological_data()

# Extract unique values for filters from the data
if not geological_data.empty:
    SETTINGS = sorted(geological_data['Setting'].dropna().unique().tolist())
    PROCESSES = sorted(geological_data['Process'].dropna().unique().tolist())
    CONSTRAINT_TYPES = sorted(geological_data['Constraint_Type'].dropna().unique().tolist())
    GEOLOGICAL_FEATURES = sorted(geological_data['Geological_Feature'].dropna().unique().tolist())
    FOUNDATION_TYPES = ["Piles", "Suction Caisson", "GBS", "Cables"]
else:
    # Fallback options if data can't be loaded
    SETTINGS = ["Glacial", "Marine", "Fluvial", "Coastal", "Solid Earth"]
    PROCESSES = ["Mass movement", "Karst", "Fluid flow", "Biogenic", "Post-depositional"]
    CONSTRAINT_TYPES = ["Lithology", "Relief", "Structure", "Geohazard"]
    GEOLOGICAL_FEATURES = ["Rocky coast", "Steep slopes", "Hard substrate", "Soft sediments"]
    FOUNDATION_TYPES = ["Piles", "Suction Caisson", "GBS", "Cables"]

# Custom CSS for styling with improved spacing
st.markdown("""
<style>
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
    
    .section-header {
        background-color: #1e4d5b;
        color: white;
        padding: 0.5rem;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
    
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
    
    .parameter-section {
        background-color: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .tags {
        margin: 1rem 0;
    }
    
    .tag {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border: 1px solid #6c757d;
        border-radius: 20px;
        background-color: #f8f9fa;
        font-size: 0.9rem;
    }
    
    /* Remove all paragraph margins globally */
    p {
        margin-bottom: 0.5rem !important;
        margin-top: 0rem !important;
    }
    
    /* Remove margins from all Streamlit form elements */
    .stSelectbox, .stSelectbox > label, .stSelectbox > div {
        margin-top: 0rem !important;
        margin-bottom: 0rem !important;
    }
    
    /* Add pointer cursor to dropdown elements */
    .stSelectbox > div > div {
        cursor: pointer !important;
    }
    
    /* Center text in buttons */
    .stButton > button {
        text-align: center !important;
    }
    
    /* Remove margin from paragraphs inside buttons */
    .stButton > button p {
        margin-bottom: 0rem !important;
        margin-top: 0rem !important;
    }
    
    /* Add margin-top to sidebar buttons */
    .stColumn .stButton {
        margin-top: 1rem !important;
    }
    
    /* Custom tooltip styling */
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

def create_tooltip(text, tooltip_content):
    """Create a tooltip with hover functionality."""
    return f"""
    <span class="tooltip">{text}
        <span class="tooltiptext">{tooltip_content}</span>
    </span>
    """

def get_feature_data(geological_feature_name):
    """Get geological feature data from CSV."""
    if not geological_data.empty and geological_feature_name != "No features match criteria":
        feature_data = geological_data[geological_data['Geological_Feature'] == geological_feature_name]
        if not feature_data.empty:
            return feature_data.iloc[0]
    return None

def get_assessment(feature_data, foundation_type):
    """Get constraint assessment for foundation type."""
    if feature_data is None:
        return "Data not available"
    
    assessment_mapping = {
        "Piles": "Piles_Assessment",
        "Suction Caisson": "Suction_Caisson_Assessment", 
        "GBS": "GBS_Assessment",
        "Cables": "Cables_Assessment"
    }
    
    col_name = assessment_mapping.get(foundation_type)
    if col_name and col_name in feature_data:
        return feature_data[col_name] if pd.notna(feature_data[col_name]) else "No assessment available"
    return "Assessment not available"

def get_complexity_level(assessment):
    """Convert assessment to complexity level."""
    if "Higher Constraint" in str(assessment):
        return "High"
    elif "Moderate constraint" in str(assessment):
        return "Medium"
    elif "Lower Constraint" in str(assessment):
        return "Low"
    else:
        return "Unknown"

def filter_geological_features(setting, process, constraint_type):
    """Filter geological features based on selected criteria."""
    if geological_data.empty:
        return GEOLOGICAL_FEATURES
    
    filtered_data = geological_data.copy()
    
    if setting != "All":
        filtered_data = filtered_data[filtered_data['Setting'] == setting]
    if process != "All":
        filtered_data = filtered_data[filtered_data['Process'] == process]
    if constraint_type != "All":
        filtered_data = filtered_data[filtered_data['Constraint_Type'] == constraint_type]
    
    return sorted(filtered_data['Geological_Feature'].dropna().unique().tolist())

def get_foundation_header_class(foundation_type):
    """Get CSS class for foundation header styling."""
    if foundation_type.lower() == "cables":
        return "cables-header"
    elif foundation_type.lower() in ["pipelines", "suction caisson", "piles", "gbs"]:
        return "pipelines-header"
    else:
        return "cables-header"

# Header
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

# Main layout
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Geological Comparison")
    st.write("""
    Compare two geological features and their engineering constraints for offshore windfarm development.
    """)
    
    st.subheader("Feature Selection")
    
    # Geological Feature 1
    st.markdown("**Geological Feature 1**")
    geological_feature_1 = st.selectbox("Feature 1", GEOLOGICAL_FEATURES, key="feature1", label_visibility="collapsed")
    
    # Geological Feature 2
    st.markdown("**Geological Feature 2**") 
    geological_feature_2 = st.selectbox("Feature 2", GEOLOGICAL_FEATURES, index=1 if len(GEOLOGICAL_FEATURES) > 1 else 0, key="feature2", label_visibility="collapsed")
    
    # Action buttons
    if st.button("Reset Selection", use_container_width=True):
        # Clear all session state keys for features
        for key in ["feature1", "feature2"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

with col2:
    # Feature comparison headers
    col_feature1, col_feature2 = st.columns(2)
    
    with col_feature1:
        st.markdown(f'<div class="foundation-header cables-header">{geological_feature_1}</div>', unsafe_allow_html=True)
    
    with col_feature2:
        st.markdown(f'<div class="foundation-header pipelines-header">{geological_feature_2}</div>', unsafe_allow_html=True)
    
    # Get data for both selected geological features
    feature_data_1 = get_feature_data(geological_feature_1)
    feature_data_2 = get_feature_data(geological_feature_2)
    
    # Geological Constraints section with tooltip
    st.markdown(f'<div class="section-header">{create_tooltip("Geological Characteristics", "Key geological characteristics for both selected features")}</div>', 
                unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        if feature_data_1 is not None:
            st.markdown(f"**Setting:** {feature_data_1['Setting']}")
            st.markdown(f"**Process:** {feature_data_1['Process']}")
            st.markdown(f"**Constraint Type:** {feature_data_1['Constraint_Type']}")
            st.markdown(f"**Dominant Constraint:** {feature_data_1['Dominant_Constraint']}")
        else:
            st.markdown("**No data available for Feature 1**")
    
    with col_c2:
        if feature_data_2 is not None:
            st.markdown(f"**Setting:** {feature_data_2['Setting']}")
            st.markdown(f"**Process:** {feature_data_2['Process']}")
            st.markdown(f"**Constraint Type:** {feature_data_2['Constraint_Type']}")
            st.markdown(f"**Dominant Constraint:** {feature_data_2['Dominant_Constraint']}")
        else:
            st.markdown("**No data available for Feature 2**")
    
    # Foundation Assessment Comparison
    st.markdown(f'<div class="section-header">{create_tooltip("Foundation Assessment Comparison", "Constraint levels for all foundation types for both features")}</div>', 
                unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        if feature_data_1 is not None:
            for foundation_type in FOUNDATION_TYPES:
                assessment = get_assessment(feature_data_1, foundation_type)
                st.markdown(f"**{foundation_type}:** {assessment}")
        else:
            st.markdown("**No assessment data available**")
    
    with col_f2:
        if feature_data_2 is not None:
            for foundation_type in FOUNDATION_TYPES:
                assessment = get_assessment(feature_data_2, foundation_type)
                st.markdown(f"**{foundation_type}:** {assessment}")
        else:
            st.markdown("**No assessment data available**")
    
    # Definitions section
    st.markdown(f'<div class="section-header">{create_tooltip("Feature Definitions", "Scientific descriptions of both geological features")}</div>', 
                unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        if feature_data_1 is not None:
            definition_text = feature_data_1['Definition'] if pd.notna(feature_data_1['Definition']) else "No definition available"
            st.markdown(f"""
            <div class="parameter-section">
                <p>{definition_text}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="parameter-section">
                <p>No definition available</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_d2:
        if feature_data_2 is not None:
            definition_text = feature_data_2['Definition'] if pd.notna(feature_data_2['Definition']) else "No definition available"
            st.markdown(f"""
            <div class="parameter-section">
                <p>{definition_text}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="parameter-section">
                <p>No definition available</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Engineering Comments section
    st.markdown(f'<div class="section-header">{create_tooltip("Engineering Comments", "Practical guidance and recommendations for offshore wind development")}</div>', 
                unsafe_allow_html=True)
    
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        if feature_data_1 is not None:
            comments_text = feature_data_1['Comments'] if pd.notna(feature_data_1['Comments']) else "No comments available"
            st.markdown(f"""
            <div class="parameter-section">
                <p>{comments_text}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="parameter-section">
                <p>No engineering comments available</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_e2:
        if feature_data_2 is not None:
            comments_text = feature_data_2['Comments'] if pd.notna(feature_data_2['Comments']) else "No comments available"
            st.markdown(f"""
            <div class="parameter-section">
                <p>{comments_text}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="parameter-section">
                <p>No engineering comments available</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Download Report button
    st.markdown("<br>", unsafe_allow_html=True)
    col_empty, col_download = st.columns([3, 1])
    with col_download:
        if st.button("Download Report", use_container_width=True):
            st.info("Report generation feature coming soon!")