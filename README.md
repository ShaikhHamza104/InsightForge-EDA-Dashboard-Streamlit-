# 📊 InsightForge — EDA Dashboard

**A comprehensive Exploratory Data Analysis dashboard built with Streamlit** 

Analyze datasets quickly with interactive Overview, Univariate, and Bivariate visualizations — all in your browser with multiple data source options.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.49%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌐 Live Demo

**Try it now!** ➡️ **[InsightForge EDA Dashboard](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)**

No installation required — start analyzing your data immediately in your browser!

## ✨ Features I Created

### 🔍 **Multiple Data Source Integration** ([main.py](main.py))
- **📁 File Upload**: CSV and TSV support with automatic delimiter detection
- **🌐 Web Scraping**: Extract HTML tables directly from website URLs using pandas
- **🔗 API Integration**: Fetch and process JSON data from REST APIs with error handling
- **🧪 Sample Dataset**: Pre-loaded laptop dataset for immediate testing

### 📊 **Comprehensive Overview Analysis** ([overview.py](overview.py))
- **Dataset Metrics**: Real-time shape, memory usage, and missing value tracking
- **Statistical Summary**: Automatic descriptive statistics for numerical columns
- **Missing Value Analysis**: Visual charts and detailed breakdown of null values
- **Data Type Distribution**: Pie charts and detailed column information
- **Correlation Matrix**: Interactive heatmaps with customizable filtering
- **Categorical Analysis**: Value counts and distribution visualizations

### 📈 **Interactive Univariate Analysis** ([univariate_analysis.py](univariate_analysis.py))
- **Smart Column Detection**: Automatic separation of numerical and categorical data
- **Multiple Plot Types**: 
  - **Numerical**: Histogram, Boxplot, Lineplot, Scatterplot, Density plots
  - **Categorical**: Countplot, Pie chart, Barplot with customizable row limits
- **Null Value Handling**: Automatic filtering with user warnings
- **Dynamic Binning**: Intelligent bin sizing for histograms

### 🔀 **Advanced Bivariate Analysis** ([bivariate_analysis.py](bivariate_analysis.py))
- **Three Analysis Types**:
  - **Numerical vs Numerical**: Scatter, Line, Box, Density, and Correlation heatmaps
  - **Categorical vs Categorical**: Grouped bars and Cross-tabulation heatmaps
  - **Numerical vs Categorical**: Box plots, Violin plots, and Mean comparison bars
- **Interactive Plotly Charts**: Zoom, pan, and hover functionality
- **Category Limiting**: Smart handling of high-cardinality columns
- **Statistical Insights**: Correlation coefficients and distribution summaries

### 🧹 **Advanced Data Cleaning System** ([basic_data_clean.py](basic_data_clean.py))
- **Missing Value Imputation**:
  - **Numerical**: Mean, Median, Mode, Custom values, KNN imputation
  - **Categorical**: Mode, Custom text, Advanced KNN with label encoding
- **Column Management**: Interactive column dropping with multi-selection
- **High Missing Value Detection**: Automatic identification and removal of >50% missing columns
- **Before/After Comparison**: Side-by-side data quality comparison
- **Advanced Imputation**: Optional fancyimpute integration for sophisticated missing value handling

### 🎨 **Modern UI/UX Design** ([main.py](main.py))
- **Custom CSS Styling**: Professional color scheme and responsive design
- **Tabbed Interface**: Organized data cleaning workflow
- **Interactive Metrics**: Real-time dataset statistics display
- **Error Handling**: Comprehensive error messages and user guidance
- **Performance Optimization**: Data caching and memory monitoring

## 🚀 Technical Implementation

### Architecture
- **Modular Design**: Each analysis type in separate Python modules
- **Class-Based Structure**: OOP approach for maintainable code
- **Error Resilience**: Comprehensive exception handling throughout
- **Memory Efficient**: Smart data sampling and caching strategies

### Data Processing Pipeline
1. **Data Loading**: Multiple source validation and preprocessing
2. **Type Detection**: Automatic numerical/categorical classification
3. **Quality Assessment**: Missing value and data type analysis
4. **Interactive Analysis**: Real-time parameter adjustment
5. **Visualization**: Dynamic chart generation with Plotly/Matplotlib

### Key Technologies
- **Frontend**: Streamlit with custom CSS
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (interactive), Matplotlib, Seaborn
- **ML/Statistics**: Scikit-learn KNN imputation, Statistical analysis
- **Web Integration**: Requests, BeautifulSoup for data fetching

## 💻 Local Development

```bash
git clone https://github.com/ShaikhHamza104/InsightForge-EDA-Dashboard-Streamlit-.git
cd InsightForge-EDA-Dashboard-Streamlit-
pip install -r requirements.txt
streamlit run main.py
```

## 🧪 Usage Examples

### Load Data from Multiple Sources
```python
# File upload with automatic delimiter detection
# URL scraping with table selection
# API integration with JSON processing
# Sample dataset for immediate testing
```

### Perform Comprehensive Analysis
```python
# Overview: Dataset metrics and correlations
# Univariate: Single variable distributions
# Bivariate: Variable relationships
# Cleaning: Missing value imputation
```

## 📋 Dependencies

```txt
# Core Libraries
pandas>=2.3.2          # Data manipulation
streamlit>=1.49.1       # Web framework
plotly>=5.24.1          # Interactive charts
matplotlib>=3.10.6      # Statistical plots
seaborn>=0.13.2         # Statistical visualization
numpy>=2.3.2            # Numerical computing

# Data Processing
scikit-learn            # ML algorithms
requests>=2.32.5        # HTTP requests
lxml>=4.9.0             # HTML parsing

# Optional Advanced Features
fancyimpute             # Advanced imputation
knnimpute               # KNN imputation
```

## 📞 Contact & Support

**Created by**: [Shaikh Hamza](https://github.com/ShaikhHamza104)

- **🌐 Live Demo**: [Try it here](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)
- **🐛 Issues**: Report bugs via GitHub Issues
- **💡 Features**: Submit enhancement requests
- **📧 Contact**: Reach out through GitHub

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**🌐 [Try the Live Demo](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)** | ⭐ **Star if helpful!** ⭐

*Built with Python, Streamlit, and modern data science libraries*

</div>