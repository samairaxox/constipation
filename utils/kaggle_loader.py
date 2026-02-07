"""
Kaggle Dataset Loader
Loads and preprocesses real social media trend data from Kaggle.
Dataset: atharvasoundankar/viral-social-media-trends-and-engagement-analysis
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple

try:
    import kagglehub
    KAGGLEHUB_AVAILABLE = True
except ImportError:
    KAGGLEHUB_AVAILABLE = False
    print("⚠️  kagglehub not installed. Install with: pip install kagglehub")


class KaggleDatasetLoader:
    """
    Loads and manages Kaggle social media trend dataset.
    """
    
    def __init__(self):
        self.name = "Kaggle Dataset Loader"
        self.dataset_name = "atharvasoundankar/viral-social-media-trends-and-engagement-analysis"
        self.data_path = None
        self.raw_data = None
        self.cleaned_data = None
        
    def load_dataset(self, force_download: bool = False) -> pd.DataFrame:
        """
        Load Kaggle dataset using kagglehub.
        
        Args:
            force_download (bool): Force re-download of dataset
        
        Returns:
            pd.DataFrame: Raw dataset
        """
        print(f"[{self.name}] Loading Kaggle dataset...")
        
        if not KAGGLEHUB_AVAILABLE:
            raise ImportError("kagglehub is required. Install with: pip install kagglehub")
        
        try:
            # Download dataset
            print(f"  Downloading: {self.dataset_name}")
            self.data_path = kagglehub.dataset_download(self.dataset_name)
            
            print(f"  ✅ Dataset path: {self.data_path}")
            
            # Detect CSV files
            csv_files = self._detect_csv_files(self.data_path)
            
            if not csv_files:
                raise FileNotFoundError("No CSV files found in dataset")
            
            print(f"  Found {len(csv_files)} CSV file(s)")
            
            # Load primary CSV
            primary_csv = csv_files[0]
            print(f"  Loading: {primary_csv}")
            
            self.raw_data = pd.read_csv(primary_csv)
            
            print(f"  ✅ Loaded {len(self.raw_data)} rows, {len(self.raw_data.columns)} columns")
            
            return self.raw_data
            
        except Exception as e:
            print(f"  ❌ Error loading dataset: {e}")
            raise
    
    def _detect_csv_files(self, path: str) -> List[str]:
        """
        Detect CSV files in dataset directory.
        
        Args:
            path (str): Dataset directory path
        
        Returns:
            list: List of CSV file paths
        """
        csv_files = []
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))
        
        return csv_files
    
    def preview_dataset(self, n: int = 5) -> Dict:
        """
        Preview dataset structure and content.
        
        Args:
            n (int): Number of rows to preview
        
        Returns:
            dict: Dataset preview information
        """
        if self.raw_data is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")
        
        preview = {
            "shape": self.raw_data.shape,
            "columns": list(self.raw_data.columns),
            "dtypes": self.raw_data.dtypes.to_dict(),
            "head": self.raw_data.head(n).to_dict('records'),
            "missing_values": self.raw_data.isnull().sum().to_dict(),
            "memory_usage": self.raw_data.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        return preview
    
    def display_schema(self):
        """
        Display dataset schema in readable format.
        """
        if self.raw_data is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")
        
        print(f"\n{'='*70}")
        print("DATASET SCHEMA")
        print('='*70)
        print(f"\nShape: {self.raw_data.shape[0]} rows × {self.raw_data.shape[1]} columns")
        print(f"\nColumns:")
        
        for col in self.raw_data.columns:
            dtype = self.raw_data[col].dtype
            null_count = self.raw_data[col].isnull().sum()
            null_pct = (null_count / len(self.raw_data) * 100)
            
            print(f"  • {col:30s} {str(dtype):15s} (null: {null_pct:5.1f}%)")
        
        print(f"\nMemory Usage: {self.raw_data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print('='*70)


# Test the loader
if __name__ == "__main__":
    print("🧪 Testing Kaggle Dataset Loader\n")
    
    if not KAGGLEHUB_AVAILABLE:
        print("❌ kagglehub not installed")
        print("Install with: pip install kagglehub")
    else:
        try:
            loader = KaggleDatasetLoader()
            
            # Load dataset
            data = loader.load_dataset()
            
            # Display schema
            loader.display_schema()
            
            # Preview
            preview = loader.preview_dataset(n=3)
            
            print(f"\n📊 Preview (first 3 rows):")
            print(pd.DataFrame(preview['head']))
            
            print("\n✅ Kaggle Dataset Loader test complete!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
