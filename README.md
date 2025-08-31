# InsightForge — EDA Dashboard (Streamlit)

Analyze datasets quickly with interactive Overview, Univariate, and Bivariate visualizations — all in your browser.

- Built with Streamlit, Plotly, Seaborn, and Matplotlib
- Upload your CSV or explore with a sample dataset
- Clean UI with metrics, warnings, and rich charts

## Demo

- Launch locally: `streamlit run main.py`
- Navigate via sidebar:
  - Overview
  - Univariate Analysis
  - Bivariate Analysis

## Features

- Overview
  - Dataset shape, head/tail, numerical summary, missing values table
  - Data types, detailed dtype listing, correlation heatmap
- Univariate Analysis
  - Numeric: Histogram, Boxplot, Lineplot, Scatterplot, Density
  - Categorical: Countplot, Pie chart, Barplot
  - Null handling with clear warnings
- Bivariate Analysis
  - Numerical vs Numerical: Scatter, Line, Box, Density, Heatmap (correlation)
  - Categorical vs Categorical: Grouped Bar, Heatmap (crosstab)
  - Numerical vs Categorical: Box, Violin, Mean Bar
  - Category limiting for heavy-cardinality columns

## Quick Start

1) Create and activate a virtual environment
- Windows
  - Python 3.11+ recommended
  - `py -m venv .venv`
  - `.venv\Scripts\activate`
- macOS/Linux
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`

2) Install dependencies
- Preferred: `pip install -r requirements.txt` ([requirements.txt](requirements.txt))
- If your requirements file appears garbled, install the core libs:
  - `pip install streamlit pandas numpy seaborn matplotlib plotly`

3) Run the app
- `streamlit run main.py` ([main.py](main.py))

## Using the App

- Upload a CSV via the uploader or check “Use sample data”
- Review metrics at the top (Rows, Columns, Missing Values)
- Choose an analysis mode from the sidebar

### Modules

- App entry and routing: [main.py](main.py)
  - Instantiates analysis classes and renders pages
- Overview: [overview.py](overview.py)
  - Class: [`overview.Overview`](overview.py)
  - Method: `display_overview` (dataset shape, preview, stats, missing values, dtypes, correlation)
- Univariate: [univariate_analysis.py](univariate_analysis.py)
  - Class: [`univariate_analysis.UnivariateAnalysis`](univariate_analysis.py)
  - Method: `display` (column selection, plot type, null-safe plotting)
- Bivariate: [bivariate_analysis.py](bivariate_analysis.py)
  - Class: [`bivariate_analysis.BivariateAnalysis`](bivariate_analysis.py)
  - Methods: `column_vs_column_display`, `numerical_vs_numerical`, `categorical_vs_categorical`, `numerical_vs_categorical`

## Project Structure

```
.
├─ main.py
├─ overview.py
├─ univariate_analysis.py
├─ bivariate_analysis.py
├─ requirements.txt
```

## Tips & Troubleshooting

- CSV encoding errors: try re-saving as UTF-8 or load with a specific encoding in your own preprocessing.
- Large categorical columns: use the “Max categories to display” slider to keep charts readable.
- Missing values: charts exclude NaNs and warn you when applicable.
- Correlation NaNs: the Overview fills NaNs as 0 for heatmap display.

## License

MIT — feel free to use and adapt. Update this section if you choose a