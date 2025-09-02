import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any


class BasicDataClean:
    """A class for basic data cleaning operations with Streamlit interface."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with the original dataframe."""
        if df is None or df.empty:
            st.error("❌ Cannot initialize cleaner with empty or None dataframe")
            return
            
        self.original_df = df.copy()
        self.df = df.copy()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state for tracking cleaning operations."""
        if 'cleaning_operations' not in st.session_state:
            st.session_state.cleaning_operations = []
        if 'current_cleaned_df' not in st.session_state:
            st.session_state.current_cleaned_df = self.df.copy()
    
    def get_missing_value_summary(self) -> pd.DataFrame:
        """Get summary of missing values in the dataset."""
        try:
            missing_data = pd.DataFrame({
                'Column': self.df.columns,
                'Missing Count': self.df.isnull().sum(),
                'Missing Percentage': (self.df.isnull().sum() / len(self.df)) * 100,
                'Data Type': self.df.dtypes
            })
            missing_data = missing_data[missing_data['Missing Count'] > 0]
            return missing_data.sort_values('Missing Percentage', ascending=False)
        except Exception as e:
            st.error(f"❌ Error getting missing value summary: {e}")
            return pd.DataFrame()
    
    def handle_missing_values(self, strategy: str, column: str = None) -> pd.DataFrame:
        """Handle missing values using specified strategy."""
        try:
            df_copy = self.df.copy()
            
            if strategy == "Drop rows with any missing values":
                df_copy = df_copy.dropna()
                operation = "Dropped all rows with missing values"
                
            elif strategy == "Drop rows with all missing values":
                df_copy = df_copy.dropna(how='all')
                operation = "Dropped rows with all missing values"
                
            elif strategy == "Fill with mean (numeric only)":
                numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if df_copy[col].isnull().any():
                        df_copy[col] = df_copy[col].fillna(df_copy[col].mean())
                operation = f"Filled missing values with mean for numeric columns: {list(numeric_cols)}"
                
            elif strategy == "Fill with median (numeric only)":
                numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    if df_copy[col].isnull().any():
                        df_copy[col] = df_copy[col].fillna(df_copy[col].median())
                operation = f"Filled missing values with median for numeric columns: {list(numeric_cols)}"
                
            elif strategy == "Fill with mode (all columns)":
                for col in df_copy.columns:
                    if df_copy[col].isnull().any():
                        mode_val = df_copy[col].mode()
                        if not mode_val.empty:
                            df_copy[col] = df_copy[col].fillna(mode_val[0])
                operation = "Filled missing values with mode for all columns"
                
            elif strategy == "Forward fill":
                df_copy = df_copy.ffill()  # Updated method
                operation = "Applied forward fill for missing values"
                
            elif strategy == "Backward fill":
                df_copy = df_copy.bfill()  # Updated method
                operation = "Applied backward fill for missing values"
                
            elif strategy == "Fill with zero":
                df_copy = df_copy.fillna(0)
                operation = "Filled missing values with zero"
                
            elif strategy == "Fill with custom value" and column:
                custom_value = st.text_input(f"Enter custom value for {column}:", key=f"custom_{column}")
                if custom_value:
                    df_copy[column] = df_copy[column].fillna(custom_value)
                    operation = f"Filled missing values in {column} with '{custom_value}'"
            
            # Track the operation
            if 'operation' in locals():
                st.session_state.cleaning_operations.append(operation)
            return df_copy
            
        except Exception as e:
            st.error(f"❌ Error handling missing values: {e}")
            return self.df
    
    def drop_columns(self) -> None:
        """Interface for dropping selected columns."""
        st.subheader("🗑️ Drop Columns")
        
        if self.df.empty:
            st.warning("⚠️ No data available.")
            return
        
        try:
            # Show current columns
            st.write(f"**Current dataset has {len(self.df.columns)} columns:**")
            
            # Multi-select for columns to drop
            columns_to_drop = st.multiselect(
                "Select columns to drop:",
                options=list(self.df.columns),
                help="Select one or more columns to remove from the dataset",
                key="columns_to_drop_multiselect"
            )
            
            # Show preview of what will be dropped
            if columns_to_drop:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Columns to be dropped:**")
                    for col in columns_to_drop:
                        st.write(f"• {col} ({self.df[col].dtype})")
                
                with col2:
                    st.write("**Remaining columns:**")
                    remaining_cols = [col for col in self.df.columns if col not in columns_to_drop]
                    for col in remaining_cols:
                        st.write(f"• {col} ({self.df[col].dtype})")
                
                # Show impact
                st.info(f"📊 This will reduce the dataset from {len(self.df.columns)} to {len(self.df.columns) - len(columns_to_drop)} columns.")
                
                # Drop columns button
                if st.button("🗑️ Drop Selected Columns", type="primary"):
                    try:
                        self.df = self.df.drop(columns=columns_to_drop)
                        st.session_state.current_cleaned_df = self.df.copy()
                        
                        operation = f"Dropped columns: {', '.join(columns_to_drop)}"
                        st.session_state.cleaning_operations.append(operation)
                        
                        st.success(f"✅ Successfully dropped {len(columns_to_drop)} column(s)!")
                        st.success(f"📊 Dataset now has {len(self.df.columns)} columns and {len(self.df)} rows.")
                        
                        # Clear the multiselect
                        if "columns_to_drop_multiselect" in st.session_state:
                            del st.session_state["columns_to_drop_multiselect"]
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error dropping columns: {e}")
            
            # Show current dataset preview
            if not self.df.empty:
                with st.expander("📋 Current Dataset Preview", expanded=False):
                    st.dataframe(self.df.head(), use_container_width=True)
                    
        except Exception as e:
            st.error(f"❌ Error in drop columns interface: {e}")
    
    def drop_high_missing_columns(self, threshold: float = 0.5) -> None:
        """Interface for dropping columns with high missing value percentage."""
        st.subheader("📊 Handle High Missing Columns")
        
        if self.df.empty:
            st.warning("⚠️ No data available.")
            return
        
        try:
            # Calculate missing percentages
            missing_percentages = (self.df.isnull().sum() / len(self.df)) * 100
            high_missing_cols = missing_percentages[missing_percentages > threshold * 100].sort_values(ascending=False)
            
            if high_missing_cols.empty:
                st.success(f"✅ No columns have more than {threshold*100:.0f}% missing values!")
                return
            
            # Threshold selector
            threshold_percent = st.slider(
                "Missing value threshold (%):",
                min_value=10,
                max_value=90,
                value=int(threshold * 100),
                step=5,
                help="Columns with missing values above this threshold will be identified"
            )
            
            # Recalculate with new threshold
            high_missing_cols = missing_percentages[missing_percentages > threshold_percent].sort_values(ascending=False)
            
            if not high_missing_cols.empty:
                st.write(f"**Found {len(high_missing_cols)} column(s) with more than {threshold_percent}% missing values:**")
                
                # Display high missing columns
                for col, missing_pct in high_missing_cols.items():
                    st.write(f"• **{col}**: {missing_pct:.1f}% missing ({int(self.df[col].isnull().sum())} out of {len(self.df)} rows)")
                
                # Select columns to drop
                cols_to_drop = st.multiselect(
                    "Select columns to drop:",
                    options=high_missing_cols.index.tolist(),
                    default=high_missing_cols.index.tolist(),
                    help="These columns have high missing value percentages",
                    key="high_missing_cols_to_drop"
                )
                
                if cols_to_drop:
                    st.warning(f"⚠️ This will permanently remove {len(cols_to_drop)} column(s) from your dataset.")
                    
                    if st.button("🗑️ Drop High Missing Columns", type="primary"):
                        try:
                            self.df = self.df.drop(columns=cols_to_drop)
                            st.session_state.current_cleaned_df = self.df.copy()
                            
                            operation = f"Dropped high missing columns (>{threshold_percent}%): {', '.join(cols_to_drop)}"
                            st.session_state.cleaning_operations.append(operation)
                            
                            st.success(f"✅ Successfully dropped {len(cols_to_drop)} column(s) with high missing values!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error dropping columns: {e}")
            else:
                st.success(f"✅ No columns have more than {threshold_percent}% missing values!")
                
        except Exception as e:
            st.error(f"❌ Error in high missing columns interface: {e}")
    
    def display_cleaning_interface(self) -> pd.DataFrame:
        """Display the main cleaning interface for missing values."""
        st.subheader("🧹 Missing Value Treatment")
        
        if self.df.empty:
            st.warning("⚠️ No data available for cleaning.")
            return self.df
        
        try:
            # Show missing value summary
            missing_summary = self.get_missing_value_summary()
            
            if missing_summary.empty:
                st.success("✅ No missing values found in the dataset!")
                return self.df
            
            st.write("**Missing Value Summary:**")
            st.dataframe(missing_summary, use_container_width=True)
            
            # Cleaning strategy selection
            strategy_options = [
                "Drop rows with any missing values",
                "Drop rows with all missing values",
                "Fill with mean (numeric only)",
                "Fill with median (numeric only)",
                "Fill with mode (all columns)",
                "Forward fill",
                "Backward fill",
                "Fill with zero"
            ]
            
            strategy = st.selectbox(
                "Select cleaning strategy:",
                options=strategy_options,
                help="Choose how to handle missing values in your dataset"
            )
            
            # Apply cleaning
            if st.button("🧹 Apply Cleaning Strategy", type="primary"):
                try:
                    self.df = self.handle_missing_values(strategy)
                    st.session_state.current_cleaned_df = self.df.copy()
                    
                    st.success(f"✅ Applied strategy: {strategy}")
                    
                    # Show results
                    new_missing = self.df.isnull().sum().sum()
                    st.info(f"📊 Missing values after cleaning: {new_missing}")
                    
                    if new_missing == 0:
                        st.success("🎉 All missing values have been handled!")
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error applying cleaning strategy: {e}")
            
            # Show cleaning operations history
            if st.session_state.cleaning_operations:
                with st.expander("📝 Cleaning Operations History"):
                    for i, operation in enumerate(st.session_state.cleaning_operations, 1):
                        st.write(f"{i}. {operation}")
            
            # Reset button
            if st.button("🔄 Reset to Original Data"):
                self.df = self.original_df.copy()
                st.session_state.current_cleaned_df = self.df.copy()
                st.session_state.cleaning_operations = []
                st.success("✅ Reset to original data!")
                st.rerun()
            
            return self.df
            
        except Exception as e:
            st.error(f"❌ Error in cleaning interface: {e}")
            return self.df
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Get the current cleaned dataframe."""
        return self.df.copy()
    
    def export_cleaned_data(self) -> None:
        """Export the cleaned data."""
        try:
            if not self.df.empty:
                csv = self.df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Cleaned Data (CSV)",
                    data=csv,
                    file_name="cleaned_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ No data available to export.")
        except Exception as e:
            st.error(f"❌ Error exporting data: {e}")