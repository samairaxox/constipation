"""
Synthetic Social Media Trend Data Generator

Generates realistic time-series trend lifecycle data for testing and simulation.
Simulates growth, peak, and decline phases of social media trends.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json


class TrendDataGenerator:
    def __init__(self, seed=42):
        """
        Initialize the trend data generator.
        
        Args:
            seed (int): Random seed for reproducibility
        """
        np.random.seed(seed)
        self.phases = {
            'growth': {'days': 25, 'weight': 1.5},
            'peak': {'days': 20, 'weight': 1.0},
            'decline': {'days': 35, 'weight': 0.5}
        }
    
    def _generate_growth_phase(self, days):
        """Generate exponential growth phase data."""
        base = np.linspace(0, 1, days)
        curve = np.power(base, 0.5)  # Square root for smooth acceleration
        noise = np.random.normal(0, 0.05, days)
        return np.clip(curve + noise, 0, 1)
    
    def _generate_peak_phase(self, days):
        """Generate stable peak phase with minor fluctuations."""
        base = np.ones(days) * 0.95
        noise = np.random.normal(0, 0.08, days)
        return np.clip(base + noise, 0.7, 1.0)
    
    def _generate_decline_phase(self, days):
        """Generate decline phase with exponential decay."""
        base = np.linspace(1, 0, days)
        curve = np.power(base, 1.5)  # Accelerating decline
        noise = np.random.normal(0, 0.06, days)
        return np.clip(curve + noise, 0, 1)
    
    def _calculate_engagement_rate(self, lifecycle_position, base_rate=0.045):
        """
        Calculate engagement rate based on lifecycle position.
        
        Args:
            lifecycle_position (float): 0-1 normalized position in lifecycle
            base_rate (float): Base engagement rate
        """
        # Peak engagement during growth and peak phases
        engagement_multiplier = 1 + (lifecycle_position * 1.5)
        noise = np.random.normal(1, 0.15)
        return base_rate * engagement_multiplier * noise
    
    def _calculate_sentiment(self, lifecycle_position):
        """
        Calculate sentiment score based on trend phase.
        Early adopters are enthusiastic, late phase shows fatigue.
        """
        base_sentiment = 0.7 - (lifecycle_position * 0.3)  # Decline over time
        noise = np.random.normal(0, 0.1)
        return np.clip(base_sentiment + noise, 0, 1)
    
    def _calculate_influencer_ratio(self, lifecycle_position):
        """
        Calculate ratio of influencer posts to total posts.
        Higher in early/peak phases, drops during decline.
        """
        if lifecycle_position < 0.3:  # Growth phase
            base = 0.25
        elif lifecycle_position < 0.6:  # Peak phase
            base = 0.18
        else:  # Decline phase
            base = 0.08
        
        noise = np.random.normal(0, 0.03)
        return np.clip(base + noise, 0, 0.5)
    
    def _calculate_saturation(self, lifecycle_position):
        """
        Calculate market saturation score (0-100).
        Increases throughout lifecycle.
        """
        base = lifecycle_position * 100
        noise = np.random.normal(0, 5)
        return np.clip(base + noise, 0, 100)
    
    def _calculate_algorithm_boost(self, lifecycle_position):
        """
        Simulate platform algorithm boost.
        Boosts new trends, reduces boost as trend ages.
        """
        if lifecycle_position < 0.2:
            base = 1.8  # Strong boost for new trends
        elif lifecycle_position < 0.5:
            base = 1.3  # Moderate boost during peak
        else:
            base = 0.7  # Reduced visibility during decline
        
        noise = np.random.normal(0, 0.15)
        return np.clip(base + noise, 0.5, 2.0)
    
    def generate_trend_data(self, trend_name, start_date=None, total_days=None):
        """
        Generate complete trend lifecycle data.
        
        Args:
            trend_name (str): Name of the trend
            start_date (str or datetime): Start date (default: 90 days ago)
            total_days (int): Total days to generate (default: random 60-90)
        
        Returns:
            pandas.DataFrame: Complete trend dataset
        """
        # Set defaults
        if total_days is None:
            total_days = np.random.randint(60, 91)
        
        if start_date is None:
            start_date = datetime.now() - timedelta(days=total_days)
        elif isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        
        # Calculate phase distribution
        growth_days = int(total_days * 0.30)  # 30% growth
        peak_days = int(total_days * 0.25)    # 25% peak
        decline_days = total_days - growth_days - peak_days  # ~45% decline
        
        # Generate lifecycle curves
        growth_curve = self._generate_growth_phase(growth_days)
        peak_curve = self._generate_peak_phase(peak_days)
        decline_curve = self._generate_decline_phase(decline_days)
        
        lifecycle_curve = np.concatenate([growth_curve, peak_curve, decline_curve])
        
        # Generate dataset
        data = []
        
        for day_idx in range(total_days):
            current_date = start_date + timedelta(days=day_idx)
            lifecycle_pos = day_idx / total_days
            intensity = lifecycle_curve[day_idx]
            
            # Calculate metrics based on lifecycle position
            post_count = int(intensity * np.random.randint(800, 2500))
            engagement_rate = self._calculate_engagement_rate(intensity)
            sentiment_score = self._calculate_sentiment(lifecycle_pos)
            influencer_ratio = self._calculate_influencer_ratio(lifecycle_pos)
            saturation_score = self._calculate_saturation(lifecycle_pos)
            algorithm_boost = self._calculate_algorithm_boost(lifecycle_pos)
            
            data.append({
                'trend_name': trend_name,
                'date': current_date.strftime('%Y-%m-%d'),
                'post_count': post_count,
                'engagement_rate': round(engagement_rate, 4),
                'sentiment_score': round(sentiment_score, 4),
                'influencer_ratio': round(influencer_ratio, 4),
                'saturation_score': round(saturation_score, 2),
                'algorithm_boost': round(algorithm_boost, 2)
            })
        
        df = pd.DataFrame(data)
        return df
    
    def export_to_json(self, df, filename=None):
        """
        Export DataFrame to JSON format.
        
        Args:
            df (pandas.DataFrame): Trend data
            filename (str): Optional filename to save
        
        Returns:
            str: JSON string
        """
        json_data = df.to_dict(orient='records')
        json_string = json.dumps(json_data, indent=2)
        
        if filename:
            with open(filename, 'w') as f:
                f.write(json_string)
            print(f"✅ Data saved to {filename}")
        
        return json_string
    
    def generate_multiple_trends(self, trend_names, start_date=None):
        """
        Generate data for multiple trends.
        
        Args:
            trend_names (list): List of trend names
            start_date (str or datetime): Start date for all trends
        
        Returns:
            pandas.DataFrame: Combined dataset
        """
        all_data = []
        
        for trend in trend_names:
            df = self.generate_trend_data(trend, start_date)
            all_data.append(df)
        
        combined_df = pd.concat(all_data, ignore_index=True)
        return combined_df


# Main function for easy usage
def generate_trend_data(trend_name, start_date=None, total_days=None, export_json=False):
    """
    Convenience function to generate trend data.
    
    Args:
        trend_name (str): Name of the trend
        start_date (str or datetime): Start date
        total_days (int): Total days to generate
        export_json (bool): Whether to export to JSON file
    
    Returns:
        pandas.DataFrame: Generated trend data
    """
    generator = TrendDataGenerator()
    df = generator.generate_trend_data(trend_name, start_date, total_days)
    
    if export_json:
        filename = f"{trend_name.replace(' ', '_').lower()}_trend_data.json"
        generator.export_to_json(df, filename)
    
    print(f"✅ Generated {len(df)} days of data for trend: '{trend_name}'")
    print(f"📊 Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"📈 Peak post count: {df['post_count'].max()}")
    print(f"💬 Avg engagement rate: {df['engagement_rate'].mean():.4f}")
    
    return df


# Example usage and testing
if __name__ == "__main__":
    print("🚀 Trend Data Generator\n")
    
    # Generate single trend
    trend_df = generate_trend_data("Viral Dance Challenge", total_days=75)
    
    print("\n📋 Sample Data (first 5 rows):")
    print(trend_df.head())
    
    print("\n📋 Sample Data (last 5 rows):")
    print(trend_df.tail())
    
    print("\n📊 Dataset Statistics:")
    print(trend_df.describe())
    
    # Export to JSON
    generator = TrendDataGenerator()
    json_output = generator.export_to_json(trend_df, "sample_trend_data.json")
    
    print("\n✅ Data generation complete!")
