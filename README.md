# 📊 InsightForge — EDA Dashboard

**A comprehensive Exploratory Data Analysis dashboard built with Streamlit** 

Analyze datasets quickly with interactive Overview, Univariate, and Bivariate visualizations — all in your browser with multiple data source options.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.49%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌐 Live Demo

**Try it now!** ➡️ **[InsightForge EDA Dashboard](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)**

No installation required — start analyzing your data immediately in your browser!

## ✨ Key Features

🔍 **Multiple Data Sources**
- 📁 **File Upload**: CSV and TSV files with drag-and-drop support
- 🌐 **Web Scraping**: Extract tables directly from website URLs
- 🔗 **API Integration**: Fetch data from REST APIs with JSON response handling
- 🧪 **Sample Dataset**: Pre-loaded laptop specifications dataset for testing

📊 **Comprehensive Analysis**
- **Overview**: Dataset summary, statistics, missing values, correlations
- **Univariate**: Single variable analysis with interactive visualizations
- **Bivariate**: Two-variable relationship analysis with smart categorization

🎨 **Interactive Visualizations**
- Built with **Plotly** for rich, interactive charts
- **Seaborn** and **Matplotlib** integration for statistical plots
- Real-time parameter adjustment and filtering

⚡ **Performance Optimized**
- Caching for faster data loading
- Memory usage monitoring
- Efficient handling of large datasets

## 🚀 Demo

### 🌐 Online Demo (Recommended)
**Access instantly:** [https://insightforge-eda-dashboard-streamlit-1.onrender.com/](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)
- No setup required
- Try all features immediately
- Perfect for quick data analysis

### 💻 Local Development
```bash
git clone https://github.com/ShaikhHamza104/InsightForge-EDA-Dashboard-Streamlit-.git
cd InsightForge-EDA-Dashboard-Streamlit-
pip install -r requirements.txt
streamlit run main.py
```

### Navigation
Use the sidebar to switch between analysis types:
- 📋 **Overview**: Dataset summary and insights
- 📊 **Univariate Analysis**: Single variable exploration
- 📈 **Bivariate Analysis**: Variable relationships

## 💡 Usage Guide

### Getting Started
1. **Access the App**: Visit the [live demo](https://insightforge-eda-dashboard-streamlit-1.onrender.com/) or run locally
2. **Select Data Source**: Choose from upload, URL, API, or sample dataset
3. **Load Your Data**: Follow the on-screen instructions for your chosen method
4. **Review Metrics**: Check the dataset overview metrics
5. **Choose Analysis**: Use the sidebar to navigate between analysis types
6. **Interact**: Customize visualizations with the available controls

### Data Source Options

#### 📁 File Upload
- **Supported Formats**: CSV, TSV
- **Max File Size**: 200MB
- **Encoding**: UTF-8 recommended
- **Features**: Automatic delimiter detection

#### 🌐 Website URL
- **Extract Tables**: Automatically finds and parses HTML tables
- **Multiple Tables**: Select from available tables on the page
- **Example**: Wikipedia tables, data repositories

#### 🔗 API Integration
- **JSON APIs**: Handles REST API responses
- **Nested Data**: Automatically flattens complex JSON structures
- **Timeout**: 10-second request timeout for reliability

#### 🧪 Sample Dataset
- **Laptop Specifications**: Pre-loaded dataset with 1000+ records
- **16 Columns**: Mixed numerical and categorical data
- **Perfect for Testing**: Demonstrates all dashboard features

## 💡 Tips & Troubleshooting

### Common Issues & Solutions

#### 📁 File Upload Issues
- **Encoding Errors**: Save your CSV as UTF-8 encoding
- **Large Files**: Use the sample dataset feature for testing
- **Format Problems**: Ensure proper CSV/TSV format with headers

#### 🌐 Web Scraping Issues
- **No Tables Found**: Check if the webpage contains HTML tables
- **Access Denied**: Some websites block automated requests
- **Timeout**: Website may be slow; try again later

#### 🔗 API Integration Issues
- **JSON Parse Error**: Ensure the API returns valid JSON
- **Network Timeout**: Check your internet connection
- **API Limits**: Some APIs have rate limiting

#### 📊 Visualization Issues
- **Large Categories**: Use the "Max categories" slider to limit display
- **Missing Values**: Charts automatically exclude NaN values with warnings
- **Performance**: For large datasets, use data sampling options

#### 🧮 Analysis Issues
- **Correlation NaNs**: Overview automatically handles NaN values in correlation matrix
- **Empty Data**: Application gracefully handles empty or invalid datasets
- **Mixed Types**: Automatic type detection works with most data formats

### Performance Tips
- **Large Datasets**: Use the row limiting features in bivariate analysis
- **High Cardinality**: Limit categories using the slider controls
- **Memory Usage**: Monitor memory metrics in the overview section
- **Caching**: Sample data is cached for faster loading

### Best Practices
- **Data Quality**: Clean your data before analysis for best results
- **Column Names**: Use descriptive column names for better insights
- **Data Types**: Ensure proper data types are detected
- **Backup Data**: Keep original data files as backup

## 🚀 Deployment

### Local Development
```bash
streamlit run main.py
```

### Production Deployment

#### 🌐 Live Demo (Current)
The application is currently deployed at: [https://insightforge-eda-dashboard-streamlit-1.onrender.com/](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)

#### Render.com (Recommended)
1. **Fork this repository**
2. **Connect to Render**: Link your GitHub repository
3. **Configure**: Select "Web Service" and use Python environment
4. **Deploy**: Automatic deployment with GitHub integration
5. **Custom Domain**: Optional custom domain configuration

#### Heroku
1. **Fork this repository**
2. **Connect to Heroku**: Link your GitHub repository
3. **Deploy**: Heroku will automatically use the included `Procfile`
4. **Environment**: Uses the provided `requirements.txt`

#### Streamlit Cloud
1. **Connect Repository**: Link your GitHub account
2. **Select Branch**: Deploy from main branch
3. **Configure**: Use `main.py` as entry point
4. **Deploy**: Automatic deployment with GitHub integration

#### Docker (Advanced)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
```

## 🧪 Testing

The project includes comprehensive testing:

```bash
# Run the test suite
python test_main.py
```

**Test Coverage:**
- ✅ Import validation
- ✅ Data loading from all sources
- ✅ Analysis module initialization
- ✅ Edge case handling
- ✅ Error handling
- ✅ Performance metrics

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Implement your feature or fix
4. **Add Tests**: Ensure your changes work correctly
5. **Commit Changes**: `git commit -m 'Add amazing feature'`
6. **Push Branch**: `git push origin feature/amazing-feature`
7. **Create Pull Request**: Submit your changes for review

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Include error handling for new features
- Test with different data types and sizes
- Update documentation as needed

## 📋 Dependencies

### Core Requirements
```txt
streamlit>=1.49.1      # Web app framework
pandas>=2.3.2          # Data manipulation
plotly>=5.24.1         # Interactive plotting
seaborn>=0.13.2        # Statistical plotting
matplotlib>=3.10.6     # Base plotting library
numpy>=2.3.2           # Numerical computing
requests>=2.32.5       # HTTP requests
lxml>=4.9.0            # HTML/XML parsing
html5lib>=1.1          # HTML parsing
```

### Development Requirements
```txt
pytest                 # Testing framework
black                  # Code formatting
flake8                 # Code linting
jupyter               # Notebook development
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Shaikh Hamza

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🌟 Acknowledgments

- **Streamlit Team** - For the amazing web app framework
- **Plotly** - For interactive visualization capabilities
- **Pandas Community** - For powerful data manipulation tools
- **Open Source Community** - For inspiration and contributions

## 📞 Support

Having issues? Here's how to get help:

- **🌐 Live Demo**: Try the [online version](https://insightforge-eda-dashboard-streamlit-1.onrender.com/) first
- **📖 Documentation**: Check this README and inline help text
- **🐛 Bug Reports**: Open an issue on GitHub
- **💡 Feature Requests**: Submit enhancement ideas via GitHub issues
- **📧 Contact**: Reach out to the maintainer through GitHub

---

<div align="center">

**Made with ❤️ by [Shaikh Hamza](https://github.com/ShaikhHamza104)**

🌐 **[Try the Live Demo](https://insightforge-eda-dashboard-streamlit-1.onrender.com/)** | ⭐ **Star this repository if you found it helpful!** ⭐

</div>