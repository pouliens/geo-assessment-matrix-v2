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
        df = pd.read_csv("geological_data_comprehensive.csv")
        return df
    except FileNotFoundError:
        st.error("geological_data_updated.csv not found. Please ensure the data file is in the correct location.")
        return pd.DataFrame()
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV file: {e}")
        return pd.DataFrame()

# Load the data
geological_data = load_geological_data()

# Extract unique values for dropdowns
if not geological_data.empty:
    GEOLOGICAL_FEATURES = sorted(geological_data['Geological_Feature'].dropna().unique().tolist())
    FOUNDATION_TYPES = ["Piles", "Suction Caisson", "GBS", "Cables"]
else:
    GEOLOGICAL_FEATURES = ["No data available"]
    FOUNDATION_TYPES = ["Piles", "Suction Caisson", "GBS", "Cables"]

# Custom CSS for styling
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
    
    .feature1-header {
        background-color: #2E8B57;
        color: white;
    }
    
    .feature2-header {
        background-color: #4682B4;
        color: white;
    }
    
    .comparison-section {
        background-color: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-left: 4px solid #1e4d5b;
    }
    
    .constraint-box {
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    
    .higher-constraint {
        background-color: #ffebee;
        border-color: #f44336;
    }
    
    .moderate-constraint {
        background-color: #fff3e0;
        border-color: #ff9800;
    }
    
    .lower-constraint {
        background-color: #e8f5e8;
        border-color: #4caf50;
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
</style>
""", unsafe_allow_html=True)

def get_feature_data(geological_feature_name):
    """Get geological feature data from CSV."""
    if not geological_data.empty and geological_feature_name in geological_data['Geological_Feature'].values:
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

def get_constraint_class(assessment):
    """Get CSS class for constraint level."""
    assessment_str = str(assessment).lower()
    if "higher constraint" in assessment_str:
        return "higher-constraint"
    elif "moderate constraint" in assessment_str:
        return "moderate-constraint"
    elif "lower constraint" in assessment_str:
        return "lower-constraint"
    else:
        return ""

def get_complexity_level(assessment):
    """Convert assessment to complexity level."""
    assessment_str = str(assessment).lower()
    if "higher constraint" in assessment_str:
        return "High"
    elif "moderate constraint" in assessment_str:
        return "Medium"
    elif "lower constraint" in assessment_str:
        return "Low"
    else:
        return "Unknown"

def get_active_constraints(feature_data):
    """Get list of active geological constraints for a geological feature."""
    if feature_data is None or 'Active_Constraints' not in feature_data:
        return []
    
    constraints_str = feature_data['Active_Constraints']
    if pd.isna(constraints_str) or not constraints_str:
        return []
    
    # Split by semicolon and clean up
    constraints = [c.strip() for c in str(constraints_str).split(';') if c.strip()]
    return constraints

def get_engineering_constraints(feature_data):
    """Get list of engineering constraints for a geological feature."""
    if feature_data is None or 'Engineering_Constraints' not in feature_data:
        return []
    
    constraints_str = feature_data['Engineering_Constraints']
    if pd.isna(constraints_str) or not constraints_str:
        return []
    
    # Split by semicolon and clean up
    constraints = [c.strip() for c in str(constraints_str).split(';') if c.strip()]
    return constraints

def display_constraints(constraints, title):
    """Display active constraints as styled badges."""
    if not constraints:
        st.markdown(f"<p><em>No active {title.lower()} identified</em></p>", unsafe_allow_html=True)
        return
    
    st.markdown(f"<p><strong>{title}:</strong></p>", unsafe_allow_html=True)
    
    # Color mapping for different constraint types
    constraint_colors = {
        'spatial': '#e3f2fd',  # light blue
        'rafts': '#fce4ec',    # light pink  
        'coarse': '#f3e5f5',   # light purple
        'soft': '#e8f5e8',     # light green
        'overconsolidation': '#fff3e0',  # light orange
        'bedrock': '#f5f5f5',  # light gray
        'uneven': '#fff8e1',   # light yellow
        'steep': '#ffebee',    # light red
        'active': '#e0f2f1',   # light teal
        'shallow': '#e1f5fe',  # light cyan
        'deep': '#e8eaf6',     # light indigo
        'fault': '#fce4ec',    # light pink
        'slope': '#f1f8e9',    # light green
        'volcanic': '#ffecb3',  # light amber
        'conduit': '#f3e5f5',  # light purple
        'fluid': '#e0f7fa',    # light cyan
        'organic': '#f9fbe7',  # light lime
        'unknown': '#f5f5f5'   # light gray
    }
    
    # Create badges for each constraint
    badges_html = '<div style="margin: 0.5rem 0;">'
    
    for constraint in constraints:
        # Determine color based on constraint type keywords
        color = constraint_colors['unknown']  # default
        constraint_lower = constraint.lower()
        
        for key, col in constraint_colors.items():
            if key in constraint_lower:
                color = col
                break
        
        badges_html += f'<span style="display: inline-block; padding: 0.3rem 0.6rem; margin: 0.2rem; background-color: {color}; border: 1px solid #ddd; border-radius: 15px; font-size: 0.85rem; font-weight: 500;">{constraint}</span>'
    
    badges_html += '</div>'
    st.markdown(badges_html, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>EGDI - Geological Feature Comparison Tool</h2>
        <div class="nav-links">
            <a href="https://www.europe-geology.eu/" target="_blank">EGDI</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Select Features to Compare")
    st.write("Choose two geological features to compare their engineering constraints for offshore wind development.")
    
    # Feature selection dropdowns
    st.markdown("**First Geological Feature**")
    feature1 = st.selectbox("Feature 1", GEOLOGICAL_FEATURES, key="feature1", label_visibility="collapsed")
    
    st.markdown("**Second Geological Feature**")  
    feature2 = st.selectbox("Feature 2", GEOLOGICAL_FEATURES, index=1 if len(GEOLOGICAL_FEATURES) > 1 else 0, key="feature2", label_visibility="collapsed")
    
    st.markdown("**Foundation Type for Comparison**")
    foundation_type = st.selectbox("Foundation Type", FOUNDATION_TYPES, key="foundation", label_visibility="collapsed")
    
    # Reset button
    if st.button("Reset Selection", use_container_width=True):
        # Clear all session state keys
        for key in ["feature1", "feature2", "foundation"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

with col2:
    if feature1 and feature2:
        # Feature headers
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            st.markdown(f'<div class="foundation-header feature1-header">{feature1}</div>', unsafe_allow_html=True)
        
        with col_f2:
            st.markdown(f'<div class="foundation-header feature2-header">{feature2}</div>', unsafe_allow_html=True)
        
        # Get data for both features
        feature1_data = get_feature_data(feature1)
        feature2_data = get_feature_data(feature2)
        
        # Basic Information
        st.markdown('<div class="section-header">Basic Information</div>', unsafe_allow_html=True)
        
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            if feature1_data is not None:
                st.markdown(f"""
                <div class="comparison-section">
                    <p><strong>Setting:</strong> {feature1_data['Setting']}</p>
                    <p><strong>Process:</strong> {feature1_data['Process']}</p>
                    <p><strong>Dominant Constraint:</strong> {feature1_data['Dominant_Constraint']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="comparison-section"><p>No data available</p></div>', unsafe_allow_html=True)
        
        with col_info2:
            if feature2_data is not None:
                st.markdown(f"""
                <div class="comparison-section">
                    <p><strong>Setting:</strong> {feature2_data['Setting']}</p>
                    <p><strong>Process:</strong> {feature2_data['Process']}</p>
                    <p><strong>Dominant Constraint:</strong> {feature2_data['Dominant_Constraint']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="comparison-section"><p>No data available</p></div>', unsafe_allow_html=True)
        
        # Geological and Engineering Constraints
        st.markdown('<div class="section-header">Geological and Engineering Constraints</div>', unsafe_allow_html=True)
        
        col_con1, col_con2 = st.columns(2)
        
        with col_con1:
            # Get constraints
            geo_constraints1 = get_active_constraints(feature1_data)
            eng_constraints1 = get_engineering_constraints(feature1_data)
            
            constraints_html = '<div class="comparison-section">'
            
            # Geological constraints
            if geo_constraints1:
                constraints_html += '<p><strong>Geological Constraints:</strong></p><div style="margin: 0.5rem 0;">'
                for constraint in geo_constraints1:
                    constraints_html += f'<span style="display: inline-block; padding: 0.3rem 0.6rem; margin: 0.2rem; background-color: #e3f2fd; border: 1px solid #ddd; border-radius: 15px; font-size: 0.85rem; font-weight: 500;">{constraint}</span>'
                constraints_html += '</div>'
            else:
                constraints_html += '<p><strong>Geological Constraints:</strong> <em>None identified</em></p>'
            
            # Engineering constraints
            if eng_constraints1:
                constraints_html += '<p><strong>Engineering Constraints:</strong></p><div style="margin: 0.5rem 0;">'
                for constraint in eng_constraints1:
                    constraints_html += f'<span style="display: inline-block; padding: 0.3rem 0.6rem; margin: 0.2rem; background-color: #fff3e0; border: 1px solid #ddd; border-radius: 15px; font-size: 0.85rem; font-weight: 500;">{constraint}</span>'
                constraints_html += '</div>'
            else:
                constraints_html += '<p><strong>Engineering Constraints:</strong> <em>None identified</em></p>'
            
            constraints_html += '</div>'
            st.markdown(constraints_html, unsafe_allow_html=True)
        
        with col_con2:
            # Get constraints
            geo_constraints2 = get_active_constraints(feature2_data)
            eng_constraints2 = get_engineering_constraints(feature2_data)
            
            constraints_html = '<div class="comparison-section">'
            
            # Geological constraints
            if geo_constraints2:
                constraints_html += '<p><strong>Geological Constraints:</strong></p><div style="margin: 0.5rem 0;">'
                for constraint in geo_constraints2:
                    constraints_html += f'<span style="display: inline-block; padding: 0.3rem 0.6rem; margin: 0.2rem; background-color: #e3f2fd; border: 1px solid #ddd; border-radius: 15px; font-size: 0.85rem; font-weight: 500;">{constraint}</span>'
                constraints_html += '</div>'
            else:
                constraints_html += '<p><strong>Geological Constraints:</strong> <em>None identified</em></p>'
            
            # Engineering constraints
            if eng_constraints2:
                constraints_html += '<p><strong>Engineering Constraints:</strong></p><div style="margin: 0.5rem 0;">'
                for constraint in eng_constraints2:
                    constraints_html += f'<span style="display: inline-block; padding: 0.3rem 0.6rem; margin: 0.2rem; background-color: #fff3e0; border: 1px solid #ddd; border-radius: 15px; font-size: 0.85rem; font-weight: 500;">{constraint}</span>'
                constraints_html += '</div>'
            else:
                constraints_html += '<p><strong>Engineering Constraints:</strong> <em>None identified</em></p>'
            
            constraints_html += '</div>'
            st.markdown(constraints_html, unsafe_allow_html=True)
        
        # Foundation Constraint Comparison
        st.markdown(f'<div class="section-header">{foundation_type} Foundation Assessment</div>', unsafe_allow_html=True)
        
        col_assess1, col_assess2 = st.columns(2)
        
        assessment1 = get_assessment(feature1_data, foundation_type)
        assessment2 = get_assessment(feature2_data, foundation_type)
        
        constraint_class1 = get_constraint_class(assessment1)
        constraint_class2 = get_constraint_class(assessment2)
        
        complexity1 = get_complexity_level(assessment1)
        complexity2 = get_complexity_level(assessment2)
        
        with col_assess1:
            st.markdown(f"""
            <div class="constraint-box {constraint_class1}">
                <p><strong>Assessment:</strong> {assessment1}</p>
                <p><strong>Complexity Level:</strong> {complexity1}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_assess2:
            st.markdown(f"""
            <div class="constraint-box {constraint_class2}">
                <p><strong>Assessment:</strong> {assessment2}</p>
                <p><strong>Complexity Level:</strong> {complexity2}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Definitions
        st.markdown('<div class="section-header">Definitions</div>', unsafe_allow_html=True)
        
        col_def1, col_def2 = st.columns(2)
        
        with col_def1:
            if feature1_data is not None:
                definition1 = feature1_data['Definition'] if pd.notna(feature1_data['Definition']) else "No definition available"
                st.markdown(f"""
                <div class="comparison-section">
                    <p>{definition1}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="comparison-section"><p>No definition available</p></div>', unsafe_allow_html=True)
        
        with col_def2:
            if feature2_data is not None:
                definition2 = feature2_data['Definition'] if pd.notna(feature2_data['Definition']) else "No definition available"
                st.markdown(f"""
                <div class="comparison-section">
                    <p>{definition2}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="comparison-section"><p>No definition available</p></div>', unsafe_allow_html=True)
        
        # Engineering Comments
        st.markdown('<div class="section-header">Engineering Comments</div>', unsafe_allow_html=True)
        
        col_com1, col_com2 = st.columns(2)
        
        with col_com1:
            if feature1_data is not None:
                comments1 = feature1_data['Comments'] if pd.notna(feature1_data['Comments']) else "No comments available"
                st.markdown(f"""
                <div class="comparison-section">
                    <p>{comments1}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="comparison-section"><p>No comments available</p></div>', unsafe_allow_html=True)
        
        with col_com2:
            if feature2_data is not None:
                comments2 = feature2_data['Comments'] if pd.notna(feature2_data['Comments']) else "No comments available"
                st.markdown(f"""
                <div class="comparison-section">
                    <p>{comments2}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="comparison-section"><p>No comments available</p></div>', unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="comparison-section">
            <h3>Welcome to the EGDI Geo-Assessment Matrix</h3>
            <p>This tool helps engineers and developers assess geological constraints for offshore wind development.</p>
            <p>Please select two geological features from the sidebar to begin comparison.</p>
        </div>
        """, unsafe_allow_html=True)