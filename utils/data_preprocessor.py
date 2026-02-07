"""
Data Preprocessing Module
Cleans and prepares Kaggle dataset for AI agent consumption.
Handles missing values, normalization, and feature engineering.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from sklearn.preprocessing import MinMaxScaler


class DataPreprocessor:
    """
    Preprocesses social media trend data for AI analysis.
    """
    
    def __init__(self):
        self.name = "Data Preprocessor"
        self.scalers = {}
    
    def clean_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform comprehensive data cleaning.
        
        Args:
            df (pd.DataFrame): Raw dataset
        
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        print(f"[{self.name}] Cleaning dataset...")
        
        cleaned = df.copy()
        
        # Remove duplicates
        initial_rows = len(cleaned)
        cleaned = cleaned.drop_duplicates()
        duplicates_removed = initial_rows - len(cleaned)
        print(f"  • Removed {duplicates_removed} duplicate rows")
        
        # Handle missing values
        cleaned = self._handle_missing_values(cleaned)
        
        # Standardize column names
        cleaned = self._standardize_columns(cleaned)
        
        # Standardize platform names
        if 'platform' in cleaned.columns:
            cleaned = self._standardize_platforms(cleaned)
        
        # Convert date columns
        cleaned = self._convert_dates(cleaned)
        
        # Clean influencer fields
        cleaned = self._clean_influencer_fields(cleaned)
        
        # Normalize engagement metrics
        cleaned = self._normalize_metrics(cleaned)
        
        print(f"  ✅ Cleaning complete: {len(cleaned)} rows")
        
        return cleaned
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values with appropriate strategies.
        """
        print(f"  • Handling missing values...")
        
        df = df.copy()
        
        # Numeric columns: fill with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
        
        # Categorical columns: fill with mode or 'unknown'
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                if df[col].mode().empty:
                    df[col].fillna('unknown', inplace=True)
                else:
                    df[col].fillna(df[col].mode()[0], inplace=True)
        
        return df
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names to lowercase with underscores.
        """
        df = df.copy()
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
        return df
    
    def _standardize_platforms(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize platform names.
        """
        df = df.copy()
        
        platform_mapping = {
            'tiktok': 'TikTok',
            'instagram': 'Instagram',
            'twitter': 'Twitter',
            'x': 'Twitter',
            'youtube': 'YouTube',
            'facebook': 'Facebook',
            'snapchat': 'Snapchat'
        }
        
        if 'platform' in df.columns:
            df['platform'] = df['platform'].str.lower().map(
                lambda x: platform_mapping.get(x, x.title() if isinstance(x, str) else x)
            )
        
        return df
    
    def _convert_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert date columns to datetime format.
        """
        df = df.copy()
        
        date_columns = ['date', 'created_date', 'posted_date', 'trend_date', 'timestamp']
        
        for col in df.columns:
            if any(date_col in col.lower() for date_col in date_columns):
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
        
        return df
    
    def _clean_influencer_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean influencer-related fields.
        """
        df = df.copy()
        
        influencer_cols = [col for col in df.columns if 'influencer' in col.lower()]
        
        for col in influencer_cols:
            if df[col].dtype == 'object':
                # Remove special characters
                df[col] = df[col].str.replace(r'[^\w\s]', '', regex=True)
                # Strip whitespace
                df[col] = df[col].str.strip()
        
        return df
    
    def _normalize_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize engagement metrics to 0-1 scale.
        """
        print(f"  • Normalizing metrics...")
        
        df = df.copy()
        
        # Identify metric columns
        metric_cols = [col for col in df.columns if any(
            metric in col.lower() for metric in ['engagement', 'likes', 'shares', 'views', 'comments']
        )]
        
        for col in metric_cols:
            if df[col].dtype in [np.float64, np.int64]:
                scaler = MinMaxScaler()
                df[f'{col}_normalized'] = scaler.fit_transform(df[[col]])
                self.scalers[col] = scaler
        
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create AI-compatible features.
        
        Args:
            df (pd.DataFrame): Cleaned dataset
        
        Returns:
            pd.DataFrame: Dataset with engineered features
        """
        print(f"[{self.name}] Engineering features...")
        
        df = df.copy()
        
        # Engagement rate
        df = self._create_engagement_rate(df)
        
        # Influencer ratio
        df = self._create_influencer_ratio(df)
        
        # Sentiment score
        df = self._create_sentiment_score(df)
        
        # Saturation score
        df = self._create_saturation_score(df)
        
        # Virality decay rate
        df = self._create_virality_decay(df)
        
        print(f"  ✅ Feature engineering complete")
        
        return df
    
    def _create_engagement_rate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate engagement rate.
        Formula: (likes + comments + shares) / views
        """
        df = df.copy()
        
        # Try to find relevant columns
        engagement_cols = {
            'likes': None,
            'comments': None,
            'shares': None,
            'views': None
        }
        
        for col in df.columns:
            col_lower = col.lower()
            if 'like' in col_lower:
                engagement_cols['likes'] = col
            elif 'comment' in col_lower:
                engagement_cols['comments'] = col
            elif 'share' in col_lower:
                engagement_cols['shares'] = col
            elif 'view' in col_lower or 'reach' in col_lower:
                engagement_cols['views'] = col
        
        # Calculate engagement rate if columns exist
        if all(engagement_cols.values()):
            df['engagement_rate'] = (
                df[engagement_cols['likes']] + 
                df[engagement_cols['comments']] + 
                df[engagement_cols['shares']]
            ) / (df[engagement_cols['views']] + 1)  # +1 to avoid division by zero
            
            # Normalize to 0-1
            df['engagement_rate'] = df['engagement_rate'].clip(0, 1)
        else:
            # Fallback: use normalized engagement if available
            engagement_normalized = [col for col in df.columns if 'engagement' in col.lower() and 'normalized' in col.lower()]
            if engagement_normalized:
                df['engagement_rate'] = df[engagement_normalized[0]]
            else:
                df['engagement_rate'] = 0.5  # Default neutral value
        
        return df
    
    def _create_influencer_ratio(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate influencer participation ratio.
        """
        df = df.copy()
        
        # Try to find influencer columns
        influencer_col = None
        for col in df.columns:
            if 'influencer' in col.lower() and 'count' in col.lower():
                influencer_col = col
                break
        
        if influencer_col:
            # Normalize to 0-1 scale
            max_val = df[influencer_col].max()
            if max_val > 0:
                df['influencer_ratio'] = df[influencer_col] / max_val
            else:
                df['influencer_ratio'] = 0.1
        else:
            # Default value
            df['influencer_ratio'] = 0.15
        
        return df
    
    def _create_sentiment_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate sentiment score (0-1 scale).
        """
        df = df.copy()
        
        # Try to find sentiment column
        sentiment_col = None
        for col in df.columns:
            if 'sentiment' in col.lower():
                sentiment_col = col
                break
        
        if sentiment_col:
            # If sentiment is numeric, normalize it
            if df[sentiment_col].dtype in [np.float64, np.int64]:
                min_val = df[sentiment_col].min()
                max_val = df[sentiment_col].max()
                if max_val > min_val:
                    df['sentiment_score'] = (df[sentiment_col] - min_val) / (max_val - min_val)
                else:
                    df['sentiment_score'] = 0.5
            # If categorical (positive/neutral/negative)
            elif df[sentiment_col].dtype == 'object':
                sentiment_map = {
                    'positive': 0.8,
                    'neutral': 0.5,
                    'negative': 0.2
                }
                df['sentiment_score'] = df[sentiment_col].str.lower().map(sentiment_map).fillna(0.5)
        else:
            # Default neutral sentiment
            df['sentiment_score'] = 0.6
        
        return df
    
    def _create_saturation_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate market saturation score (0-100).
        """
        df = df.copy()
        
        # If we have a date column, calculate based on trend age
        date_col = None
        for col in df.columns:
            if 'date' in col.lower() and df[col].dtype == 'datetime64[ns]':
                date_col = col
                break
        
        if date_col:
            # Group by trend and calculate days since start
            if 'trend_name' in df.columns or 'trend' in df.columns:
                trend_col = 'trend_name' if 'trend_name' in df.columns else 'trend'
                
                df['days_since_start'] = df.groupby(trend_col)[date_col].transform(
                    lambda x: (x - x.min()).dt.days
                )
                
                # Normalize to 0-100 scale (assume 90 days = 100% saturation)
                df['saturation_score'] = (df['days_since_start'] / 90 * 100).clip(0, 100)
            else:
                df['saturation_score'] = 50.0
        else:
            df['saturation_score'] = 45.0
        
        return df
    
    def _create_virality_decay(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate virality decay rate.
        """
        df = df.copy()
        
        # If we have engagement over time, calculate decay
        if 'engagement_rate' in df.columns and 'trend_name' in df.columns:
            df['virality_decay_rate'] = df.groupby('trend_name')['engagement_rate'].pct_change()
            df['virality_decay_rate'] = df['virality_decay_rate'].fillna(0)
        else:
            df['virality_decay_rate'] = 0.0
        
        return df


# Test the preprocessor
if __name__ == "__main__":
    print("🧪 Testing Data Preprocessor\n")
    
    # Create sample data
    sample_data = pd.DataFrame({
        'Trend Name': ['Dance Challenge', 'Fashion Trend', 'Dance Challenge'],
        'Platform': ['tiktok', 'Instagram', 'tiktok'],
        'Date': ['2026-01-01', '2026-01-02', '2026-01-03'],
        'Likes': [1000, 2000, 1500],
        'Comments': [100, 200, 150],
        'Shares': [50, 100, 75],
        'Views': [10000, 20000, 15000],
        'Influencer Count': [5, 10, 7]
    })
    
    preprocessor = DataPreprocessor()
    
    # Clean
    cleaned = preprocessor.clean_dataset(sample_data)
    
    # Engineer features
    featured = preprocessor.engineer_features(cleaned)
    
    print("\n📊 Engineered Features:")
    print(featured[['trend_name', 'engagement_rate', 'influencer_ratio', 'sentiment_score', 'saturation_score']].head())
    
    print("\n✅ Data Preprocessor test complete!")
