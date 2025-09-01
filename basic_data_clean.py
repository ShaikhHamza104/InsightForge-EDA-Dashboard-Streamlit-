# Thin wrapper to preserve existing imports in main.py:
# from basic_data_clean import BasicDataClean
from components.cleaning import BasicDataClean

__all__ = ["BasicDataClean"]