import pandas as pd
import numpy as np
import streamlit as st
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder

# Try to import fancyimpute
try:
    from fancyimpute import KNN as FancyKNN
    FANCYIMPUTE_AVAILABLE = True
except ImportError:
    FANCYIMPUTE_AVAILABLE = False

class BasicDataClean:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()  # Work with a copy to avoid modifying original

    def drop_high_missing_columns(self):
        """Drop columns that have more than 50% missing values based on user selection."""
        missing_percentages = (self.df.isnull().sum() / self.df.shape[0]) * 100
        high_missing_cols = missing_percentages[missing_percentages > 50].index.tolist()

        if len(high_missing_cols) > 0:
            st.write(f"Columns with >50% missing values: {high_missing_cols}")
            user_choice = st.selectbox('What would you like to do?', options=['Keep as is', 'Drop columns'])
            if user_choice == 'Drop columns':
                self.df = self.df.drop(columns=high_missing_cols)
                st.success(f"Dropped {len(high_missing_cols)} columns with high missing values")
    def drop_columns(self):
                    """Drop columns based on user selection."""
                    all_columns = self.df.columns.tolist()

                    if len(all_columns) == 0:
                        st.warning("No columns available to drop.")
                        return

                    # Allow multiple column selection
                    columns_to_drop = st.multiselect(
                        'Which columns do you want to drop?',
                        options=all_columns,
                        default=[]
                    )

                    if columns_to_drop:
                        if st.button('Drop Selected Columns', key='drop_cols_btn'):
                            self.df = self.df.drop(columns=columns_to_drop)
                            st.success(f"Successfully dropped {len(columns_to_drop)} columns: {', '.join(columns_to_drop)}")
                    else:
                        st.info("No columns selected for dropping.")
    def display_cleaning_interface(self):
        st.title('🧹 Basic Data Cleaning')
        
        if self.df is None or self.df.empty:
            st.warning("⚠️ No data available for cleaning. Please upload a dataset first.")
            return None
            
        # Display initial data info
        st.subheader('📊 Dataset Overview')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", self.df.shape[0])
        with col2:
            st.metric("Columns", self.df.shape[1])
        with col3:
            st.metric("Missing Values", self.df.isnull().sum().sum())
            
        st.header('🔍 Missing Data Overview')
        missing_summary = self.df.isnull().sum()
        missing_df = pd.DataFrame({
            'Column': missing_summary.index,
            'Missing Count': missing_summary.values,
            'Missing Percentage': (missing_summary.values / len(self.df) * 100).round(2)
        })
        
        # Only show columns with missing values
        missing_cols_df = missing_df[missing_df['Missing Count'] > 0]
        
        if len(missing_cols_df) == 0:
            st.success("✅ No missing values found in the dataset!")
            return self.df
        
        st.dataframe(missing_cols_df, use_container_width=True)
        
        # Create tabs for different cleaning approaches
        tab1, tab2 = st.tabs(["🔢 Numeric Columns", "📝 Categorical Columns"])
        
        with tab1:
            self._clean_numeric_columns()
        
        with tab2:
            self._clean_categorical_columns()
        
        # Show results
        st.header('📋 Cleaning Results')
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Before Cleaning')
            st.write(f"Missing values: {missing_df['Missing Count'].sum()}")
            
        with col2:
            st.subheader('After Cleaning')
            current_missing = self.df.isnull().sum().sum()
            st.write(f"Missing values: {current_missing}")
            
        # Show cleaned data preview
        st.subheader('🔍 Data Preview After Cleaning')
        st.write(f"Shape: {self.df.shape}")
        st.dataframe(self.df.head(), use_container_width=True)
        
        # Final status
        final_missing = self.df.isnull().sum().sum()
        if final_missing == 0:
            st.success("✅ All missing values have been handled!")
        else:
            st.warning(f"⚠️ {final_missing} missing values remain")
            
        return self.df
    
    def _clean_numeric_columns(self):
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            st.info("ℹ️ No numeric columns found in the dataset.")
            return
            
        missing_numeric = self.df[numeric_cols].isnull().sum()
        numeric_with_missing = missing_numeric[missing_numeric > 0]
        
        if len(numeric_with_missing) == 0:
            st.info("ℹ️ No missing values in numeric columns.")
            return
            
        st.write(f"**Numeric columns with missing values:** {len(numeric_with_missing)}")
        
        # Display missing values info
        for col, missing_count in numeric_with_missing.items():
            st.write(f"• {col}: {missing_count} missing values ({missing_count/len(self.df)*100:.1f}%)")
        
        missing_method = st.selectbox(
            "Choose method for filling missing values in numeric columns:",
            options=['mean', 'median', 'mode', 'custom value', 'knn imputation'],
            key='numeric_missing_method'
        )

        if st.button("Apply Numeric Imputation", key="apply_numeric"):
            if missing_method == 'mean':
                self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
                st.success("✅ Missing values filled with column means")
                
            elif missing_method == 'median':
                self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
                st.success("✅ Missing values filled with column medians")
                
            elif missing_method == 'mode':
                for col in numeric_cols:
                    if self.df[col].isnull().sum() > 0:
                        mode_val = self.df[col].mode()
                        if len(mode_val) > 0:
                            self.df[col] = self.df[col].fillna(mode_val.iloc[0])
                st.success("✅ Missing values filled with column modes")
                
            elif missing_method == 'custom value':
                custom_val = st.number_input('Enter custom number:', value=0.0, key="custom_numeric")
                self.df[numeric_cols] = self.df[numeric_cols].fillna(custom_val)
                st.success(f"✅ Missing values filled with {custom_val}")
                
            elif missing_method == 'knn imputation':
                try:
                    with st.spinner("Performing KNN imputation..."):
                        n_neighbors = min(5, len(self.df.dropna()) - 1)
                        if n_neighbors > 0:
                            imputer = KNNImputer(n_neighbors=n_neighbors)
                            self.df[numeric_cols] = imputer.fit_transform(self.df[numeric_cols])
                            st.success("✅ Missing values filled using KNN imputation")
                        else:
                            st.error("❌ Not enough data for KNN imputation")
                except Exception as e:
                    st.error(f"❌ Error during KNN imputation: {str(e)}")

    def _clean_categorical_columns(self):
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_cols) == 0:
            st.info("ℹ️ No categorical columns found in the dataset.")
            return
            
        missing_categorical = self.df[categorical_cols].isnull().sum()
        categorical_with_missing = missing_categorical[missing_categorical > 0]
        
        if len(categorical_with_missing) == 0:
            st.info("ℹ️ No missing values in categorical columns.")
            return

        st.write(f"**Categorical columns with missing values:** {len(categorical_with_missing)}")
        
        # Display missing values info
        for col, missing_count in categorical_with_missing.items():
            st.write(f"• {col}: {missing_count} missing values ({missing_count/len(self.df)*100:.1f}%)")
        
        # Imputation method selection
        imputation_options = ['mode', 'unknown', 'custom value']
        
        if FANCYIMPUTE_AVAILABLE:
            imputation_options.append('fancyimpute KNN')
            st.info("✅ fancyimpute is available for advanced categorical imputation")
        else:
            st.warning("⚠️ fancyimpute not available. Install with: `pip install fancyimpute`")

        missing_method = st.selectbox(
            "Choose method for filling missing values in categorical columns:",
            options=imputation_options,
            key='categorical_missing_method'
        )

        # Additional parameters based on method
        if missing_method == 'custom value':
            custom_val = st.text_input('Enter custom text:', value='Missing', key="custom_categorical")
        elif missing_method == 'fancyimpute KNN' and FANCYIMPUTE_AVAILABLE:
            k_neighbors = st.slider('Number of neighbors for KNN:', min_value=1, max_value=10, value=3, key="knn_neighbors")

        if st.button("Apply Categorical Imputation", key="apply_categorical"):
            if missing_method == 'mode':
                self._apply_mode_imputation(categorical_cols)
            elif missing_method == 'unknown':
                self.df[categorical_cols] = self.df[categorical_cols].fillna('Unknown')
                st.success("✅ Missing values filled with 'Unknown'")
            elif missing_method == 'custom value':
                self.df[categorical_cols] = self.df[categorical_cols].fillna(custom_val)
                st.success(f"✅ Missing values filled with '{custom_val}'")
            elif missing_method == 'fancyimpute KNN' and FANCYIMPUTE_AVAILABLE:
                self._apply_fancyimpute_categorical(categorical_cols, k_neighbors)

    def _apply_mode_imputation(self, categorical_cols):
        """Apply mode imputation to categorical columns"""
        imputed_cols = []
        for col in categorical_cols:
            if self.df[col].isnull().sum() > 0:
                mode_val = self.df[col].mode()
                if len(mode_val) > 0:
                    self.df[col] = self.df[col].fillna(mode_val.iloc[0])
                    imputed_cols.append(col)
        
        if imputed_cols:
            st.success(f"✅ Missing values filled with mode for columns: {', '.join(imputed_cols)}")
        else:
            st.info("ℹ️ No categorical columns needed mode imputation")

    def _apply_fancyimpute_categorical(self, categorical_cols, k_neighbors=3):
        """Apply fancyimpute KNN to categorical columns using label encoding"""
        try:
            with st.spinner("Performing fancyimpute KNN imputation on categorical data..."):
                # Filter to only columns with missing values
                cols_to_impute = [col for col in categorical_cols if self.df[col].isnull().sum() > 0]
                
                if not cols_to_impute:
                    st.info("ℹ️ No categorical columns need imputation")
                    return

                # Store original data for potential restoration
                original_data = self.df[cols_to_impute].copy()
                
                # Check if we have enough non-null samples
                min_samples_needed = k_neighbors + 1
                non_null_rows = self.df[cols_to_impute].dropna().shape[0]
                
                if non_null_rows < min_samples_needed:
                    st.warning(f"⚠️ Not enough complete rows ({non_null_rows}) for KNN with k={k_neighbors}. Using mode imputation instead.")
                    self._apply_mode_imputation(categorical_cols)
                    return

                # Dictionary to store label encoders
                label_encoders = {}
                encoded_data = pd.DataFrame(index=self.df.index)

                # Label encode each categorical column
                for col in cols_to_impute:
                    # Get non-null values for fitting
                    non_null_values = self.df[col].dropna().unique()
                    
                    if len(non_null_values) > 0:
                        le = LabelEncoder()
                        le.fit(non_null_values)
                        label_encoders[col] = le

                        # Transform the entire column
                        encoded_col = pd.Series(index=self.df.index, dtype=float)
                        mask = ~self.df[col].isnull()
                        
                        if mask.sum() > 0:
                            encoded_col.loc[mask] = le.transform(self.df[col].loc[mask])
                        
                        encoded_data[col] = encoded_col
                    else:
                        # If no non-null values, skip this column
                        st.warning(f"⚠️ Column {col} has no non-null values to learn from")
                        continue

                if len(label_encoders) == 0:
                    st.error("❌ No columns could be encoded for imputation")
                    return

                # Apply fancyimpute KNN
                k_neighbors = min(k_neighbors, non_null_rows - 1)
                imputer = FancyKNN(k=k_neighbors)

                # Perform imputation
                imputed_encoded = imputer.fit_transform(encoded_data.values)
                
                # Create DataFrame with imputed values
                imputed_df = pd.DataFrame(
                    imputed_encoded,
                    columns=encoded_data.columns,
                    index=encoded_data.index
                )

                # Decode back to original categorical values
                successfully_imputed = []
                for col in cols_to_impute:
                    if col in label_encoders:
                        try:
                            # Round to nearest integer and clip to valid range
                            rounded_values = np.round(imputed_df[col]).astype(int)
                            min_label = 0
                            max_label = len(label_encoders[col].classes_) - 1
                            clipped_values = np.clip(rounded_values, min_label, max_label)

                            # Inverse transform
                            self.df[col] = label_encoders[col].inverse_transform(clipped_values)
                            successfully_imputed.append(col)
                            
                        except Exception as col_error:
                            st.warning(f"⚠️ Error imputing column {col}: {str(col_error)}. Using mode instead.")
                            # Fallback to mode for this column
                            mode_val = original_data[col].mode()
                            if len(mode_val) > 0:
                                self.df[col] = original_data[col].fillna(mode_val.iloc[0])

                if successfully_imputed:
                    st.success(f"✅ FancyImpute KNN applied to columns: {', '.join(successfully_imputed)}")
                else:
                    st.error("❌ FancyImpute failed for all columns. Using mode imputation as fallback.")
                    self._apply_mode_imputation(categorical_cols)

        except Exception as e:
            st.error(f"❌ Error during fancyimpute KNN imputation: {str(e)}")
            st.info("ℹ️ Falling back to mode imputation...")
            
            # Restore original data and use mode imputation as fallback
            for col in cols_to_impute:
                if col in original_data.columns:
                    self.df[col] = original_data[col]
            
            self._apply_mode_imputation(categorical_cols)

# Example usage for standalone testing
if __name__ == "__main__":
    # Create sample data with missing values for testing
    sample_data = pd.DataFrame({
        'numeric1': [1, 2, np.nan, 4, 5],
        'numeric2': [10, np.nan, 30, 40, 50],
        'category1': ['A', 'B', None, 'A', 'C'],
        'category2': ['X', 'Y', 'Z', None, 'X']
    })
    
    cleaner = BasicDataClean(sample_data)
    cleaned_df = cleaner.display_cleaning_interface()
