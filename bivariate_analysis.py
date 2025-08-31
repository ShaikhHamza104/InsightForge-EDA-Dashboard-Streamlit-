import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

class BivariateAnalysis:
    def __init__(self, df):
        self.df = df
        
        if self.df is None or self.df.empty:
            self.numerical_columns = []
            self.categorical_columns = []
            return
            
        # Safely identify column types
        self.numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Ensure categorical columns contain string values
        for col in self.categorical_columns[:]:  # Use slice copy to avoid modification during iteration
            try:
                self.df[col] = self.df[col].fillna('Missing').astype(str)
            except Exception:
                # If conversion fails, remove from categorical columns
                self.categorical_columns.remove(col)

    def column_vs_column_display(self):
        st.title("📈 Bivariate Analysis with Interactive Plotly")
        st.markdown("""
        Explore relationships between two variables with interactive visualizations.
        Choose your analysis type based on the variable types you want to compare.
        """)

        if self.df is None or self.df.empty:
            st.warning("⚠️ No data available for analysis. Please upload a dataset first.")
            return
            
        if not self.numerical_columns and not self.categorical_columns:
            st.error("❌ No suitable columns found for analysis. The dataset might be empty or contains unsupported data types.")
            return

        # Show available column types
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📊 **Numerical columns**: {len(self.numerical_columns)}")
        with col2:
            st.info(f"🏷️ **Categorical columns**: {len(self.categorical_columns)}")

        # Determine available analysis options based on data
        analysis_options = []
        if len(self.numerical_columns) >= 2:
            analysis_options.append("📊 Numerical vs Numerical")
        if len(self.categorical_columns) >= 2:
            analysis_options.append("🏷️ Categorical vs Categorical")
        if self.numerical_columns and self.categorical_columns:
            analysis_options.append("🔀 Numerical vs Categorical")
            
        if not analysis_options:
            st.warning("⚠️ Not enough columns of compatible types for bivariate analysis.")
            st.info("💡 **Requirements**: You need at least 2 columns of the same type, or 1 numerical and 1 categorical column.")
            return
            
        analysis_type = st.selectbox("🎯 Select Analysis Type", analysis_options)

        if analysis_type == "📊 Numerical vs Numerical":
            self.numerical_vs_numerical()
        elif analysis_type == "🏷️ Categorical vs Categorical":
            self.categorical_vs_categorical()
        elif analysis_type == "🔀 Numerical vs Categorical":
            self.numerical_vs_categorical()

    def numerical_vs_numerical(self):
        st.subheader("📊 Numerical vs Numerical Analysis")
        st.info("💡 Explore relationships, correlations, and patterns between two numerical variables.")
        
        if len(self.numerical_columns) < 2:
            st.warning("⚠️ Need at least 2 numerical columns for this analysis.")
            return
            
        # Column selection with better UX
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("📈 Select X-axis (Independent Variable)", self.numerical_columns, key='num_x')
        with col2:
            remaining_cols = [col for col in self.numerical_columns if col != x_col]
            y_col = st.selectbox("📉 Select Y-axis (Dependent Variable)", remaining_cols, key='num_y')
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            max_rows = len(self.df)
            rows = st.slider("📊 Number of data points to analyze", 
                           min_value=10, 
                           max_value=max_rows, 
                           value=min(max_rows, 1000),
                           help="Reduce for faster rendering on large datasets")
            
            color_col = st.selectbox("🎨 Color by (optional)", 
                                   [None] + self.categorical_columns, 
                                   help="Add a third dimension by coloring points by a categorical variable")
        
        plot_options = {
            'Scatterplot': 'Best for showing correlation and outliers',
            'Lineplot': 'Good for time series or ordered data',
            'Boxplot': 'Compare distributions when X-axis has few unique values',
            'Densityplot': 'Shows concentration areas and patterns',
            'Heatmap': 'Display correlation strength'
        }
        
        plot_type = st.selectbox("📊 Select Visualization Type", 
                               list(plot_options.keys()),
                               help="Each plot type reveals different aspects of the relationship")
        
        # Show plot description
        st.markdown(f"**📝 About {plot_type}**: {plot_options[plot_type]}")

        st.markdown(f"### 📊 {x_col} vs {y_col}")
        
        # Handle NaN values
        df_clean = self.df[[x_col, y_col]].dropna()
        if df_clean.empty:
            st.error("❌ No valid data points after removing NaN values.")
            return
            
        if len(df_clean) < rows:
            st.info(f"ℹ️ Dataset has {len(df_clean)} valid data points (less than requested {rows})")
            df_display = df_clean
        else:
            df_display = df_clean.head(rows)

        try:
            # Add color column if selected
            if color_col and color_col in self.df.columns:
                df_display = df_display.copy()
                df_display[color_col] = self.df[color_col].head(len(df_display))
                color_param = color_col
            else:
                color_param = None

            if plot_type == 'Scatterplot':
                fig = px.scatter(df_display, x=x_col, y=y_col, 
                               color=color_param,
                               title=f'Scatter Plot: {x_col} vs {y_col}',
                               trendline="ols" if color_param is None else None)
            elif plot_type == 'Lineplot':
                df_sorted = df_display.sort_values(by=x_col)
                fig = px.line(df_sorted, x=x_col, y=y_col, 
                             color=color_param,
                             title=f'Line Plot: {x_col} vs {y_col}')
            elif plot_type == 'Boxplot':
                # For boxplot, we need to bin the x variable if it's continuous
                if df_display[x_col].nunique() > 10:
                    df_display_copy = df_display.copy()
                    df_display_copy[f'{x_col}_binned'] = pd.cut(df_display_copy[x_col], bins=10)
                    fig = px.box(df_display_copy, x=f'{x_col}_binned', y=y_col,
                               title=f'Box Plot: {y_col} by {x_col} (binned)')
                else:
                    fig = px.box(df_display, x=x_col, y=y_col,
                               title=f'Box Plot: {y_col} by {x_col}')
            elif plot_type == 'Densityplot':
                if len(df_display) < 10:
                    st.warning("⚠️ Not enough data points for a density plot (minimum 10 required).")
                    return
                fig = px.density_contour(df_display, x=x_col, y=y_col,
                                       title=f'Density Plot: {x_col} vs {y_col}')
            elif plot_type == 'Heatmap':
                corr = df_display[[x_col, y_col]].corr()
                fig = go.Figure(data=go.Heatmap(
                    z=corr.values,
                    x=corr.columns,
                    y=corr.columns,
                    colorscale='RdBu',
                    zmin=-1, zmax=1,
                    text=corr.values,
                    texttemplate='%{text:.3f}',
                    textfont={"size": 12}
                ))
                fig.update_layout(title=f'Correlation Heatmap: {x_col} and {y_col}')

            # Update layout for better appearance
            fig.update_layout(
                height=600,
                showlegend=True if color_param else False,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show correlation coefficient for numerical pairs
            if plot_type != 'Heatmap':
                correlation = df_display[[x_col, y_col]].corr().iloc[0, 1]
                st.metric("🔗 Correlation Coefficient", f"{correlation:.3f}")
                
                # Interpretation
                if abs(correlation) < 0.3:
                    interpretation = "Weak correlation"
                elif abs(correlation) < 0.7:
                    interpretation = "Moderate correlation"
                else:
                    interpretation = "Strong correlation"
                
                direction = "positive" if correlation > 0 else "negative"
                st.caption(f"📝 **Interpretation**: {interpretation} ({direction})")
            
        except Exception as e:
            st.error(f"❌ Error creating plot: {str(e)}")

    def categorical_vs_categorical(self):
        st.subheader("🏷️ Categorical vs Categorical Analysis")
        st.info("💡 Analyze relationships and distributions between two categorical variables.")
        
        if len(self.categorical_columns) < 2:
            st.warning("⚠️ Need at least 2 categorical columns for this analysis.")
            return
            
        # Column selection
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("📊 Select First Categorical Variable", self.categorical_columns, key='cat_x')
        with col2:
            remaining_cols = [col for col in self.categorical_columns if col != x_col]
            y_col = st.selectbox("📈 Select Second Categorical Variable", remaining_cols, key='cat_y')
        
        # Count unique values in each column
        unique_x = self.df[x_col].nunique()
        unique_y = self.df[y_col].nunique()
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            # Warn if too many categories
            if unique_x > 15 or unique_y > 15:
                st.warning(f"⚠️ High cardinality detected: {x_col} has {unique_x} and {y_col} has {unique_y} categories. " 
                          f"Consider limiting categories for better visualization.")
            
            max_categories = st.slider("📊 Max categories to display per variable", 
                                     5, 30, 
                                     min(15, max(unique_x, unique_y)),
                                     help="Reduce to focus on most frequent categories")
        
        plot_options = {
            'Countplot': 'Shows frequency distribution across categories',
            'Heatmap': 'Displays cross-tabulation as a color-coded matrix'
        }
        
        plot_type = st.selectbox("📊 Select Visualization Type", list(plot_options.keys()))
        st.markdown(f"**📝 About {plot_type}**: {plot_options[plot_type]}")

        st.markdown(f"### 🏷️ {x_col} vs {y_col}")
        
        # Get the most frequent categories for each column
        top_cats_x = self.df[x_col].value_counts().nlargest(max_categories).index
        top_cats_y = self.df[y_col].value_counts().nlargest(max_categories).index
        
        # Filter the dataframe to include only top categories
        df_filtered = self.df[self.df[x_col].isin(top_cats_x) & self.df[y_col].isin(top_cats_y)]
        
        if df_filtered.empty:
            st.error("❌ No data available after filtering categories.")
            return
            
        try:
            # Create crosstab with limited categories
            cross_tab = pd.crosstab(df_filtered[x_col], df_filtered[y_col])
            
            if plot_type == 'Countplot':
                # Create long format for grouped bar chart
                df_long = cross_tab.reset_index()
                df_long = df_long.melt(id_vars=x_col, var_name=y_col, value_name='Count')
                
                fig = px.bar(df_long, x=x_col, y='Count', color=y_col, 
                            title=f'Count Distribution: {y_col} by {x_col}',
                            text='Count')
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                
            elif plot_type == 'Heatmap':
                fig = px.imshow(cross_tab, 
                               text_auto=True, 
                               color_continuous_scale='Blues',
                               title=f'Cross-tabulation Heatmap: {x_col} vs {y_col}',
                               labels=dict(color="Count"))

            # Update layout
            fig.update_layout(
                height=600,
                template="plotly_white",
                xaxis_tickangle=-45 if len(top_cats_x) > 5 else 0
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total Combinations", f"{cross_tab.size}")
            with col2:
                st.metric("🔢 Non-zero Combinations", f"{(cross_tab > 0).sum().sum()}")
            with col3:
                st.metric("📈 Most Common Combination", f"{cross_tab.max().max()}")
            
            # Show cross-tabulation table
            with st.expander("📋 View Cross-tabulation Table"):
                st.dataframe(cross_tab)
            
        except Exception as e:
            st.error(f"❌ Error creating plot: {str(e)}")

    def numerical_vs_categorical(self):
        st.subheader("🔀 Numerical vs Categorical Analysis")
        st.info("💡 Compare numerical distributions across different categories.")
        
        if not self.numerical_columns or not self.categorical_columns:
            st.warning("⚠️ Need at least 1 numerical and 1 categorical column for this analysis.")
            return
            
        # Column selection
        col1, col2 = st.columns(2)
        with col1:
            num_col = st.selectbox("📊 Select Numerical Variable", self.numerical_columns, key='numcat_num')
        with col2:
            cat_col = st.selectbox("🏷️ Select Categorical Variable", self.categorical_columns, key='numcat_cat')
        
        # Count unique values in categorical column
        unique_cats = self.df[cat_col].nunique()
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            if unique_cats > 15:
                st.warning(f"⚠️ High cardinality detected: {cat_col} has {unique_cats} categories. " 
                          f"Consider limiting categories for better visualization.")
            
            max_categories = st.slider("📊 Max categories to display", 
                                     5, 30, 
                                     min(15, unique_cats),
                                     help="Focus on most frequent categories")
            
            show_outliers = st.checkbox("🎯 Show outliers", value=True, help="Display outlier points in box/violin plots")
        
        plot_options = {
            'Boxplot': 'Compare distributions and identify outliers across categories',
            'Violinplot': 'Show distribution shape and density across categories',
            'Barplot': 'Compare average values across categories'
        }
        
        plot_type = st.selectbox("📊 Select Visualization Type", list(plot_options.keys()))
        st.markdown(f"**📝 About {plot_type}**: {plot_options[plot_type]}")

        st.markdown(f"### 🔀 {num_col} by {cat_col}")
        
        # Get the most frequent categories
        top_cats = self.df[cat_col].value_counts().nlargest(max_categories).index
        
        # Filter the dataframe to include only top categories
        df_filtered = self.df[self.df[cat_col].isin(top_cats)]
        df_filtered = df_filtered.dropna(subset=[num_col, cat_col])
        
        if df_filtered.empty:
            st.error("❌ No valid data points after filtering categories and removing NaN values.")
            return
            
        try:
            if plot_type == 'Boxplot':
                fig = px.box(df_filtered, x=cat_col, y=num_col, 
                           title=f'Distribution of {num_col} by {cat_col}',
                           points="outliers" if show_outliers else False)
            elif plot_type == 'Violinplot':
                fig = px.violin(df_filtered, x=cat_col, y=num_col, 
                              box=True, 
                              points="outliers" if show_outliers else False,
                              title=f'Distribution of {num_col} by {cat_col}')
            elif plot_type == 'Barplot':
                grouped = df_filtered.groupby(cat_col)[num_col].agg(['mean', 'count']).reset_index()
                fig = px.bar(grouped, x=cat_col, y='mean', 
                           title=f'Average {num_col} by {cat_col}',
                           text='mean',
                           hover_data=['count'])
                fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

            # Update layout for better readability
            fig.update_layout(
                height=600,
                template="plotly_white",
                xaxis={'categoryorder': 'total descending'},
                xaxis_tickangle=-45 if len(top_cats) > 5 else 0
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show summary statistics
            summary_stats = df_filtered.groupby(cat_col)[num_col].agg(['count', 'mean', 'std', 'min', 'max']).round(2)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📊 Categories Analyzed", f"{len(summary_stats)}")
            with col2:
                st.metric("🔢 Total Data Points", f"{summary_stats['count'].sum()}")
            
            # Show detailed statistics
            with st.expander("📊 View Detailed Statistics by Category"):
                st.dataframe(summary_stats)
            
        except Exception as e:
            st.error(f"❌ Error creating plot: {str(e)}")

# Load data function for standalone execution
@st.cache_data
def load_data():
    """Load sample data for standalone execution"""
    try:
        return pd.read_csv('https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/refs/heads/master/laptop_cleaning.csv')
    except Exception as e:
        st.error(f"Error loading sample data: {str(e)}")
        return pd.DataFrame()

# Run app
if __name__ == "__main__":
    df = load_data()
    if not df.empty:
        app = BivariateAnalysis(df)
        app.column_vs_column_display()
    else:
        st.error("❌ Could not load sample data. Please check your internet connection.")