import streamlit as st
from data_export import DataExporter  # your existing class

def display_export_interface(df, data_type: str = "cleaned"):
    """Display export interface using Streamlit's download buttons."""
    st.markdown('<div class="export-section">', unsafe_allow_html=True)
    st.subheader(f"📤 Export {data_type.title()} Data")
    st.write("Choose your preferred format to download the data:")

    if df is None or getattr(df, "empty", True):
        st.warning("⚠️ No data available for export.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    exporter = DataExporter(df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📄 Text Formats**")
        csv_str = exporter.to_csv()
        st.download_button(
            "📊 Download CSV",
            data=csv_str.encode("utf-8"),
            file_name=f"{data_type}_data_{exporter.timestamp}.csv",
            mime="text/csv",
            use_container_width=True,
            key=f"dl_csv_{data_type}",
        )

        tsv_str = exporter.to_tsv()
        st.download_button(
            "📋 Download TSV",
            data=tsv_str.encode("utf-8"),
            file_name=f"{data_type}_data_{exporter.timestamp}.tsv",
            mime="text/tab-separated-values",
            use_container_width=True,
            key=f"dl_tsv_{data_type}",
        )

    with col2:
        st.markdown("**🗂️ Structured Formats**")
        json_str = exporter.to_json()
        st.download_button(
            "🔗 Download JSON",
            data=json_str.encode("utf-8"),
            file_name=f"{data_type}_data_{exporter.timestamp}.json",
            mime="application/json",
            use_container_width=True,
            key=f"dl_json_{data_type}",
        )

        try:
            xlsx_bytes = exporter.to_excel()
            st.download_button(
                "📈 Download Excel",
                data=xlsx_bytes,
                file_name=f"{data_type}_data_{exporter.timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key=f"dl_xlsx_{data_type}",
            )
        except Exception as e:
            st.error(f"❌ Error creating Excel file: {e}")

    with col3:
        st.markdown("**📊 Data Summary**")
        st.metric("📈 Total Rows", len(df))
        st.metric("📊 Total Columns", len(df.columns))
        mem_kb = df.memory_usage(deep=True).sum() / 1024
        st.metric("💾 Memory", f"{mem_kb:.1f} KB")

    with st.expander("🔧 Advanced Export Options"):
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**CSV / Delimited Options**")
            include_index = st.checkbox("Include Index", value=False, key=f"index_{data_type}")
            sep_label = st.selectbox(
                "Separator",
                [(",", "Comma , (.csv)"), (";", "Semicolon ; (.csv)"), ("|", "Pipe | (.csv)"), ("\t", "Tab \\t (.tsv)")],
                index=0,
                format_func=lambda x: x[1],
                key=f"sep_{data_type}",
            )
            separator = sep_label[0]
            ext = "tsv" if separator == "\t" else "csv"
            mime = "text/tab-separated-values" if ext == "tsv" else "text/csv"

            custom_csv = exporter.to_csv(index=include_index, separator=separator)
            st.download_button(
                f"📥 Download Custom {ext.upper()}",
                data=custom_csv.encode("utf-8"),
                file_name=f"{data_type}_data_custom_{exporter.timestamp}.{ext}",
                mime=mime,
                use_container_width=True,
                key=f"dl_custom_{ext}_{data_type}",
            )

        with c2:
            st.markdown("**JSON Options**")
            orient = st.selectbox(
                "JSON Orientation",
                ["records", "index", "columns", "values", "split", "table"],
                index=0,
                key=f"json_orient_{data_type}",
            )
            lines = st.checkbox("JSON Lines (one record per line)", value=False, key=f"json_lines_{data_type}")

            try:
                # Try with both parameters first
                custom_json = exporter.to_json(orient=orient, lines=lines)
            except TypeError:
                # If lines parameter is not supported, fall back to orient only
                custom_json = exporter.to_json(orient=orient)
                if lines:
                    st.warning("⚠️ JSON Lines format not supported by DataExporter. Using standard JSON format.")
            
            st.download_button(
                "🔗 Download Custom JSON",
                data=custom_json.encode("utf-8"),
                file_name=f"{data_type}_data_custom_{exporter.timestamp}.json",
                mime="application/json",
                use_container_width=True,
            )

    with st.expander("👀 Preview Data (First 5 rows)"):
        st.dataframe(df.head(), use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)