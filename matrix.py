import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="EGDI - Geo-Assessment Matrix",
    page_icon="🌊",
    layout="wide"
)

# Database options from the assessment matrix
SETTINGS = ["Glacial", "Marine", "Fluvial", "Coastal", "Solid Earth"]
PROCESSES = ["Mass movement", "Karst", "Fluid flow", "Biogenic", "Post-depositional"]
CONSTRAINT_TYPES = ["Lithology", "Sediments", "Physiographic"]
FEATURES = ["Rocky coast", "Steep slopes", "Hard substrate", "Soft sediments", "Complex topography"]
FOUNDATION_TYPES = ["Cables", "Pipelines", "Monopile", "Jacket", "Gravity base", "Floating"]

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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2>EGDI</h2>
        <div class="nav-links">
            <a href="#home">Home</a>
            <a href="#about">About</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Geo-Assessment Matrix")
    st.write("""
    Explore the database of surficial and subsurface parameters influencing cost, 
    stability and performance of turbines, cables and hubs in shallow and deep waters.
    """)
    
    st.subheader("Filters")
    
    # Setting & Process filter
    st.write("**Setting & Process** ℹ️")
    col_setting, col_process = st.columns(2)
    with col_setting:
        setting = st.selectbox("Setting", SETTINGS, index=3, key="setting")  # Default to Coastal
    with col_process:
        process = st.selectbox("Process", PROCESSES, key="process")
    
    # Type of constraint filter
    st.write("**Type of constraint** ℹ️")
    constraint_type = st.selectbox("", CONSTRAINT_TYPES, key="constraint")
    
    # Features filter
    st.write("**Features** ℹ️")
    features = st.selectbox("", FEATURES, key="features")
    
    # Foundation type filters
    st.write("**Foundation type 1** ℹ️")
    foundation_type_1 = st.selectbox("", FOUNDATION_TYPES, key="foundation1")
    
    st.write("**Foundation type 2** ℹ️")
    foundation_type_2 = st.selectbox("", FOUNDATION_TYPES, index=1, key="foundation2")  # Default to Pipelines
    
    # Action buttons
    col_reset, col_search = st.columns(2)
    with col_reset:
        if st.button("Reset", use_container_width=True):
            st.rerun()
    with col_search:
        st.button("Search", type="primary", use_container_width=True)

with col2:
    # Parameter tags - now dynamic based on selections
    st.markdown(f"""
    <div class="tags">
        <span class="tag">SETTING: {setting.upper()}</span>
        <span class="tag">PROCESS: {process.upper()}</span>
        <span class="tag">CONSTRAINTS: {constraint_type.upper()}</span>
        <span class="tag">FEATURES: {features.upper()}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Foundation type headers - now dynamic
    col_foundation1, col_foundation2 = st.columns(2)
    
    with col_foundation1:
        header_class = "cables-header" if foundation_type_1.lower() == "cables" else "pipelines-header"
        st.markdown(f'<div class="foundation-header {header_class}">{foundation_type_1}</div>', unsafe_allow_html=True)
    
    with col_foundation2:
        header_class = "cables-header" if foundation_type_2.lower() == "cables" else "pipelines-header"
        st.markdown(f'<div class="foundation-header {header_class}">{foundation_type_2}</div>', unsafe_allow_html=True)
    
    # Potential Geological / Geomorph Constraints
    st.markdown('<div class="section-header">Potential Geological / Geomorph Constraints ℹ️</div>', unsafe_allow_html=True)
    
    col_c1, col_p1 = st.columns(2)
    
    with col_c1:
        with st.container():
            st.markdown("#### LITHOLOGY")
            st.markdown("**Hard soils:** Hard substrate")
            st.markdown("#### RELIEF")
            st.markdown("**Morphology:** Steep slopes/margins (>5 degrees)")
    
    with col_p1:
        with st.container():
            st.markdown("#### LITHOLOGY")
            st.markdown("**Hard soils:** Hard substrate")
            st.markdown("#### RELIEF")
            st.markdown("**Morphology:** Steep slopes/margins (>5 degrees)")
    
    # Potential Principal Engineering Significance
    st.markdown('<div class="section-header">Potential Principal Engineering Significance (Pre- Or During Installation) ℹ️</div>', unsafe_allow_html=True)
    
    col_c2, col_p2 = st.columns(2)
    
    with col_c2:
        st.markdown("""
        <div class="parameter-section">
            <p><strong>All:</strong> Requires individual WTG siting investigation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p2:
        st.markdown("""
        <div class="parameter-section">
            <p><strong>All:</strong> Requires individual WTG siting investigation</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Geological Complexity Assessment
    st.markdown('<div class="section-header">Geological Complexity Assessment ℹ️</div>', unsafe_allow_html=True)
    
    col_c3, col_p3 = st.columns(2)
    
    with col_c3:
        st.markdown("""
        <div class="parameter-section">
            <p><strong>Medium</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p3:
        st.markdown("""
        <div class="parameter-section">
            <p><strong>Medium</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Comments
    st.markdown('<div class="section-header">Comments ℹ️</div>', unsafe_allow_html=True)
    
    col_c4, col_p4 = st.columns(2)
    
    with col_c4:
        st.markdown("""
        <div class="parameter-section">
            <p>Lorem ipsum dolor sit amet consectetur. Aliquam tortor vestibulum praesent enim purus cursus. In facilisi commodo enim ipsum. Non rhoncus aliquam lacus ac ac commodo. Morbi turpis praesent dui parturient est aliquet. In aenean imperdiet in nunc tortor volutpat dignissim. Luctus accumsan orci condimentum id. Adipiscing eu at maecenas luctus egestas maecenas a adipiscing lacus. Semper tristique a faucibus lectus. Diam massa libero faucibus pharetra mauris ornare ut.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_p4:
        st.markdown("""
        <div class="parameter-section">
            <p>Lorem ipsum dolor sit amet consectetur. Aliquam tortor vestibulum praesent enim purus cursus. In facilisi commodo enim ipsum. Non rhoncus aliquam lacus ac ac commodo. Morbi turpis praesent dui parturient est aliquet. In aenean imperdiet in nunc tortor volutpat dignissim. Luctus accumsan orci condimentum id. Adipiscing eu at maecenas luctus egestas maecenas a adipiscing lacus. Semper tristique a faucibus lectus. Diam massa libero faucibus pharetra mauris ornare ut.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Download Report button
    st.markdown("<br>", unsafe_allow_html=True)
    col_empty, col_download = st.columns([3, 1])
    with col_download:
        st.button("Download Report", use_container_width=True)

# Sidebar for additional functionality (optional)
with st.sidebar:
    st.header("Assessment Options")
    st.write("Configure your foundation assessment parameters:")
    
    water_depth = st.slider("Water Depth (m)", 0, 200, 50)
    wind_speed = st.slider("Average Wind Speed (m/s)", 5, 25, 15)
    soil_type = st.selectbox("Primary Soil Type", ["Clay", "Sand", "Rock", "Mixed"])
    
    st.write("---")
    st.write("**Quick Actions:**")
    if st.button("Export Data", use_container_width=True):
        st.success("Data exported successfully!")
    
    if st.button("Generate Report", use_container_width=True):
        st.success("Report generated!")