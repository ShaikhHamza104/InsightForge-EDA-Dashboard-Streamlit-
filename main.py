import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
import streamlit as st
import pandas as pd

# External analysis modules (existing files at project root)
import univariate_analysis
import bivariate_analysis

# Refactored components (modularized)
from components.overview import Overview
from components.cleaning import BasicDataClean
from components.load_data import load_data
from components.metrics import display_dataset_metrics
from components.export_ui import display_export_interface
from components.welcome import show_welcome
from components.state import apply_cleaned_preference, ensure_cleaned_consistency


# 1) Page setup MUST be first Streamlit call
st.set_page_config(
    page_title="InsightForge — EDA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 2) Load CSS once
def load_css(path: str = "components/styles.css"):
    try:
        css = Path(path).read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Could not load CSS from {path}: {e}")

load_css()


# 3) Header
st.markdown('<h1 class="main-header">📊 InsightForge — EDA Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Analyze datasets quickly with interactive Overview, Univariate, and Bivariate visualizations</p>', unsafe_allow_html=True)


# 4) Sidebar: app navigation
with st.sidebar:
    st.markdown('<h2 style="text-align: center; color: var(--primary);">📊 InsightForge</h2>', unsafe_allow_html=True)

    options_map = {
        "overview": "📋 Overview",
        "univariate": "📊 Univariate Analysis",
        "bivariate": "📈 Bivariate Analysis",
        "cleaning": "🧹 Data Cleaning",
        "export": "📤 Export Data",
    }
    analysis_key = st.radio(
        "🎯 Select Analysis Type",
        options=list(options_map.keys()),
        format_func=lambda k: options_map[k],
        index=0,
        help="Choose the type of analysis you want to perform",
        key="analysis_type_key",
    )

    st.markdown("---")

    # About
    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown("### 🚀 Features")
    st.markdown("""
    - **📋 Overview**: Dataset summary, statistics, correlations
    - **📊 Univariate**: Single variable analysis
    - **📈 Bivariate**: Relationship analysis
    - **🧹 Data Cleaning**: Handle missing values, outliers
    - **📤 Export Data**: Multiple format downloads
    - **🎨 Interactive**: Plotly-powered visualizations
    - **⚡ Fast**: Optimized for performance
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p style="text-align: center; font-size: 0.8rem; color: #666;">Built with ❤️ using Streamlit</p>', unsafe_allow_html=True)


# 5) Load data (includes its own "source" selector UI)
df = load_data()

# Keep cleaned data consistent when a new dataset is loaded
ensure_cleaned_consistency(df)

# Apply "Use cleaned data" preference, except in Cleaning/Export views
active_df, using_cleaned = apply_cleaned_preference(
    df=df,
    analysis_key=analysis_key,
    disallowed_views={"cleaning", "export"},
)

# 6) Notify about active dataset
if using_cleaned:
    st.info("ℹ️ Currently using cleaned data. Toggle off in the sidebar to use the original dataset.")

# 7) Route
if active_df is not None and not active_df.empty:
    # Metrics
    display_dataset_metrics(active_df)

    st.markdown("---")

    if analysis_key == "overview":
        with st.spinner("Computing overview..."):
            try:
                Overview(active_df).display_overview()
            except Exception as e:
                st.error(f"❌ Error in Overview analysis: {e}")
                st.exception(e)

    elif analysis_key == "univariate":
        with st.spinner("Running univariate analysis..."):
            try:
                univariate = univariate_analysis.UnivariateAnalysis(active_df)
                univariate.display()
            except Exception as e:
                st.error(f"❌ Error in Univariate analysis: {e}")
                st.exception(e)

    elif analysis_key == "bivariate":
        with st.spinner("Exploring relationships..."):
            try:
                bivariate = bivariate_analysis.BivariateAnalysis(active_df)
                bivariate.column_vs_column_display()
            except Exception as e:
                st.error(f"❌ Error in Bivariate analysis: {e}")
                st.exception(e)

    elif analysis_key == "export":
        try:
            # Tabs: Original vs Cleaned (if available)
            if "cleaned_df" in st.session_state and st.session_state["cleaned_df"] is not None:
                tab1, tab2 = st.tabs(["📋 Original Data", "✨ Cleaned Data"])
                with tab1:
                    st.subheader("📋 Export Original Data")
                    display_export_interface(df, "original")
                with tab2:
                    st.subheader("✨ Export Cleaned Data")
                    display_export_interface(st.session_state["cleaned_df"], "cleaned")
            else:
                st.subheader("📋 Export Current Data")
                display_export_interface(active_df, "current")
                st.info("💡 Tip: Clean your data first to have both original and cleaned export options!")
        except Exception as e:
            st.error(f"❌ Error in Export functionality: {e}")
            st.exception(e)

    elif analysis_key == "cleaning":
        try:
            cleaner = BasicDataClean(df)  # Always start cleaning from the original context

            tab1, tab2, tab3, tab4 = st.tabs(["🧹 Missing Values", "🗑️ Drop Columns", "📊 High Missing Columns", "📤 Export"])

            with tab1:
                with st.spinner("Applying missing value strategies..."):
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
                if hasattr(cleaner, "df") and cleaner.df is not None:
                    display_export_interface(cleaner.df, "cleaned")
                else:
                    st.warning("⚠️ No cleaned data available. Please clean the data first.")

            # Offer to use cleaned data
            if hasattr(cleaner, "df") and cleaner.df is not None:
                current_df = cleaner.df
                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info("💡 Your data has been modified. You can use the cleaned data for further analysis.")
                with col2:
                    if st.button("📊 Use Cleaned Data", type="primary"):
                        st.session_state["cleaned_df"] = current_df.copy()
                        st.success("✅ Cleaned data is now available for analysis!")
                        st.rerun()

                if st.checkbox("🔍 Show Before/After Comparison"):
                    colA, colB = st.columns(2)
                    with colA:
                        st.subheader("📊 Original Data")
                        st.write(f"Shape: {df.shape}")
                        st.write(f"Missing values: {int(df.size - df.count().sum()):,}")
                        st.dataframe(df.head(), use_container_width=True)
                    with colB:
                        st.subheader("✨ Cleaned Data")
                        st.write(f"Shape: {current_df.shape}")
                        st.write(f"Missing values: {int(current_df.size - current_df.count().sum()):,}")
                        st.dataframe(current_df.head(), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error in Data Cleaning: {e}")
            st.exception(e)

else:
    show_welcome(df)