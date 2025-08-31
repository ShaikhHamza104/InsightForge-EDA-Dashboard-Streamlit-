import streamlit as st
import pandas as pd
import overview
import univariate_analysis
import bivariate_analysis
import numpy as np
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="InsightForge — EDA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
        margin-top: 1rem;
    }
    .info-text {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1E88E5;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .upload-section {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 2px dashed #1E88E5;
    }
    .metric-container {
        background-color: #FFFFFF;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1E88E5;
    }
    .sidebar .css-1d391kg {
        background-color: #E3F2FD;
    }
    .about-section {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Load sample dataset with caching for better performance"""
    try:
        return pd.read_csv('https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/refs/heads/master/laptop_cleaning.csv')
    except Exception as e:
        st.error(f"Error loading sample data: {str(e)}")
        return None

def load_data():
    """Handle data loading from file upload or sample dataset"""
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📁 Choose a CSV file", 
        type="csv",
        help="Upload your CSV file for analysis. Maximum file size: 200MB"
    )
    
    # Option to use sample data
    use_sample = st.checkbox("🔬 Use sample laptop dataset instead", value=False)
    
    if use_sample:
        st.info("💡 **Sample Dataset**: Laptop specifications and prices for demonstration")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Show file details
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": f"{uploaded_file.size / 1024:.2f} KB"
            }
            st.success(f"✅ Loaded: {file_details['filename']} ({file_details['filesize']})")
            
            df = pd.read_csv(uploaded_file)
            return df
        except UnicodeDecodeError:
            st.error("❌ Encoding error. Try saving your CSV as UTF-8 encoding.")
            return None
        except pd.errors.EmptyDataError:
            st.error("❌ The uploaded file is empty.")
            return None
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")
            return None
    elif use_sample:
        st.info("📊 Loading sample laptop dataset...")
        return load_sample_data()
    else:
        return None

def display_dataset_metrics(df):
    """Display key dataset metrics in an attractive format"""
    st.markdown('<div class="info-text">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("📈 Columns", f"{df.shape[1]}")
    with col3:
        missing_count = df.isna().sum().sum()
        st.metric("⚠️ Missing Values", f"{missing_count:,}")
    with col4:
        memory_usage = df.memory_usage(deep=True).sum() / 1024**2
        st.metric("💾 Memory Usage", f"{memory_usage:.1f} MB")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main app header
st.markdown('<h1 class="main-header">📊 InsightForge — EDA Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Analyze datasets quickly with interactive Overview, Univariate, and Bivariate visualizations</p>', unsafe_allow_html=True)

# Sidebar for navigation with better styling
with st.sidebar:
    st.markdown('<h2 style="text-align: center; color: #1E88E5;">📊 InsightForge</h2>', unsafe_allow_html=True)
    
    analysis_type = st.radio(
        "🎯 Select Analysis Type",
        ("📋 Overview", "📊 Univariate Analysis", "📈 Bivariate Analysis"),
        index=0,
        help="Choose the type of analysis you want to perform"
    )
    
    st.markdown('---')
    
    # About section in sidebar
    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown('### 🚀 Features')
    st.markdown("""
    - **📋 Overview**: Dataset summary, statistics, correlations
    - **📊 Univariate**: Single variable analysis
    - **📈 Bivariate**: Relationship analysis
    - **🎨 Interactive**: Plotly-powered visualizations
    - **⚡ Fast**: Optimized for performance
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('---')
    st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #666;">Built with ❤️ using Streamlit</p>', unsafe_allow_html=True)

# Load data
df = load_data()

if df is not None and not df.empty:
    # Display dataset metrics
    display_dataset_metrics(df)
    
    # Add a separator
    st.markdown("---")
    
    # Route to appropriate analysis based on selection
    if analysis_type == '📋 Overview':
        try:
            overview_instance = overview.Overview(df)
            overview_instance.display_overview()
        except Exception as e:
            st.error(f"❌ Error in Overview analysis: {str(e)}")
        
    elif analysis_type == "📊 Univariate Analysis":
        try:
            univariate = univariate_analysis.UnivariateAnalysis(df)
            univariate.display()
        except Exception as e:
            st.error(f"❌ Error in Univariate analysis: {str(e)}")

    elif analysis_type == "📈 Bivariate Analysis":
        try:
            bivariate = bivariate_analysis.BivariateAnalysis(df)
            bivariate.column_vs_column_display()
        except Exception as e:
            st.error(f"❌ Error in Bivariate analysis: {str(e)}")
else:
    # Welcome screen with instructions
    st.markdown('<div class="info-text">', unsafe_allow_html=True)
    
    if df is None:
        st.info("👋 **Welcome to InsightForge!** Please upload a CSV file or use the sample dataset to begin analysis.")
    else:
        st.warning("⚠️ The uploaded dataset appears to be empty. Please check your file and try again.")
    
    st.markdown("""
    ### 🎯 What can you do here?
    
    **📋 Overview Analysis**
    - Get dataset shape, preview, and summary statistics
    - Identify missing values and data types
    - View correlation heatmaps for numerical features
    
    **📊 Univariate Analysis**
    - **Numerical**: Histograms, Box plots, Density plots, Scatter plots
    - **Categorical**: Count plots, Pie charts, Bar plots
    - Smart null value handling with clear warnings
    
    **📈 Bivariate Analysis**
    - **Numerical vs Numerical**: Scatter, Line, Box, Density, Correlation heatmaps
    - **Categorical vs Categorical**: Grouped bars, Cross-tabulation heatmaps
    - **Numerical vs Categorical**: Box plots, Violin plots, Mean comparison bars
    - Category limiting for high-cardinality columns
    
    ### 🚀 Quick Start
    1. **Upload your CSV** using the file uploader above
    2. **Or try the sample dataset** by checking the checkbox
    3. **Navigate** using the sidebar to explore different analysis types
    4. **Interact** with the visualizations and adjust parameters as needed
    
    ### 💡 Tips
    - For large datasets, visualizations are automatically optimized
    - Missing values are handled gracefully with warnings
    - Use category limiting sliders for columns with many unique values
    """)
    st.markdown('</div>', unsafe_allow_html=True)
