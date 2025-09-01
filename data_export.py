import io
import base64
from datetime import datetime
import pandas as pd 
class DataExporter:
    def __init__(self, df):
        self.df = df
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def to_csv(self, index=False, separator=','):
        """Export to CSV format"""
        return self.df.to_csv(index=index, sep=separator)
    
    def to_tsv(self, index=False):
        """Export to TSV format"""
        return self.df.to_csv(index=index, sep='\t')
    
    def to_json(self, orient='records', indent=2):
        """Export to JSON format"""
        return self.df.to_json(orient=orient, indent=indent)
    
    def to_excel(self):
        """Export to Excel format"""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            self.df.to_excel(writer, index=False, sheet_name='Cleaned_Data')
        return output.getvalue()
