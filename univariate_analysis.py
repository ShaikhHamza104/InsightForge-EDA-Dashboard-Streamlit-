import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

class UnivariateAnalysis:

    def __init__(self, df):
        self.df = df
        self.selected_column = None
        self.selected_plot_type = None
        self.rows = 3

    def display(self):
        if self.df is None or self.df.empty:
            st.warning("No data available for analysis. Please upload a dataset first.")
            return
            
        st.title("📊 Univariate Analysis")
        st.write("This app performs univariate analysis on a selected column of the dataset.")
        
        column_type = st.selectbox('Select column type', ['Numeric', 'Categorical'])

        st.write("### Data Preview")
        if column_type == 'Numeric':
            numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            if numeric_cols:
                self.selected_column = st.selectbox("Select a numeric column", numeric_cols)
                st.write(self.df[self.selected_column].describe())
            else:
                st.warning("No numeric columns found in the dataset.")
                return
        else:
            cat_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
            if cat_cols:
                self.selected_column = st.selectbox("Select a categorical column", cat_cols)
                self.rows = st.number_input("Number of rows to display", min_value=1, max_value=min(len(self.df[self.selected_column].unique()), 20), value=5)
                st.write(self.df[self.selected_column].value_counts().head(self.rows))
            else:
                st.warning("No categorical columns found in the dataset.")
                return

        if self.selected_column:
            st.write("### Plot Preview")
            try:
                self.generate_plot(column_type)
            except Exception as e:
                st.error(f"Error generating plot: {str(e)}")

    def generate_plot(self, column_type):
        # Check for null values
        null_count = self.df[self.selected_column].isna().sum()
        if null_count > 0:
            st.warning(f"Warning: {null_count} null values found in this column. They will be excluded from the visualization.")
        
        # Create figure with appropriate size
        plt.figure(figsize=(10, 6))
        fig, ax = plt.subplots(figsize=(10, 6))

        if column_type == 'Numeric':
            self.selected_plot_type = st.selectbox(
                "Select plot type", ["Histogram", "Boxplot", "Lineplot", "Scatterplot", "Density"]
            )
            
            # Filter out null values
            valid_data = self.df[self.selected_column].dropna()
            
            if len(valid_data) == 0:
                st.error("No valid data points to plot after removing null values.")
                return
                
            if self.selected_plot_type == "Histogram":
                sns.histplot(valid_data, bins=min(30, len(valid_data.unique())), ax=ax)
            elif self.selected_plot_type == "Boxplot":
                sns.boxplot(x=valid_data, ax=ax)
            elif self.selected_plot_type == "Lineplot":
                sns.lineplot(y=valid_data, x=range(len(valid_data)), ax=ax)
            elif self.selected_plot_type == "Scatterplot":
                sns.scatterplot(x=range(len(valid_data)), y=valid_data, ax=ax)
            elif self.selected_plot_type == "Density":
                if len(valid_data.unique()) > 1:  # Need at least 2 unique values for density plot
                    sns.kdeplot(valid_data, ax=ax)
                else:
                    st.warning("Cannot create density plot: not enough unique values.")
                    return
        else:
            self.selected_plot_type = st.selectbox(
                "Select plot type", ["Countplot", "Pie chart", "Barplot"]
            )
            
            # Get value counts excluding NaNs
            data_counts = self.df[self.selected_column].value_counts().head(self.rows)
            
            if len(data_counts) == 0:
                st.error("No data to plot. The column might only contain null values.")
                return
                
            if self.selected_plot_type == "Countplot":
                # Use the pre-calculated counts for plotting
                sns.barplot(x=data_counts.index, y=data_counts.values, ax=ax)
                ax.set_xticklabels(data_counts.index)
            elif self.selected_plot_type == "Pie chart":
                plt.close(fig)  # Close the previous figure
                fig, ax = plt.subplots(figsize=(10, 10))
                ax.pie(data_counts.values, labels=data_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
            elif self.selected_plot_type == "Barplot":
                sns.barplot(x=data_counts.index, y=data_counts.values, ax=ax)

        # Set title and handle x-labels
        ax.set_title(f"{self.selected_plot_type} of {self.selected_column}")
        
        # Rotate labels only if there are more than a few categories
        if self.selected_plot_type not in ["Pie chart"]:
            if len(ax.get_xticklabels()) > 3:
                plt.xticks(rotation=45, ha='right')
            
        # Adjust layout
        plt.tight_layout()
        st.pyplot(fig)

# Run app
if __name__ == "__main__":
    try:
        df = pd.read_csv('https://raw.githubusercontent.com/ShaikhHamza104/LaptopInsight-Cleaning-EDA/refs/heads/master/laptop_cleaning.csv')
        univariate_analysis = UnivariateAnalysis(df)
        univariate_analysis.display()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")