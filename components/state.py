import streamlit as st
import pandas as pd

def _df_hash(df: pd.DataFrame) -> str:
    """Cheap-ish content hash to detect dataset changes across reruns."""
    try:
        return str(pd.util.hash_pandas_object(df, index=True).sum())
    except Exception:
        # Fallback to shape + columns
        return f"{df.shape}-{tuple(df.columns)}"

def ensure_cleaned_consistency(df):
    """Clear stale cleaned_df when a new source dataset is loaded."""
    if df is None or getattr(df, "empty", False):
        return
    new_hash = _df_hash(df)
    if st.session_state.get("source_df_hash") != new_hash:
        st.session_state["source_df_hash"] = new_hash
        if "cleaned_df" in st.session_state:
            del st.session_state["cleaned_df"]

def apply_cleaned_preference(df, analysis_key: str, disallowed_views: set):
    """
    Return (active_df, using_cleaned) based on a sidebar toggle.
    We disable cleaned usage on disallowed views (e.g., cleaning/export).
    """
    has_cleaned = "cleaned_df" in st.session_state and st.session_state["cleaned_df"] is not None and not st.session_state["cleaned_df"].empty

    # Sidebar toggle
    with st.sidebar:
        use_cleaned = st.toggle(
            "Use cleaned data",
            value=has_cleaned,  # default to cleaned if available
            disabled=not has_cleaned,
            help="When enabled, analyses (except Cleaning and Export) use your cleaned dataset.",
            key="use_cleaned_toggle",
        )
        # Quick reset
        if has_cleaned and st.button("🔄 Reset to Original"):
            del st.session_state["cleaned_df"]
            st.rerun()

    if has_cleaned and use_cleaned and analysis_key not in disallowed_views:
        return st.session_state["cleaned_df"], True
    return df, False