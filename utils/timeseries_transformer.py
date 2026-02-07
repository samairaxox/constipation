"""
Time-Series Transformer
Converts Kaggle dataset into lifecycle format for AI agent consumption.
Groups by trend and generates engagement/sentiment/influencer curves.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class TimeSeriesTransformer:
    """
    Transforms dataset into time-series lifecycle format.
    """
    
    def __init__(self):
        self.name = "Time-Series Transformer"
    
    def transform_to_lifecycle(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Convert dataset into lifecycle format grouped by trend.
        
        Args:
            df (pd.DataFrame): Cleaned and featured dataset
        
        Returns:
            dict: Dictionary of trend_name -> time-series DataFrame
        """
        print(f"[{self.name}] Transforming to lifecycle format...")
        
        # Identify required columns
        trend_col = self._find_column(df, ['trend_name', 'trend', 'hashtag'])
        date_col = self._find_column(df, ['date', 'created_date', 'posted_date'])
        
        if not trend_col or not date_col:
            raise ValueError("Dataset must have trend identifier and date columns")
        
        # Ensure date column is datetime
        if df[date_col].dtype != 'datetime64[ns]':
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Group by trend
        trends = {}
        
        for trend_name, group in df.groupby(trend_col):
            # Sort by date
            group = group.sort_values(date_col)
            
            # Create lifecycle DataFrame
            lifecycle_df = self._create_lifecycle_dataframe(group, trend_name, date_col)
            
            trends[trend_name] = lifecycle_df
        
        print(f"  ✅ Transformed {len(trends)} trends")
        
        return trends
    
    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> Optional[str]:
        """
        Find column matching possible names.
        """
        for col in df.columns:
            if col.lower() in [name.lower() for name in possible_names]:
                return col
        return None
    
    def _create_lifecycle_dataframe(self, group: pd.DataFrame, trend_name: str, date_col: str) -> pd.DataFrame:
        """
        Create lifecycle DataFrame for a single trend.
        """
        # Aggregate by date
        daily = group.groupby(date_col).agg({
            'engagement_rate': 'mean',
            'sentiment_score': 'mean',
            'influencer_ratio': 'mean',
            'saturation_score': 'mean'
        }).reset_index()
        
        # Rename date column
        daily = daily.rename(columns={date_col: 'date'})
        
        # Add trend name
        daily['trend_name'] = trend_name
        
        # Generate additional time-series features
        daily = self._generate_engagement_trend(daily)
        daily = self._generate_sentiment_trend(daily)
        daily = self._generate_influencer_curve(daily)
        
        return daily
    
    def _generate_engagement_trend(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate engagement trend metrics.
        """
        df = df.copy()
        
        # Calculate rolling average
        df['engagement_7d_avg'] = df['engagement_rate'].rolling(window=7, min_periods=1).mean()
        
        # Calculate trend direction
        df['engagement_trend'] = df['engagement_rate'].pct_change()
        
        # Identify peak
        max_idx = df['engagement_rate'].idxmax()
        df['days_since_peak'] = 0
        
        if pd.notna(max_idx):
            peak_date = df.loc[max_idx, 'date']
            df['days_since_peak'] = (df['date'] - peak_date).dt.days
        
        return df
    
    def _generate_sentiment_trend(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate sentiment trend metrics.
        """
        df = df.copy()
        
        # Calculate sentiment change
        df['sentiment_change'] = df['sentiment_score'].diff()
        
        # Calculate sentiment volatility
        df['sentiment_volatility'] = df['sentiment_score'].rolling(window=7, min_periods=1).std()
        
        return df
    
    def _generate_influencer_curve(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate influencer participation curve.
        """
        df = df.copy()
        
        # Calculate influencer trend
        df['influencer_trend'] = df['influencer_ratio'].pct_change()
        
        # Identify influencer peak
        max_idx = df['influencer_ratio'].idxmax()
        df['influencer_peak_passed'] = False
        
        if pd.notna(max_idx):
            peak_idx_position = df.index.get_loc(max_idx)
            df.loc[df.index > max_idx, 'influencer_peak_passed'] = True
        
        return df
    
    def aggregate_to_agent_format(self, lifecycle_df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert lifecycle DataFrame to format expected by agents.
        
        Args:
            lifecycle_df (pd.DataFrame): Lifecycle time-series
        
        Returns:
            pd.DataFrame: Agent-compatible format
        """
        # Ensure required columns exist
        required_columns = [
            'date',
            'engagement_rate',
            'sentiment_score',
            'influencer_ratio',
            'saturation_score'
        ]
        
        agent_df = lifecycle_df.copy()
        
        # Add any missing required columns with defaults
        for col in required_columns:
            if col not in agent_df.columns:
                if col == 'date':
                    agent_df['date'] = pd.date_range(start='2026-01-01', periods=len(agent_df))
                else:
                    agent_df[col] = 0.5
        
        # Select and reorder columns
        agent_columns = required_columns + [
            col for col in agent_df.columns 
            if col not in required_columns and col != 'trend_name'
        ]
        
        agent_df = agent_df[agent_columns]
        
        return agent_df


# Test the transformer
if __name__ == "__main__":
    print("🧪 Testing Time-Series Transformer\n")
    
    # Create sample data
    dates = pd.date_range('2026-01-01', periods=30, freq='D')
    
    sample_data = pd.DataFrame({
        'trend_name': ['Dance Challenge'] * 30,
        'date': dates,
        'engagement_rate': np.concatenate([
            np.linspace(0.2, 0.8, 10),  # Growth
            np.linspace(0.8, 0.7, 5),   # Peak
            np.linspace(0.7, 0.3, 15)   # Decline
        ]),
        'sentiment_score': np.random.uniform(0.5, 0.9, 30),
        'influencer_ratio': np.concatenate([
            np.linspace(0.1, 0.3, 10),
            np.linspace(0.3, 0.25, 5),
            np.linspace(0.25, 0.1, 15)
        ]),
        'saturation_score': np.linspace(0, 90, 30)
    })
    
    transformer = TimeSeriesTransformer()
    
    # Transform to lifecycle
    trends = transformer.transform_to_lifecycle(sample_data)
    
    print(f"📊 Transformed Trends:")
    for trend_name, lifecycle_df in trends.items():
        print(f"\n  Trend: {trend_name}")
        print(f"  Days: {len(lifecycle_df)}")
        print(f"  Columns: {list(lifecycle_df.columns)}")
        
        # Convert to agent format
        agent_df = transformer.aggregate_to_agent_format(lifecycle_df)
        print(f"\n  Agent Format Preview:")
        print(agent_df.head())
    
    print("\n✅ Time-Series Transformer test complete!")
