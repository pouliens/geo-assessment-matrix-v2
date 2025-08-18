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
    st.header("Geological Assessment")
    st.write("""
    Explore geological features and their engineering constraints for offshore windfarm development. 
    Compare foundation types and assess geological risks for optimal site selection.
    """)
    
    st.subheader("Filters")
    
    # Setting & Process filter with tooltips
    st.markdown(create_tooltip("**Setting & Process**", 
                              "Setting: Geological environment where the feature occurs (e.g., Glacial, Marine, Coastal)<br>"
                              "Process: Geological process that formed the feature (e.g., Lithology, Relief, Structure)"), 
                unsafe_allow_html=True)
    
    col_setting, col_process = st.columns(2)
    with col_setting:
        setting = st.selectbox("Setting", ["All"] + SETTINGS, key="setting", label_visibility="collapsed")
    with col_process:
        process = st.selectbox("Process", ["All"] + PROCESSES, key="process", label_visibility="collapsed")
    
    # Type of constraint filter with tooltip
    st.markdown(create_tooltip("**Type of Constraint**", 
                              "Primary geological constraint category affecting foundation installation and performance"), 
                unsafe_allow_html=True)
    constraint_type = st.selectbox("Constraint Type", ["All"] + CONSTRAINT_TYPES, key="constraint", label_visibility="collapsed")
    
    # Geological Features filter with tooltip
    filtered_features = filter_geological_features(setting, process, constraint_type)
    st.markdown(create_tooltip("**Geological Features**", 
                              "Specific geological features filtered based on your selected criteria above"), 
                unsafe_allow_html=True)
    geological_feature = st.selectbox("Geological Feature", 
                                    filtered_features if filtered_features else ["No features match criteria"], 
                                    key="geological_feature", label_visibility="collapsed")
    
    # Foundation type filters with tooltips
    st.markdown(create_tooltip("**Foundation Type 1**", 
                              "First foundation type for comparison<br>"
                              "• Piles: Driven steel tube foundations<br>"
                              "• Suction Caisson: Large steel buckets with suction installation<br>"
                              "• GBS: Gravity-based concrete structures<br>"
                              "• Cables: Subsea power transmission cables"), 
                unsafe_allow_html=True)
    foundation_type_1 = st.selectbox("Foundation Type 1", FOUNDATION_TYPES, key="foundation1", label_visibility="collapsed")
    
    st.markdown(create_tooltip("**Foundation Type 2**", 
                              "Second foundation type for comparison"), 
                unsafe_allow_html=True)
    foundation_type_2 = st.selectbox("Foundation Type 2", FOUNDATION_TYPES, index=1, key="foundation2", label_visibility="collapsed")
    
    # Action buttons
    if st.button("Reset Filters", use_container_width=True):
        st.rerun()

with col2:
    # Parameter tags showing current selections
    st.markdown(f"""
    <div class="tags">
        <span class="tag">SETTING: {setting.upper()}</span>
        <span class="tag">PROCESS: {process.upper()}</span>
        <span class="tag">CONSTRAINT: {constraint_type.upper()}</span>
        <span class="tag">FEATURE: {geological_feature.upper()}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Foundation type headers
    col_foundation1, col_foundation2 = st.columns(2)
    
    with col_foundation1:
        header_class = get_foundation_header_class(foundation_type_1)
        st.markdown(f'<div class="foundation-header {header_class}">{foundation_type_1}</div>', unsafe_allow_html=True)
    
    with col_foundation2:
        header_class = get_foundation_header_class(foundation_type_2)
        st.markdown(f'<div class="foundation-header {header_class}">{foundation_type_2}</div>', unsafe_allow_html=True)
    
    # Get data for selected geological feature
    feature_data = get_feature_data(geological_feature)
    
    # Geological Constraints section with tooltip
    st.markdown(f'<div class="section-header">{create_tooltip("Geological Constraints", "Key geological characteristics and dominant constraints for the selected feature")}</div>', 
                unsafe_allow_html=True)
    
    col_c1, col_p1 = st.columns(2)
    
    with col_c1:
        if feature_data is not None:
            st.markdown(f"**Setting:** {feature_data['Setting']}")
            st.markdown(f"**Process:** {feature_data['Process']}")
            st.markdown(f"**Constraint Type:** {feature_data['Constraint_Type']}")
            st.markdown(f"**Dominant Constraint:** {feature_data['Dominant_Constraint']}")
        else:
            st.markdown("**No data available for selected feature**")
    
    with col_p1:
        if feature_data is not None:
            definition_text = feature_data['Definition'] if pd.notna(feature_data['Definition']) else "No definition available"
            st.markdown(f"**Definition:** {definition_text}")
        else:
            st.markdown("**No definition available**")
    
    # Engineering Significance section with tooltip
    st.markdown(f'<div class="section-header">{create_tooltip("Engineering Significance", "Constraint levels for foundation installation and performance (Higher/Moderate/Lower Constraint)")}</div>', 
                unsafe_allow_html=True)
    
    col_c2, col_p2 = st.columns(2)
    
    assessment_1 = get_assessment(feature_data, foundation_type_1)
    assessment_2 = get_assessment(feature_data, foundation_type_2)
    
    with col_c2:
        st.markdown(f"""
        <div class="parameter-section">
            <p><strong>{foundation_type_1}:</strong> {assessment_1}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p2:
        st.markdown(f"""
        <div class="parameter-section">
            <p><strong>{foundation_type_2}:</strong> {assessment_2}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Complexity Assessment section with tooltip
    st.markdown(f'<div class="section-header">{create_tooltip("Complexity Assessment", "Overall geological complexity level based on constraint assessments")}</div>', 
                unsafe_allow_html=True)
    
    col_c3, col_p3 = st.columns(2)
    
    complexity_1 = get_complexity_level(assessment_1)
    complexity_2 = get_complexity_level(assessment_2)
    
    with col_c3:
        st.markdown(f"""
        <div class="parameter-section">
            <p><strong>Complexity Level:</strong> {complexity_1}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p3:
        st.markdown(f"""
        <div class="parameter-section">
            <p><strong>Complexity Level:</strong> {complexity_2}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Engineering Comments section with tooltip
    st.markdown(f'<div class="section-header">{create_tooltip("Engineering Comments", "Practical guidance and recommendations for offshore wind development")}</div>', 
                unsafe_allow_html=True)
    
    if feature_data is not None:
        comments_text = feature_data['Comments'] if pd.notna(feature_data['Comments']) else "No comments available"
        st.markdown(f"""
        <div class="parameter-section">
            <p>{comments_text}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="parameter-section">
            <p>No engineering comments available for the selected feature.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Download Report button
    st.markdown("<br>", unsafe_allow_html=True)
    col_empty, col_download = st.columns([3, 1])
    with col_download:
        if st.button("Download Report", use_container_width=True):
            st.info("Report generation feature coming soon!")