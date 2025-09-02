import io
import json
from typing import Optional, List

import pandas as pd
import requests
import streamlit as st


@st.cache_data(show_spinner=False)
def load_sample_data() -> Optional[pd.DataFrame]:
    """Load sample dataset with caching for better performance."""
    try:
        # Fixed raw GitHub URL (refs/heads path can be flaky)
        url = "https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/master/laptop_cleaning.csv"
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading sample data: {e}")
        return None


def _read_uploaded_delimited(uploaded_file) -> pd.DataFrame:
    """Read CSV/TSV with simple but resilient logic."""
    name = uploaded_file.name.lower()
    sep = "\t" if name.endswith(".tsv") else ","
    # Try UTF-8, fall back to latin-1
    try:
        return pd.read_csv(uploaded_file, sep=sep)
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, sep=sep, encoding="latin-1")


@st.cache_data(ttl=300, show_spinner=False)
def _fetch_url_text(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.text


def _parse_html_tables(html_text: str) -> List[pd.DataFrame]:
    try:
        return pd.read_html(html_text)
    except ValueError:
        return []


@st.cache_data(ttl=300, show_spinner=False)
def _fetch_api_json(api_url: str, headers: Optional[dict], params: Optional[dict]):
    resp = requests.get(api_url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def load_data() -> Optional[pd.DataFrame]:
    """Handle data loading from file upload, URL, API, or sample dataset."""
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)

    input_method = st.radio(
        "Select Data Source",
        ("Upload a File", "From Website URL", "From API", "Use Sample Data"),
        horizontal=True,
        key="data_source",
    )

    df = None

    if input_method == "Upload a File":
        uploaded_file = st.file_uploader(
            "📁 Choose a CSV or TSV file",
            type=["csv", "tsv"],
            help="Upload your CSV or TSV file for analysis. Maximum file size: 200MB",
        )
        if uploaded_file:
            try:
                size_mb = uploaded_file.size / (1024 * 1024)
                st.success(f"✅ Loaded: {uploaded_file.name} ({size_mb:.2f} MB)")
                df = _read_uploaded_delimited(uploaded_file)
            except Exception as e:
                st.error(f"❌ Error loading file: {e}")

    elif input_method == "From Website URL":
        with st.form("url_form", clear_on_submit=False):
            url = st.text_input(
                "Enter URL to fetch table data from:",
                value=st.session_state.pop("prefill_demo_url", ""),
                placeholder="e.g., https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)",
            )
            submitted = st.form_submit_button("Fetch Tables")
            
        if submitted and url:
            try:
                with st.spinner("Fetching tables from URL..."):
                    html_text = _fetch_url_text(url)
                    tables = _parse_html_tables(html_text)
                    
                if tables:
                    # Store tables in session state to prevent loss on refresh
                    st.session_state["fetched_tables"] = tables
                    st.session_state["fetched_url"] = url
                    st.success(f"✅ Found {len(tables)} table(s) on the page.")
                else:
                    st.warning("⚠️ No tables found on the provided URL.")
                    if "fetched_tables" in st.session_state:
                        del st.session_state["fetched_tables"]
                        
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Could not retrieve URL: {e}")
                if "fetched_tables" in st.session_state:
                    del st.session_state["fetched_tables"]
            except ImportError:
                st.error("❌ Parsing HTML tables requires 'lxml' or 'bs4'. Try: pip install lxml")
                if "fetched_tables" in st.session_state:
                    del st.session_state["fetched_tables"]
            except Exception as e:
                st.error(f"❌ Error parsing tables from URL: {e}")
                if "fetched_tables" in st.session_state:
                    del st.session_state["fetched_tables"]

        # Display table selection if tables are available in session state
        if "fetched_tables" in st.session_state and st.session_state["fetched_tables"]:
            tables = st.session_state["fetched_tables"]
            st.info(f"📊 Previously fetched {len(tables)} table(s) from: {st.session_state.get('fetched_url', 'Unknown URL')}")
            
            # Create labels for each table
            labels = [f"Table {i+1} (Shape: {t.shape})" for i, t in enumerate(tables)]
            
            # Table selection with unique key
            selected_idx = st.selectbox(
                "Select a table to analyze:",
                options=list(range(len(tables))),
                format_func=lambda i: labels[i],
                key="table_selector"
            )
            
            if selected_idx is not None:
                df = tables[selected_idx]
                st.success(f"✅ Selected: {labels[selected_idx]}")
                
                # Show table preview
                with st.expander("📋 Table Preview", expanded=True):
                    st.dataframe(df.head(10), use_container_width=True)
                    
                # Clear tables button
                if st.button("🗑️ Clear Fetched Tables", help="Clear cached tables to fetch new ones"):
                    if "fetched_tables" in st.session_state:
                        del st.session_state["fetched_tables"]
                    if "fetched_url" in st.session_state:
                        del st.session_state["fetched_url"]
                    st.rerun()

    elif input_method == "From API":
        with st.form("api_form", clear_on_submit=False):
            api_url = st.text_input("Enter the API endpoint URL:", placeholder="e.g., https://api.publicapis.org/entries")
            c1, c2 = st.columns(2)
            with c1:
                raw_headers = st.text_area("Optional request headers (JSON)", placeholder='{"Accept":"application/json"}')
            with c2:
                raw_params = st.text_area("Optional query params (JSON)", placeholder='{"page":1}')
            fetch = st.form_submit_button("Fetch Data from API")

        if fetch and api_url:
            try:
                headers = json.loads(raw_headers) if raw_headers.strip() else None
                params = json.loads(raw_params) if raw_params.strip() else None
            except json.JSONDecodeError:
                st.error("❌ Headers/Params must be valid JSON.")
                headers = params = None

            try:
                with st.spinner("Fetching data from API..."):
                    data = _fetch_api_json(api_url, headers=headers, params=params)

                if isinstance(data, list):
                    df = pd.DataFrame(data)
                elif isinstance(data, dict):
                    list_key = next((k for k, v in data.items() if isinstance(v, list)), None)
                    if list_key:
                        st.info(f"Found a list of records under the key: '{list_key}'")
                        df = pd.json_normalize(data, record_path=list_key)
                    else:
                        df = pd.json_normalize(data)
                else:
                    st.error("❌ The API did not return a standard JSON list or dictionary format.")

                if df is not None:
                    st.success("✅ Successfully loaded data from API.")
                    st.dataframe(df.head(), use_container_width=True)

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Could not retrieve data from API: {e}")
            except ValueError:
                st.error("❌ Failed to decode JSON from the API response. Please check the URL and API documentation.")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")

    elif input_method == "Use Sample Data":
        st.info("💡 Sample Dataset: Laptop specifications and prices for demonstration. Loading...")
        df = load_sample_data()

    st.markdown("</div>", unsafe_allow_html=True)
    return df