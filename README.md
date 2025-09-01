# 📊 InsightForge — EDA Dashboard

**A comprehensive Exploratory Data Analysis dashboard built with Streamlit** 

Analyze datasets quickly with interactive Overview, Univariate, and Bivariate visualizations — all in your browser with multiple data source options.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.49%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌐 Live Demo

**Try it now!** ➡️ **[InsightForge EDA Dashboard](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)**

No installation required — start analyzing your data immediately in your browser!

## 🏗️ Project Structure

```
InsightForge-EDA-Dashboard/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── Procfile                   # Deployment configuration
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
├── .python-version           # Python version specification
├── .gitignore                # Git ignore rules
├──
├── # Core Analysis Modules
├── univariate_analysis.py     # Single variable analysis
├── bivariate_analysis.py      # Two variable relationship analysis
├── overview.py                # Dataset overview wrapper
├── basic_data_clean.py        # Data cleaning wrapper
├── data_export.py             # Export functionality
├──
├── # Modular Components
├── components/
│   ├── __init__.py           # Package initialization
│   ├── styles.css            # Custom CSS styling
│   ├── welcome.py            # Welcome screen component
│   ├── state.py              # Session state management
│   ├── metrics.py            # Dataset metrics display
│   ├── load_data.py          # Multi-source data loading
│   ├── export_ui.py          # Export interface
│   ├──
│   ├── overview/             # Overview analysis module
│   │   ├── __init__.py
│   │   ├── view.py           # Main overview class
│   │   ├── sections.py       # Individual overview sections
│   │   └── helpers.py        # Cached computation helpers
│   ├──
│   └── cleaning/             # Data cleaning module
│       ├── __init__.py
│       ├── view.py           # Main cleaning interface
│       ├── sections.py       # Cleaning UI sections
│       └── helpers.py        # Cleaning utility functions
├──
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├──
└── __pycache__/              # Python bytecode cache
```

## ✨ Key Features & Improvements

### 🔍 **Advanced Data Loading System** ([`components.load_data`](components/load_data.py))
- **📁 File Upload**: CSV/TSV with automatic encoding detection (UTF-8/Latin-1)
- **🌐 Web Scraping**: Extract HTML tables from URLs with intelligent table selection
- **🔗 API Integration**: JSON data fetching with custom headers and parameters
- **🧪 Sample Dataset**: Pre-loaded laptop dataset for immediate testing
- **⚡ Caching**: Smart data caching for improved performance

### 📊 **Comprehensive Overview Analysis** ([`components.overview`](components/overview/))
- **📐 Dataset Metrics**: Shape, memory usage, and missing value tracking
- **📈 Statistical Summary**: Cached descriptive statistics for numerical columns
- **⚠️ Missing Value Analysis**: Visual charts and detailed breakdown
- **🧬 Data Type Distribution**: Interactive pie charts and column information
- **🔗 Correlation Matrix**: Smart correlation analysis with filtering options
- **🔠 Categorical Analysis**: Value counts with customizable display limits

### 📈 **Interactive Univariate Analysis** ([`univariate_analysis.py`](univariate_analysis.py))
- **🎯 Smart Column Detection**: Automatic numerical/categorical classification
- **📊 Multiple Plot Types**: 
  - **Numerical**: Histogram, Boxplot, Lineplot, Scatterplot, Density plots
  - **Categorical**: Countplot, Pie chart, Barplot with row limits
- **🔧 Null Value Handling**: Automatic filtering with user warnings
- **📏 Dynamic Binning**: Intelligent bin sizing for histograms
- **⚡ Performance Optimized**: Efficient rendering for large datasets

### 🔀 **Advanced Bivariate Analysis** ([`bivariate_analysis.py`](bivariate_analysis.py))
- **📊 Numerical vs Numerical**: Interactive Plotly scatter, line, box, density plots
- **🏷️ Categorical vs Categorical**: Grouped bars and cross-tabulation heatmaps
- **🔀 Numerical vs Categorical**: Box plots, violin plots, mean comparison bars
- **🎨 Interactive Visualizations**: Zoom, pan, hover with Plotly
- **📈 Category Management**: Smart handling of high-cardinality columns
- **📊 Statistical Insights**: Correlation coefficients and distribution summaries

### 🧹 **Advanced Data Cleaning System** ([`components.cleaning`](components/cleaning/))
- **🔢 Numerical Imputation**:
  - Mean, Median, Mode, Custom values
  - **🤖 KNN Imputation**: Scikit-learn based intelligent imputation
- **📝 Categorical Imputation**:
  - Mode, Custom text, "Unknown" handling
  - **🔬 Advanced KNN**: Optional fancyimpute integration with label encoding
- **🗑️ Column Management**: Interactive multi-select column dropping
- **📊 High Missing Detection**: Automatic >50% missing column identification
- **📋 Before/After Comparison**: Side-by-side data quality analysis
- **💾 State Management**: Session-based cleaned data persistence

### 📤 **Comprehensive Export System** ([`components.export_ui`](components/export_ui.py))
- **📄 Multiple Formats**: CSV, TSV, JSON, Excel with custom options
- **⚙️ Advanced Options**: Custom separators, JSON orientations, index handling
- **📊 Dual Export**: Original and cleaned data export options
- **💾 Smart Downloads**: Streamlit native download buttons with proper MIME types
- **📈 Export Metrics**: File size and data summary information

### 🎨 **Modern UI/UX Design** ([`main.py`](main.py) + [`components.styles`](components/styles.css))
- **🎨 Custom CSS**: Professional color scheme with CSS variables
- **📱 Responsive Design**: Mobile-friendly layout adaptation
- **🔄 Session State**: Intelligent state management for data consistency
- **⚡ Performance**: Smart caching and memory optimization
- **🛡️ Error Handling**: Comprehensive exception handling with user-friendly messages
- **🎯 Interactive Navigation**: Sidebar-based navigation with feature descriptions

## 🚀 Technical Architecture

### Core Design Principles
- **🏗️ Modular Architecture**: Separated concerns with dedicated modules
- **🔄 State Management**: Intelligent session state for data consistency
- **⚡ Performance Optimization**: Strategic caching and data sampling
- **🛡️ Error Resilience**: Comprehensive exception handling
- **🎨 User Experience**: Intuitive interface with helpful guidance

### Data Processing Pipeline
1. **📥 Data Ingestion**: Multi-source validation and preprocessing
2. **🔍 Type Detection**: Automatic numerical/categorical classification
3. **📊 Quality Assessment**: Missing value and data type analysis
4. **🔧 Interactive Processing**: Real-time parameter adjustment
5. **📈 Visualization**: Dynamic chart generation with Plotly/Matplotlib
6. **💾 State Persistence**: Smart session management for workflow continuity

### Technology Stack
- **🖥️ Frontend**: Streamlit with custom CSS styling
- **📊 Data Processing**: Pandas, NumPy for core data manipulation
- **📈 Visualization**: 
  - **Interactive**: Plotly Express for modern web-based charts
  - **Statistical**: Matplotlib, Seaborn for detailed analysis
- **🤖 Machine Learning**: Scikit-learn for KNN imputation
- **🌐 Web Integration**: Requests, BeautifulSoup for data fetching
- **📦 Optional**: FancyImpute for advanced missing value handling

## 💻 Local Development

### Quick Start
```bash
# Clone the repository
git clone https://github.com/ShaikhHamza104/InsightForge-EDA-Dashboard-Streamlit-.git
cd InsightForge-EDA-Dashboard-Streamlit-

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

### Development Setup
```bash
# Optional: Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with optional advanced features
pip install -r requirements.txt
pip install fancyimpute  # For advanced imputation methods
```

## 🧪 Usage Examples

### Multi-Source Data Loading
```python
# File Upload: Automatic CSV/TSV detection with encoding fallback
# URL Scraping: "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
# API Integration: REST endpoints with custom headers/parameters
# Sample Data: Pre-loaded laptop dataset for testing
```

### Comprehensive Analysis Workflow
```python
# 1. Overview: Dataset metrics, correlations, missing value analysis
# 2. Univariate: Individual variable distributions and patterns
# 3. Bivariate: Relationship analysis between variable pairs
# 4. Cleaning: Advanced missing value imputation and data preparation
# 5. Export: Multi-format downloads with customization options
```

## 📋 Dependencies

### Core Requirements
```txt
# Data & Computing
pandas>=2.3.2           # Data manipulation and analysis
numpy>=2.3.2            # Numerical computing foundation
streamlit>=1.49.1       # Web application framework

# Visualization
plotly>=5.24.1          # Interactive visualizations
matplotlib>=3.10.6      # Statistical plotting
seaborn>=0.13.2         # Enhanced statistical visualizations

# Machine Learning & Data Processing
scikit-learn            # KNN imputation and preprocessing
scipy                   # Scientific computing
statsmodels             # Statistical modeling

# Web & Data Fetching
requests>=2.32.5        # HTTP requests for APIs/URLs
lxml>=4.9.0             # HTML/XML parsing for web scraping
```

### Optional Advanced Features
```txt
# Advanced Imputation (Optional)
fancyimpute             # Sophisticated missing value imputation
knnimpute               # Enhanced KNN imputation methods

# Optimization (Optional)
cvxpy                   # Convex optimization
cvxopt                  # Optimization algorithms
osqp                    # Quadratic programming
scs                     # Conic optimization

# Utilities
joblib                  # Efficient data persistence
altair                  # Alternative visualization library
```

## 🔧 Configuration

### Streamlit Configuration ([`.streamlit/config.toml`](.streamlit/config.toml))
```toml
[server]
headless = true
enableCORS = false
```

### Deployment ([`Procfile`](Procfile))
```
web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
```

## 📞 Contact & Support

**Created by**: [Shaikh Hamza](https://github.com/ShaikhHamza104)

- **🌐 Live Demo**: [Try it here](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)
- **📁 Repository**: [GitHub Repository](https://github.com/ShaikhHamza104/InsightForge-EDA-Dashboard-Streamlit-)
- **🐛 Issues**: Report bugs via GitHub Issues
- **💡 Feature Requests**: Submit enhancement requests
- **📧 Contact**: Reach out through GitHub

## 📄 License

MIT License - see [`LICENSE`](LICENSE) file for details.

---

<div align="center">

**🌐 [Try the Live Demo](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)** | ⭐ **Star if helpful!** ⭐

*Built with Python, Streamlit, and modern data science libraries*

</div>