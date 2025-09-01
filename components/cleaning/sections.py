from __future__ import annotations

from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from .helpers import (
    decode_labels_to_strings,
    encode_categoricals_label,
    fancy_knn_impute_categoricals,
    fancyimpute_available,
    high_missing_columns,
    missing_summary,
    numeric_describe,
    numeric_knn_impute,
    safe_knn_neighbors,
)


def ui_dataset_overview(df: pd.DataFrame):
    st.subheader("📊 Dataset Overview")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Rows", f"{df.shape[0]:,}")
    with c2:
        st.metric("Columns", f"{df.shape[1]:,}")
    with c3:
        st.metric("Missing Values", f"{int(df.isnull().sum().sum()):,}")


def ui_missing_overview(df: pd.DataFrame) -> pd.DataFrame:
    st.header("🔍 Missing Data Overview")
    m = missing_summary(df)
    missing_cols_df = m[m["Missing Count"] > 0]
    if missing_cols_df.empty:
        st.success("✅ No missing values found in the dataset!")
    else:
        st.dataframe(missing_cols_df, use_container_width=True)
    return missing_cols_df


def ui_drop_high_missing_columns(cleaner):
    st.subheader("📊 Handle High Missing Columns (>50%)")
    cols = high_missing_columns(cleaner.df, threshold=0.5)
    if not cols:
        st.info("No columns over 50% missing.")
        return

    st.write(f"Columns with >50% missing values ({len(cols)}):")
    st.code(", ".join(cols))
    choice = st.selectbox("Action", ["Keep as is", "Drop columns"], index=0, key="high_missing_action")
    if choice == "Drop columns":
        cleaner.df = cleaner.df.drop(columns=cols, errors="ignore")
        st.success(f"Dropped {len(cols)} high-missing columns.")


def ui_drop_columns(cleaner):
    st.subheader("🗑️ Drop Columns")
    all_cols = cleaner.df.columns.tolist()
    if not all_cols:
        st.warning("No columns available to drop.")
        return

    to_drop = st.multiselect("Select columns to drop:", options=all_cols, default=[])
    if to_drop and st.button("Drop Selected Columns", key="drop_cols_btn"):
        cleaner.df = cleaner.df.drop(columns=to_drop, errors="ignore")
        st.success(f"Dropped {len(to_drop)} column(s): {', '.join(to_drop)}")
    elif not to_drop:
        st.info("No columns selected.")


def ui_numeric_imputation(cleaner):
    st.subheader("🔢 Numeric Columns Imputation")
    numeric_cols = cleaner.df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        st.info("ℹ️ No numeric columns found.")
        return

    missing_numeric = cleaner.df[numeric_cols].isnull().sum()
    numeric_with_missing = missing_numeric[missing_numeric > 0]
    if numeric_with_missing.empty:
        st.info("ℹ️ No missing values in numeric columns.")
        return

    st.write(f"Numeric columns with missing values: {len(numeric_with_missing)}")
    with st.expander("Show per-column missing counts"):
        for col, cnt in numeric_with_missing.items():
            st.write(f"• {col}: {cnt} ({cnt/len(cleaner.df)*100:.1f}%)")

    method = st.selectbox(
        "Choose method",
        options=["mean", "median", "mode", "custom value", "knn imputation"],
        key="numeric_impute_method",
    )

    custom_val = None
    if method == "custom value":
        custom_val = st.number_input("Enter custom number", value=0.0, key="custom_numeric_value")

    if st.button("Apply Numeric Imputation", key="apply_numeric"):
        try:
            if method == "mean":
                cleaner.df[numeric_cols] = cleaner.df[numeric_cols].fillna(cleaner.df[numeric_cols].mean())
                st.success("Filled missing values with column means.")
            elif method == "median":
                cleaner.df[numeric_cols] = cleaner.df[numeric_cols].fillna(cleaner.df[numeric_cols].median())
                st.success("Filled missing values with column medians.")
            elif method == "mode":
                for col in numeric_cols:
                    if cleaner.df[col].isnull().any():
                        mode = cleaner.df[col].mode()
                        if not mode.empty:
                            cleaner.df[col] = cleaner.df[col].fillna(mode.iloc[0])
                st.success("Filled missing values with column modes.")
            elif method == "custom value":
                cleaner.df[numeric_cols] = cleaner.df[numeric_cols].fillna(custom_val)
                st.success(f"Filled missing values with {custom_val}.")
            elif method == "knn imputation":
                with st.spinner("Performing KNN imputation..."):
                    k = safe_knn_neighbors(cleaner.df.shape[0], default=5)
                    if k <= 0:
                        st.error("Not enough rows for KNN imputation.")
                    else:
                        imputed = numeric_knn_impute(cleaner.df[numeric_cols], n_neighbors=k)
                        cleaner.df[numeric_cols] = imputed
                        st.success("KNN imputation completed.")
        except Exception as e:
            st.error(f"❌ Numeric imputation error: {e}")


def ui_categorical_imputation(cleaner):
    st.subheader("📝 Categorical Columns Imputation")
    cat_cols = cleaner.df.select_dtypes(include=["object", "category"]).columns.tolist()
    if not cat_cols:
        st.info("ℹ️ No categorical columns found.")
        return

    missing_cat = cleaner.df[cat_cols].isnull().sum()
    cat_with_missing = missing_cat[missing_cat > 0].index.tolist()
    if not cat_with_missing:
        st.info("ℹ️ No missing values in categorical columns.")
        return

    st.write(f"Categorical columns with missing values: {len(cat_with_missing)}")
    with st.expander("Show per-column missing counts"):
        for col in cat_with_missing:
            cnt = int(missing_cat[col])
            st.write(f"• {col}: {cnt} ({cnt/len(cleaner.df)*100:.1f}%)")

    options = ["mode", "unknown", "custom value"]
    if fancyimpute_available():
        options.append("fancyimpute KNN")
        st.caption("✅ fancyimpute available for advanced KNN imputation.")
    else:
        st.caption("ℹ️ Install fancyimpute for advanced KNN: pip install fancyimpute")

    method = st.selectbox(
        "Choose method for categorical imputation",
        options=options,
        key="categorical_impute_method",
    )

    custom_text = None
    k_neighbors = 3
    if method == "custom value":
        custom_text = st.text_input("Enter custom text", value="Missing", key="custom_categorical_value")
    elif method == "fancyimpute KNN" and fancyimpute_available():
        k_neighbors = st.slider("Number of neighbors (KNN)", 1, 10, 3, 1, key="cat_knn_k")

    if st.button("Apply Categorical Imputation", key="apply_categorical"):
        try:
            if method == "mode":
                imputed_cols = []
                for col in cat_cols:
                    if cleaner.df[col].isnull().any():
                        mode = cleaner.df[col].mode(dropna=True)
                        if not mode.empty:
                            cleaner.df[col] = cleaner.df[col].fillna(mode.iloc[0])
                            imputed_cols.append(col)
                if imputed_cols:
                    st.success(f"Filled with mode: {', '.join(imputed_cols)}")
                else:
                    st.info("No columns required mode imputation.")
            elif method == "unknown":
                cleaner.df[cat_cols] = cleaner.df[cat_cols].fillna("Unknown")
                st.success("Filled missing values with 'Unknown'.")
            elif method == "custom value":
                cleaner.df[cat_cols] = cleaner.df[cat_cols].fillna(custom_text)
                st.success(f"Filled missing values with '{custom_text}'.")
            elif method == "fancyimpute KNN" and fancyimpute_available():
                # Only impute columns that have missing values
                cols_to_impute = [c for c in cat_cols if cleaner.df[c].isnull().any()]
                if not cols_to_impute:
                    st.info("No categorical columns require imputation.")
                    return

                original_subset = cleaner.df[cols_to_impute].copy()
                # Encode
                encoded, encoders = encode_categoricals_label(original_subset)

                # Guard for rows
                k_eff = safe_knn_neighbors(cleaner.df.shape[0], default=k_neighbors)
                if k_eff <= 0:
                    st.warning("Not enough rows for KNN; falling back to mode.")
                    # fallback
                    for col in cols_to_impute:
                        mode = original_subset[col].mode(dropna=True)
                        if not mode.empty:
                            cleaner.df[col] = original_subset[col].fillna(mode.iloc[0])
                    return

                with st.spinner("Running fancyimpute KNN on categorical data..."):
                    try:
                        imputed_encoded = fancy_knn_impute_categoricals(encoded, k=k_eff)
                        decoded = decode_labels_to_strings(imputed_encoded, encoders)
                        for col in cols_to_impute:
                            cleaner.df[col] = decoded[col]
                        st.success(f"FancyImpute KNN applied to: {', '.join(cols_to_impute)}")
                    except Exception as inner_e:
                        st.warning(f"FancyImpute failed: {inner_e}. Falling back to mode.")
                        for col in cols_to_impute:
                            mode = original_subset[col].mode(dropna=True)
                            if not mode.empty:
                                cleaner.df[col] = original_subset[col].fillna(mode.iloc[0])
        except Exception as e:
            st.error(f"❌ Categorical imputation error: {e}")