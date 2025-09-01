from textwrap import dedent
import streamlit as st

def show_welcome(df):
    """Welcome screen with clear instructions and quick actions."""
    st.markdown('<div class="info-text">', unsafe_allow_html=True)

    if df is None:
        st.info("👋 **Welcome to InsightForge!** Please select a data source to begin analysis.")
    else:
        st.warning("⚠️ The loaded dataset appears to be empty. Please check your source and try again.")

    st.markdown(dedent("""
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
    - Optional advanced methods (e.g., KNN) if installed

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
    """))

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("🧪 Use Sample Data"):
            st.session_state["data_source"] = "Use Sample Data"
            st.rerun()
    with c2:
        if st.button("🌐 Try Demo URL"):
            st.session_state["data_source"] = "From Website URL"
            st.session_state["prefill_demo_url"] = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
            st.rerun()
    with c3:
        st.caption("Tip: You can switch sources anytime from the top of the page.")

    st.markdown("</div>", unsafe_allow_html=True)