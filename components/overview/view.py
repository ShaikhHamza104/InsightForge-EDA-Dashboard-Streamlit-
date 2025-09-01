import pandas as pd
import streamlit as st

from .sections import (
    show_categorical_analysis,
    show_correlations,
    show_dimensions,
    show_dtypes_analysis,
    show_missing_values,
    show_numeric_stats,
    show_preview,
    show_summary,
)


class Overview:
    """Streamlit Overview view for quick EDA of a pandas DataFrame."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def display_overview(self):
        st.title("📋 Dataset Overview")
        st.markdown(
            "Get a comprehensive summary of your dataset including shape, statistics, missing values, "
            "data types, categorical distributions, and correlations."
        )

        if self.df is None or self.df.empty:
            st.warning("⚠️ The dataset is empty. Please upload data to see the overview.")
            return

        show_dimensions(self.df)
        show_preview(self.df)
        show_numeric_stats(self.df)
        show_missing_values(self.df)
        show_dtypes_analysis(self.df)
        show_categorical_analysis(self.df)
        show_correlations(self.df)
        show_summary(self.df)