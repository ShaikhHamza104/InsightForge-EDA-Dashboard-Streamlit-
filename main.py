import streamlit as st
import pandas as pd
import overview
import univariate_analysis
import bivariate_analysis
import numpy as np
import warnings
import requests
from basic_data_clean import BasicDataClean
from data_export import DataExporter  
import base64
import json
import io

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
    .export-section {
        background-color: #F0F8FF;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 2px solid #1E88E5;
    }
    .export-button {
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        margin: 4px 2px;
        font-size: 14px;
    }
    .export-button:hover {
        background-color: #45a049;
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

def get_download_link(data, filename, file_type):
    """Generate download link for any file type"""
    if isinstance(data, str):
        data = data.encode()
    
    b64 = base64.b64encode(data).decode()
    
    mime_types = {
        'csv': 'text/csv',
        'tsv': 'text/tab-separated-values',
        'json': 'application/json',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    
    mime_type = mime_types.get(file_type, 'application/octet-stream')
    
    return f'''
    <a href="data:{mime_type};base64,{b64}" 
       download="{filename}" 
       class="export-button">
        📥 Download {file_type.upper()}
    </a>
    '''

def display_export_interface(df, data_type="cleaned"):
    """Display export interface for cleaned data"""
    st.markdown('<div class="export-section">', unsafe_allow_html=True)
    st.subheader(f"📤 Export {data_type.title()} Data")
    st.write("Choose your preferred format to download the data:")
    
    if df is None or df.empty:
        st.warning("⚠️ No data available for export.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    exporter = DataExporter(df)
    
    # Create export options in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📄 Text Formats**")
        
        # CSV Export
        if st.button("📊 Export as CSV", key=f"csv_btn_{data_type}"):
            csv_data = exporter.to_csv()
            filename = f"{data_type}_data_{exporter.timestamp}.csv"
            st.markdown(get_download_link(csv_data, filename, 'csv'), unsafe_allow_html=True)
            st.success("✅ CSV file ready for download!")
        
        # TSV Export
        if st.button("📋 Export as TSV", key=f"tsv_btn_{data_type}"):
            tsv_data = exporter.to_tsv()
            filename = f"{data_type}_data_{exporter.timestamp}.tsv"
            st.markdown(get_download_link(tsv_data, filename, 'tsv'), unsafe_allow_html=True)
            st.success("✅ TSV file ready for download!")
    
    with col2:
        st.markdown("**🗂️ Structured Formats**")
        
        # JSON Export
        if st.button("🔗 Export as JSON", key=f"json_btn_{data_type}"):
            json_data = exporter.to_json()
            filename = f"{data_type}_data_{exporter.timestamp}.json"
            st.markdown(get_download_link(json_data, filename, 'json'), unsafe_allow_html=True)
            st.success("✅ JSON file ready for download!")
        
        # Excel Export
        if st.button("📈 Export as Excel", key=f"excel_btn_{data_type}"):
            try:
                excel_data = exporter.to_excel()
                filename = f"{data_type}_data_{exporter.timestamp}.xlsx"
                st.markdown(get_download_link(excel_data, filename, 'xlsx'), unsafe_allow_html=True)
                st.success("✅ Excel file ready for download!")
            except Exception as e:
                st.error(f"❌ Error creating Excel file: {str(e)}")
    
    with col3:
        st.markdown("**📊 Data Summary**")
        st.metric("📈 Total Rows", len(df))
        st.metric("📊 Total Columns", len(df.columns))
        memory_usage = df.memory_usage(deep=True).sum() / 1024
        st.metric("💾 Memory", f"{memory_usage:.1f} KB")
    
    # Custom export options
    with st.expander("🔧 Advanced Export Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**CSV Custom Options**")
            include_index = st.checkbox("Include Index", value=False, key=f"index_{data_type}")
            separator = st.selectbox("Separator", [',', ';', '|', '\t'], index=0, key=f"sep_{data_type}")
            
            if st.button("📊 Export Custom CSV", key=f"custom_csv_{data_type}"):
                csv_data = exporter.to_csv(index=include_index, separator=separator)
                filename = f"{data_type}_data_custom_{exporter.timestamp}.csv"
                st.markdown(get_download_link(csv_data, filename, 'csv'), unsafe_allow_html=True)
                st.success("✅ Custom CSV file ready!")
        
        with col2:
            st.markdown("**JSON Custom Options**")
            json_orient = st.selectbox("JSON Orientation", 
                                     ['records', 'index', 'values', 'columns'], 
                                     index=0, key=f"json_orient_{data_type}")
            
            if st.button("🔗 Export Custom JSON", key=f"custom_json_{data_type}"):
                json_data = exporter.to_json(orient=json_orient)
                filename = f"{data_type}_data_custom_{exporter.timestamp}.json"
                st.markdown(get_download_link(json_data, filename, 'json'), unsafe_allow_html=True)
                st.success("✅ Custom JSON file ready!")
    
    # Data Preview
    with st.expander("👀 Preview Data (First 5 rows)"):
        st.dataframe(df.head(), use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def load_data():
    """Handle data loading from file upload, URL, API, or sample dataset"""
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    input_method = st.radio(
        "Select Data Source",
        ('Upload a File', 'From Website URL', 'From API', 'Use Sample Data'),
        horizontal=True,
        key='data_source'
    )

    df = None

    if input_method == 'Upload a File':
        uploaded_file = st.file_uploader(
            "📁 Choose a CSV or TSV file", 
            type=['csv', 'tsv'],
            help="Upload your CSV or TSV file for analysis. Maximum file size: 200MB"
        )
        if uploaded_file:
            try:
                file_details = {
                    "filename": uploaded_file.name,
                    "filetype": uploaded_file.type,
                    "filesize": f"{uploaded_file.size / (1024*1024):.2f} MB"
                }
                st.success(f"✅ Loaded: {file_details['filename']} ({file_details['filesize']})")
                
                separator = ',' if uploaded_file.name.endswith('.csv') else '\t'
                df = pd.read_csv(uploaded_file, sep=separator)
            except UnicodeDecodeError:
                st.error("❌ Encoding error. Try saving your file as UTF-8.")
            except Exception as e:
                st.error(f"❌ Error loading file: {e}")
    
    elif input_method == 'From Website URL':
        url = st.text_input("Enter URL to fetch table data from:", placeholder="e.g., https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)")
        if url:
            try:
                with st.spinner('Fetching tables from URL...'):
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    tables = pd.read_html(response.text)
                
                if tables:
                    st.success(f"✅ Found {len(tables)} table(s) on the page.")
                    table_options = [f"Table {i+1} (Shape: {t.shape})" for i, t in enumerate(tables)]
                    selected_table_index = st.selectbox("Select a table to analyze:", range(len(tables)), format_func=lambda i: table_options[i])
                    df = tables[selected_table_index]
                else:
                    st.warning("⚠️ No tables found on the provided URL.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Could not retrieve URL: {e}")
            except Exception as e:
                st.error(f"❌ Error parsing tables from URL: {e}")

    elif input_method == 'From API':
        api_url = st.text_input("Enter the API endpoint URL:", placeholder="e.g., https://api.publicapis.org/entries")
        if st.button("Fetch Data from API") and api_url:
            try:
                with st.spinner('Fetching data from API...'):
                    response = requests.get(api_url, timeout=10)
                    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                    data = response.json()
                    
                    if isinstance(data, list):
                        df = pd.DataFrame(data)
                    elif isinstance(data, dict):
                        # Attempt to find a list of records within the JSON response
                        list_key = next((key for key, value in data.items() if isinstance(value, list)), None)
                        if list_key:
                            st.info(f"Found a list of records under the key: '{list_key}'")
                            df = pd.json_normalize(data, record_path=list_key)
                        else:
                            df = pd.json_normalize(data)
                    else:
                        st.error("❌ The API did not return a standard JSON list or dictionary format.")
                    
                    if df is not None:
                        st.success("✅ Successfully loaded data from API.")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Could not retrieve data from API: {e}")
            except ValueError:  # Catches JSON decoding errors
                st.error("❌ Failed to decode JSON from the API response. Please check the URL and API documentation.")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")

    elif input_method == 'Use Sample Data':
        st.info("💡 **Sample Dataset**: Laptop specifications and prices for demonstration. Loading...")
        df = load_sample_data()

    st.markdown('</div>', unsafe_allow_html=True)
    return df


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
        ("📋 Overview", "📊 Univariate Analysis", "📈 Bivariate Analysis", "🧹 Data Cleaning", "📤 Export Data"),
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
    - **🧹 Data Cleaning**: Handle missing values, outliers
    - **📤 Export Data**: Multiple format downloads
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

    elif analysis_type == "📤 Export Data":
        try:
            # Check if cleaned data is available
            if 'cleaned_df' in st.session_state:
                cleaned_data = st.session_state['cleaned_df']
                
                # Tabs for original and cleaned data export
                tab1, tab2 = st.tabs(["📋 Original Data", "✨ Cleaned Data"])
                
                with tab1:
                    st.subheader("📋 Export Original Data")
                    display_export_interface(df, "original")
                
                with tab2:
                    st.subheader("✨ Export Cleaned Data")
                    display_export_interface(cleaned_data, "cleaned")
            else:
                # Only original data available
                st.subheader("📋 Export Current Data")
                display_export_interface(df, "current")
                
                st.info("💡 **Tip**: Clean your data first to have both original and cleaned export options!")
                
        except Exception as e:
            st.error(f"❌ Error in Export functionality: {str(e)}")

    elif analysis_type == "🧹 Data Cleaning":
        try:
            cleaner = BasicDataClean(df)

            # Add data cleaning options in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🧹 Missing Values", "🗑️ Drop Columns", "📊 High Missing Columns", "📤 Export"])

            with tab1:
                cleaned_df = cleaner.display_cleaning_interface()

            with tab2:
                st.subheader("🗑️ Drop Columns")
                st.write("Remove unwanted columns from your dataset.")
                cleaner.drop_columns()

            with tab3:
                st.subheader("📊 Handle High Missing Columns")
                st.write("Deal with columns that have more than 50% missing values.")
                cleaner.drop_high_missing_columns()

            with tab4:
                st.subheader("📤 Export Cleaned Data")
                if hasattr(cleaner, 'df') and cleaner.df is not None:
                    display_export_interface(cleaner.df, "cleaned")
                else:
                    st.warning("⚠️ No cleaned data available. Please clean the data first.")

            # Option to use cleaned data for further analysis
            if hasattr(cleaner, 'df') and cleaner.df is not None:
                current_df = cleaner.df
                if not current_df.equals(df):
                    st.markdown("---")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info("💡 Your data has been modified. You can use the cleaned data for further analysis.")
                    with col2:
                        if st.button("📊 Use Cleaned Data", type="primary"):
                            st.session_state['cleaned_df'] = current_df.copy()
                            st.success("✅ Cleaned data is now available for analysis!")
                            st.rerun()

                    # Show comparison
                    if st.checkbox("🔍 Show Before/After Comparison"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("📊 Original Data")
                            st.write(f"Shape: {df.shape}")
                            st.write(f"Missing values: {df.isnull().sum().sum()}")
                            st.dataframe(df.head(), use_container_width=True)

                        with col2:
                            st.subheader("✨ Cleaned Data")
                            st.write(f"Shape: {current_df.shape}")
                            st.write(f"Missing values: {current_df.isnull().sum().sum()}")
                            st.dataframe(current_df.head(), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error in Data Cleaning: {str(e)}")
            st.exception(e)

else:
    # Welcome screen with instructions
    st.markdown('<div class="info-text">', unsafe_allow_html=True)
    
    if df is None:
        st.info("👋 **Welcome to InsightForge!** Please select a data source to begin analysis.")
    else:
        st.warning("⚠️ The loaded dataset appears to be empty. Please check your source and try again.")
    
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
    
    **🧹 Data Cleaning**
    - Handle missing values with multiple imputation methods
    - Support for both numerical and categorical data
    - Advanced imputation using KNN and fancyimpute
    
    **📤 Export Data**
    - Export in multiple formats: CSV, TSV, JSON, Excel
    - Custom export options with different separators
    - Export both original and cleaned data
    - Advanced options for JSON orientation and CSV formatting
    
    ### 🚀 Quick Start
    1. **Choose a data source**: Upload a file, paste a URL, get data from an API, or use the sample data.
    2. **Follow the on-screen instructions** to load your data.
    3. **Navigate** using the sidebar to explore different analysis types.
    4. **Clean your data** if needed using the Data Cleaning section.
    5. **Export your results** in your preferred format.
    
    ### 💡 Tips
    - For large datasets, visualizations are automatically optimized.
    - Missing values are handled gracefully with warnings.
    - Use category limiting sliders for columns with many unique values.
    - Clean your data first before performing analysis for better results.
    - Export functionality supports both original and cleaned data.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Check if we should use cleaned data
if 'cleaned_df' in st.session_state:
    cleaned_data = st.session_state['cleaned_df']

    # Show notification about using cleaned data
    st.info("ℹ️ Currently using cleaned data. Switch data source above to use original data.")

    # Option to revert to original data
    if st.button("🔄 Use Original Data"):
        if 'cleaned_df' in st.session_state:
            del st.session_state['cleaned_df']
        st.rerun()

    # Use cleaned data for analysis if not in cleaning or export mode
    if analysis_type not in ["🧹 Data Cleaning", "📤 Export Data"]:
        df = cleaned_data
