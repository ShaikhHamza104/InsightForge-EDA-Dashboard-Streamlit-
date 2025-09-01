import streamlit as st

def _format_bytes(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def display_dataset_metrics(df):
    """Display key dataset metrics in an attractive format."""
    st.markdown('<div class="info-text">', unsafe_allow_html=True)

    if df is None or getattr(df, "empty", True):
        st.warning("⚠️ No data available.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    rows, cols = df.shape
    try:
        missing = int(df.size - df.count().sum())
    except Exception:
        missing = int(df.isna().sum().sum())

    try:
        mem_bytes = int(df.memory_usage(index=True, deep=True).sum())
    except Exception:
        mem_bytes = int(df.memory_usage(index=True, deep=False).sum())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📊 Rows", f"{rows:,}")
    with c2:
        st.metric("📈 Columns", f"{cols:,}")
    with c3:
        st.metric("⚠️ Missing Values", f"{missing:,}")
    with c4:
        st.metric("💾 Memory Usage", _format_bytes(mem_bytes))

    st.markdown("</div>", unsafe_allow_html=True)