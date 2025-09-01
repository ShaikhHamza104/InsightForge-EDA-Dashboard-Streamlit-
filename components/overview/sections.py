from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from .helpers import cached_corr, cached_describe, cached_value_counts


def show_dimensions(df: pd.DataFrame):
    st.subheader("📐 Dataset Dimensions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("📈 Total Columns", f"{df.shape[1]}")
    with col3:
        memory_usage_mb = df.memory_usage(deep=True).sum() / 1024**2
        st.metric("💾 Memory Usage", f"{memory_usage_mb:.2f} MB")


def show_preview(df: pd.DataFrame):
    st.subheader("🔍 Data Preview")
    tab1, tab2, tab3 = st.tabs(["📄 First 5 Rows", "📄 Last 5 Rows", "🎲 Random Sample"])

    with tab1:
        st.dataframe(df.head(), use_container_width=True)
    with tab2:
        st.dataframe(df.tail(), use_container_width=True)
    with tab3:
        n = min(5, len(df))
        if n == 0:
            st.info("Dataset is empty.")
        else:
            st.dataframe(df.sample(n), use_container_width=True)


def show_numeric_stats(df: pd.DataFrame):
    st.subheader("📈 Summary Statistics (Numerical)")
    numeric_df = df.select_dtypes(include=["number"])
    if numeric_df.empty:
        st.info("ℹ️ No numerical columns available for statistics.")
        return

    with st.spinner("Calculating summary statistics..."):
        desc = cached_describe(numeric_df).T
    st.dataframe(desc, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("🔢 Numerical Columns", len(numeric_df.columns))
    with c2:
        total_numeric_nulls = int(numeric_df.isnull().sum().sum())
        st.metric("⚠️ Numerical Nulls", f"{total_numeric_nulls:,}")


def show_missing_values(df: pd.DataFrame):
    st.subheader("⚠️ Missing Values Analysis")
    total_rows = len(df)
    if total_rows == 0:
        st.info("No rows to analyze for missing values.")
        return

    with st.spinner("Profiling missing values..."):
        missing_counts = df.isnull().sum()
        missing_percent = (missing_counts / total_rows) * 100
        missing_df = pd.DataFrame(
            {
                "Column": missing_counts.index.astype(str),
                "Missing Count": missing_counts.values,
                "Missing Percentage (%)": missing_percent.round(2),
            }
        )
        missing_with_nulls = missing_df[missing_df["Missing Count"] > 0]

    if missing_with_nulls.empty:
        st.success("✅ Excellent! No missing values found in the dataset!")
        return

    st.dataframe(
        missing_with_nulls.sort_values("Missing Count", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.metric("📊 Columns with Missing Values", len(missing_with_nulls))
    with c2:
        st.metric("🔢 Total Missing Values", f"{int(missing_counts.sum()):,}")

    if len(missing_with_nulls) <= 20:
        fig, ax = plt.subplots(figsize=(10, 6))
        try:
            missing_with_nulls.plot(
                x="Column", y="Missing Percentage (%)", kind="bar", ax=ax, color="coral"
            )
            ax.set_title("Missing Values by Column")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig)
        finally:
            plt.close(fig)


def show_dtypes_analysis(df: pd.DataFrame):
    st.subheader("🧬 Data Types Analysis")
    try:
        dtype_series = df.dtypes.astype(str)
        counts = dtype_series.value_counts()
        dtype_counts = pd.DataFrame({"Data Type": counts.index, "Count": counts.values})

        c1, c2 = st.columns([1, 2])
        with c1:
            st.dataframe(dtype_counts, hide_index=True, use_container_width=True)
        with c2:
            fig, ax = plt.subplots(figsize=(8, 6))
            try:
                if len(dtype_counts) > 6:
                    ax.bar(dtype_counts["Data Type"], dtype_counts["Count"], color="skyblue")
                    ax.set_ylabel("Count")
                    ax.set_title("Distribution of Data Types")
                    plt.xticks(rotation=45, ha="right")
                else:
                    ax.pie(dtype_counts["Count"], labels=dtype_counts["Data Type"], autopct="%1.1f%%")
                    ax.set_title("Distribution of Data Types")
                st.pyplot(fig)
            finally:
                plt.close(fig)

        with st.expander("🔍 Show detailed column information"):
            detailed = pd.DataFrame(
                {
                    "Column": df.columns.astype(str),
                    "Data Type": [str(dt) for dt in df.dtypes.values],
                    "Non-Null Count": [df[col].count() for col in df.columns],
                    "Unique Values": [df[col].nunique(dropna=True) for col in df.columns],
                }
            )
            st.dataframe(detailed, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"❌ Error displaying data types: {str(e)}")


def show_categorical_analysis(df: pd.DataFrame):
    st.subheader("🔠 Categorical Data Analysis")
    categorical_cols: List[str] = df.select_dtypes(include=["object", "category"]).columns.astype(str).tolist()

    if not categorical_cols:
        st.info("ℹ️ No categorical columns found in the dataset.")
        return

    selected_col = st.selectbox("📊 Select a categorical column for detailed analysis:", categorical_cols)

    normalize = st.checkbox("Show percentages instead of counts", value=False)
    top_n = st.slider("Top categories to display", min_value=5, max_value=30, value=10, step=1)

    with st.spinner("Computing category distribution..."):
        vc = cached_value_counts(df[selected_col], dropna=True)
    total_categories = int(vc.shape[0])

    if total_categories == 0:
        st.info("The selected column has no valid (non-null) categories.")
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🏷️ Unique Categories", total_categories)
    with c2:
        most_label = str(vc.index[0])
        st.metric("🥇 Most Common", f"{most_label} — {int(vc.iloc[0])} occurrences")
    with c3:
        if total_categories > 1:
            second_label = str(vc.index[1])
            st.metric("🥈 Second Most Common", f"{second_label} — {int(vc.iloc[1])} occurrences")

    display_counts = vc.head(top_n) if total_categories > top_n else vc
    if total_categories > top_n:
        st.info(f"📊 Column has {total_categories} unique values. Showing top {top_n}.")

    if normalize:
        total = vc.sum()
        display_df = (display_counts / total * 100).round(2).to_frame("Percentage (%)")
    else:
        display_df = display_counts.to_frame("Count")

    st.dataframe(display_df, use_container_width=True)

    if len(display_counts) <= 15:
        fig, ax = plt.subplots(figsize=(10, 6))
        try:
            if normalize:
                (display_counts / display_counts.sum() * 100).plot(kind="bar", ax=ax, color="skyblue")
                ax.set_ylabel("Percentage (%)")
            else:
                display_counts.plot(kind="bar", ax=ax, color="skyblue")
                ax.set_ylabel("Count")
            ax.set_title(f"Top Categories in {selected_col}")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig)
        finally:
            plt.close(fig)


def show_correlations(df: pd.DataFrame):
    st.subheader("🔗 Correlation Analysis")

    numerical_df = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
    if numerical_df.empty or numerical_df.shape[1] < 2:
        st.info("ℹ️ Need at least 2 numerical columns with valid data for correlation analysis.")
        return

    # Drop constant columns
    nunique = numerical_df.nunique(dropna=True)
    constant_cols = nunique[nunique <= 1].index.tolist()
    if constant_cols:
        st.caption(f"Note: Dropping {len(constant_cols)} constant column(s) from correlation.")
        numerical_df = numerical_df.drop(columns=constant_cols, errors="ignore")

    if numerical_df.shape[1] < 2:
        st.info("ℹ️ After removing constant/all-NaN columns, fewer than 2 columns remain.")
        return

    if numerical_df.shape[1] > 15:
        st.warning(
            f"⚠️ Dataset has {numerical_df.shape[1]} numerical columns. Large correlation matrices can be hard to read."
        )

    method = st.selectbox("Correlation method", ["pearson", "spearman", "kendall"], index=0)

    if numerical_df.shape[1] > 15:
        analysis_option = st.radio(
            "Choose correlation analysis approach:",
            ["Show top correlations", "Select specific columns", "Show full matrix"],
            index=0,
        )
    else:
        analysis_option = "Show full matrix"

    if analysis_option == "Show top correlations":
        with st.spinner("Computing correlations..."):
            corr_matrix = cached_corr(numerical_df, method)
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
        stacked = pd.DataFrame(corr_matrix.where(mask).stack().reset_index())
        stacked.columns = ["Variable 1", "Variable 2", "Correlation"]
        top_k = st.slider("How many pairs to show", 5, 50, 10, 1)
        top_df = (
            stacked.reindex(stacked["Correlation"].abs().sort_values(ascending=False).index)
            .head(top_k)
            .reset_index(drop=True)
        )
        st.dataframe(top_df, use_container_width=True, hide_index=True)

    elif analysis_option == "Select specific columns":
        selected_cols = st.multiselect(
            "📊 Select columns for correlation analysis (max ~15 recommended):",
            numerical_df.columns.tolist(),
            default=numerical_df.columns.tolist()[: min(10, len(numerical_df.columns))],
        )
        if len(selected_cols) < 2:
            st.info("Please select at least two columns to compute correlations.")
            return
        numerical_df = numerical_df[selected_cols]

    if analysis_option != "Show top correlations":
        try:
            with st.spinner("Rendering correlation heatmap..."):
                corr = cached_corr(numerical_df, method)

                if corr.isnull().any().any():
                    st.warning("⚠️ Some correlation values are NaN (likely due to constant values) and will be shown as 0.")
                    corr = corr.fillna(0)

                cols_n = corr.shape[1]
                annotate = cols_n <= 12

                fig, ax = plt.subplots(figsize=(12, 10))
                try:
                    mask = np.triu(np.ones_like(corr, dtype=bool))  # mask upper triangle
                    sns.heatmap(
                        corr,
                        annot=annotate,
                        cmap="RdBu_r",
                        mask=mask,
                        fmt=".2f",
                        linewidths=0.5,
                        ax=ax,
                        annot_kws={"size": 8} if annotate else None,
                        center=0,
                        vmin=-1,
                        vmax=1,
                    )
                    plt.title("Correlation Matrix (Lower Triangle)", fontsize=14, pad=20)
                    plt.tight_layout()
                    st.pyplot(fig)
                finally:
                    plt.close(fig)

                no_diag = corr.where(~np.eye(corr.shape[0], dtype=bool))
                max_corr = float(no_diag.max().max())
                min_corr = float(no_diag.min().min())
                avg_corr = float(no_diag.abs().mean().mean())

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("🔺 Strongest Positive Correlation", f"{max_corr:.3f}")
                with c2:
                    st.metric("🔻 Strongest Negative Correlation", f"{min_corr:.3f}")
                with c3:
                    st.metric("📊 Average Absolute Correlation", f"{avg_corr:.3f}")

        except Exception as e:
            st.error(f"❌ Error generating correlation matrix: {str(e)}")


def show_summary(df: pd.DataFrame):
    st.subheader("📋 Dataset Summary")

    numeric_cols = df.select_dtypes(include=["number"]).columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns

    summary_data = {
        "Metric": [
            "Total Rows",
            "Total Columns",
            "Numerical Columns",
            "Categorical Columns",
            "Total Missing Values",
            "Memory Usage (MB)",
            "Complete Rows",
        ],
        "Value": [
            f"{df.shape[0]:,}",
            f"{df.shape[1]}",
            f"{len(numeric_cols)}",
            f"{len(categorical_cols)}",
            f"{int(df.isnull().sum().sum()):,}",
            f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}",
            f"{int(df.notna().all(axis=1).sum()):,}",
        ],
    }

    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)