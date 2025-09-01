# Thin wrapper to preserve existing imports: `import overview` then `overview.Overview(...)`
from components.overview import Overview

# Optional demo run
if __name__ == "__main__":
    import streamlit as st
    import pandas as pd

    try:
        demo_url = "https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/master/laptop_cleaning.csv"
        df_demo = pd.read_csv(demo_url)
        Overview(df_demo).display_overview()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")