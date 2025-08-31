import streamlit as st
import io
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class Overview:

    def __init__(self, df):
        self.df = df

    def display_overview(self):
        st.title("📋 Dataset Overview")
        st.markdown("Get a comprehensive summary of your dataset including shape, statistics, missing values, and correlations.")

        if self.df is None or self.df.empty:
            st.warning("⚠️ The dataset is empty. Please upload data to see the overview.")
            return

        # Dataset shape at the top for immediate context
        st.subheader("📐 Dataset Dimensions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Rows", f"{self.df.shape[0]:,}")
        with col2:
            st.metric("📈 Total Columns", f"{self.df.shape[1]}")
        with col3:
            memory_usage = self.df.memory_usage(deep=True).sum() / 1024**2
            st.metric("💾 Memory Usage", f"{memory_usage:.2f} MB")
        
        # Data preview with tabs for better organization
        st.subheader("🔍 Data Preview")
        tab1, tab2, tab3 = st.tabs(["📄 First 5 Rows", "📄 Last 5 Rows", "🎲 Random Sample"])
        
        with tab1:
            st.dataframe(self.df.head(), use_container_width=True)
        with tab2:
            st.dataframe(self.df.tail(), use_container_width=True)
        with tab3:
            if len(self.df) >= 5:
                st.dataframe(self.df.sample(min(5, len(self.df))), use_container_width=True)
            else:
                st.info("Dataset too small for random sampling")

        # Summary statistics for numerical columns
        st.subheader("📈 Summary Statistics")
        numeric_df = self.df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            st.dataframe(numeric_df.describe(), use_container_width=True)
            
            # Additional statistics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🔢 Numerical Columns", len(numeric_df.columns))
            with col2:
                total_numeric_nulls = numeric_df.isnull().sum().sum()
                st.metric("⚠️ Numerical Nulls", f"{total_numeric_nulls:,}")
        else:
            st.info("ℹ️ No numerical columns available for statistics.")

        # Missing values analysis
        st.subheader("⚠️ Missing Values Analysis")
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df)) * 100
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Count': missing.values,
            'Missing Percentage (%)': missing_percent.round(2)
        })
        
        # Only show columns with missing values
        missing_with_nulls = missing_df[missing_df['Missing Count'] > 0]
        
        if not missing_with_nulls.empty:
            st.dataframe(missing_with_nulls.sort_values('Missing Count', ascending=False), 
                        use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📊 Columns with Missing Values", len(missing_with_nulls))
            with col2:
                st.metric("🔢 Total Missing Values", f"{missing.sum():,}")
                
            # Visualization of missing values
            if len(missing_with_nulls) <= 20:  # Only show chart if manageable number of columns
                fig, ax = plt.subplots(figsize=(10, 6))
                missing_with_nulls.plot(x='Column', y='Missing Percentage (%)', 
                                       kind='bar', ax=ax, color='coral')
                plt.title('Missing Values by Column')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
        else:
            st.success("✅ Excellent! No missing values found in the dataset!")

        # Data types with counts
        st.subheader("🧬 Data Types Analysis")
        try:
            # Convert dtype objects to strings to avoid PyArrow conversion issues
            dtype_counts = pd.DataFrame({
                'Data Type': self.df.dtypes.astype(str).value_counts().index,
                'Count': self.df.dtypes.astype(str).value_counts().values
            })
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.dataframe(dtype_counts, hide_index=True)
            with col2:
                # Pie chart of data types
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.pie(dtype_counts['Count'], labels=dtype_counts['Data Type'], autopct='%1.1f%%')
                ax.set_title('Distribution of Data Types')
                st.pyplot(fig)
            
            # Detailed data types
            with st.expander("🔍 Show detailed column information"):
                dtypes_df = pd.DataFrame({
                    'Column': self.df.columns, 
                    'Data Type': [str(dtype) for dtype in self.df.dtypes.values],
                    'Non-Null Count': [self.df[col].count() for col in self.df.columns],
                    'Unique Values': [self.df[col].nunique() for col in self.df.columns]
                })
                st.dataframe(dtypes_df, use_container_width=True, hide_index=True)
                
        except Exception as e:
            st.error(f"❌ Error displaying data types: {str(e)}")

        # Value counts for categorical columns
        st.subheader("🔠 Categorical Data Analysis")
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if categorical_cols:
            selected_col = st.selectbox("📊 Select a categorical column for detailed analysis:", 
                                        categorical_cols)
            
            # Show top categories and their counts
            value_counts = self.df[selected_col].value_counts()
            total_categories = len(value_counts)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🏷️ Unique Categories", total_categories)
            with col2:
                st.metric("🥇 Most Common", f"{value_counts.iloc[0]} occurrences")
            with col3:
                if total_categories > 1:
                    st.metric("🥈 Second Most Common", f"{value_counts.iloc[1]} occurrences")
            
            # Display value counts
            if total_categories > 10:
                st.info(f"📊 Column has {total_categories} unique values. Showing top 10.")
                display_counts = value_counts.head(10)
            else:
                display_counts = value_counts
                
            st.dataframe(display_counts.to_frame('Count'), use_container_width=True)
            
            # Visualization
            if len(display_counts) <= 15:  # Only create chart for manageable number of categories
                fig, ax = plt.subplots(figsize=(10, 6))
                display_counts.plot(kind='bar', ax=ax, color='skyblue')
                plt.title(f'Top Categories in {selected_col}')
                plt.xticks(rotation=45, ha='right')
                plt.ylabel('Count')
                plt.tight_layout()
                st.pyplot(fig)
        else:
            st.info("ℹ️ No categorical columns found in the dataset.")

        # Correlation analysis
        st.subheader("🔗 Correlation Analysis")
        
        # Select only numerical columns for correlation
        numerical_df = self.df.select_dtypes(include=['number'])
        if not numerical_df.empty:
            # Drop columns with all NaN values
            numerical_df = numerical_df.dropna(axis=1, how='all')
            
            if not numerical_df.empty and len(numerical_df.columns) > 1:
                # If too many columns, let the user choose
                if numerical_df.shape[1] > 15:
                    st.warning(f"⚠️ Dataset has {numerical_df.shape[1]} numerical columns. Large correlation matrices can be hard to read.")
                    
                    analysis_option = st.radio(
                        "Choose correlation analysis approach:",
                        ["Show top correlations", "Select specific columns", "Show full matrix"]
                    )
                    
                    if analysis_option == "Show top correlations":
                        # Calculate correlation and show strongest correlations
                        corr_matrix = numerical_df.corr()
                        
                        # Get upper triangle of correlation matrix
                        upper_tri = corr_matrix.where(
                            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
                        )
                        
                        # Find strongest correlations
                        strong_corr = []
                        for column in upper_tri.columns:
                            for row in upper_tri.index:
                                if not pd.isna(upper_tri.loc[row, column]):
                                    strong_corr.append({
                                        'Variable 1': row,
                                        'Variable 2': column,
                                        'Correlation': upper_tri.loc[row, column]
                                    })
                        
                        strong_corr_df = pd.DataFrame(strong_corr)
                        strong_corr_df = strong_corr_df.reindex(
                            strong_corr_df['Correlation'].abs().sort_values(ascending=False).index
                        ).head(10)
                        
                        st.dataframe(strong_corr_df, use_container_width=True, hide_index=True)
                        
                    elif analysis_option == "Select specific columns":
                        selected_cols = st.multiselect(
                            "📊 Select columns for correlation analysis (max 15 recommended):",
                            numerical_df.columns.tolist(),
                            default=numerical_df.columns.tolist()[:min(10, len(numerical_df.columns))]
                        )
                        if selected_cols:
                            numerical_df = numerical_df[selected_cols]
                        else:
                            st.info("Please select at least one column.")
                            return
                    # For "Show full matrix", we use the full numerical_df
                
                try:
                    # Calculate correlation and handle potential errors
                    corr = numerical_df.corr()
                    
                    # Handle NaN values in correlation matrix
                    if corr.isnull().any().any():
                        st.warning("⚠️ Some correlation values are NaN (likely due to constant values) and will be shown as 0.")
                        corr = corr.fillna(0)
                    
                    # Create heatmap
                    fig, ax = plt.subplots(figsize=(12, 10))
                    
                    # Create mask for upper triangle to avoid redundancy
                    mask = np.triu(np.ones_like(corr, dtype=bool))
                    
                    # Generate heatmap
                    sns.heatmap(corr, 
                               annot=True, 
                               cmap='RdBu_r', 
                               mask=mask, 
                               fmt='.2f', 
                               linewidths=0.5, 
                               ax=ax, 
                               annot_kws={"size": 8},
                               center=0,
                               vmin=-1, 
                               vmax=1)
                    
                    plt.title('Correlation Matrix (Lower Triangle)', fontsize=14, pad=20)
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Summary statistics for correlations
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        max_corr = corr.where(~np.eye(corr.shape[0], dtype=bool)).max().max()
                        st.metric("🔺 Strongest Positive Correlation", f"{max_corr:.3f}")
                    with col2:
                        min_corr = corr.where(~np.eye(corr.shape[0], dtype=bool)).min().min()
                        st.metric("🔻 Strongest Negative Correlation", f"{min_corr:.3f}")
                    with col3:
                        avg_corr = corr.where(~np.eye(corr.shape[0], dtype=bool)).abs().mean().mean()
                        st.metric("📊 Average Absolute Correlation", f"{avg_corr:.3f}")
                        
                except Exception as e:
                    st.error(f"❌ Error generating correlation matrix: {str(e)}")
            else:
                st.info("ℹ️ Need at least 2 numerical columns with valid data for correlation analysis.")
        else:
            st.info("ℹ️ No numerical columns available for correlation matrix.")

        # Final summary
        st.subheader("📋 Dataset Summary")
        
        summary_data = {
            "Metric": [
                "Total Rows", "Total Columns", "Numerical Columns", "Categorical Columns",
                "Total Missing Values", "Memory Usage (MB)", "Complete Rows"
            ],
            "Value": [
                f"{self.df.shape[0]:,}",
                f"{self.df.shape[1]}",
                f"{len(self.df.select_dtypes(include=['number']).columns)}",
                f"{len(self.df.select_dtypes(include=['object', 'category']).columns)}",
                f"{self.df.isnull().sum().sum():,}",
                f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f}",
                f"{len(self.df.dropna()):,}"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

# Run app only if script is executed directly
if __name__ == "__main__":
    try:
        df = pd.read_csv('https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/refs/heads/master/laptop_cleaning.csv')
        overview = Overview(df)
        overview.display_overview()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")