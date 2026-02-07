"""
Engagement Agent
Analyzes engagement metrics (likes, comments, shares, views) for trend analysis.
Detects engagement decline and decay speed to assess trend health.
"""

import numpy as np
import pandas as pd


class EngagementAgent:
    def __init__(self):
        self.name = "Engagement Agent"
        self.description = "Analyzes engagement metrics and patterns"
    
    def analyze(self, data):
        """
        Analyzes engagement metrics from social media or platform data.
        
        Args:
            data (dict or pd.DataFrame): Contains engagement metrics or time-series data
        
        Returns:
            dict: Structured analysis of engagement patterns
        """
        print(f"[{self.name}] Analyzing engagement data...")
        
        # Handle different input types
        if isinstance(data, pd.DataFrame):
            return self._analyze_timeseries(data)
        elif isinstance(data, dict):
            return self._analyze_single_snapshot(data)
        else:
            raise ValueError("Data must be a pandas DataFrame or dictionary")
    
    def _analyze_timeseries(self, df):
        """
        Analyze time-series trend data.
        
        Args:
            df (pd.DataFrame): Time-series data with engagement_rate column
        
        Returns:
            dict: Comprehensive engagement analysis
        """
        if 'engagement_rate' not in df.columns:
            raise ValueError("DataFrame must contain 'engagement_rate' column")
        
        # Calculate key metrics
        engagement_rates = df['engagement_rate'].values
        
        # Peak and current engagement
        peak_engagement = np.max(engagement_rates)
        current_engagement = engagement_rates[-1]  # Most recent
        
        # Calculate decline percentage
        if peak_engagement > 0:
            decline_percent = ((peak_engagement - current_engagement) / peak_engagement) * 100
        else:
            decline_percent = 0
        
        # Detect decay speed (rate of decline over recent period)
        decay_speed = self._calculate_decay_speed(engagement_rates)
        
        # Assign risk level
        risk_level = self._assign_risk_level(decline_percent, decay_speed)
        
        # Calculate additional metrics
        avg_engagement = np.mean(engagement_rates)
        trend_direction = self._detect_trend_direction(engagement_rates)
        
        # Volatility measure
        volatility = np.std(engagement_rates)
        
        return {
            "agent": self.name,
            "status": "success",
            "engagement_decline_percent": round(decline_percent, 2),
            "risk_level": risk_level,
            "metrics": {
                "peak_engagement": round(peak_engagement, 4),
                "current_engagement": round(current_engagement, 4),
                "average_engagement": round(avg_engagement, 4),
                "volatility": round(volatility, 4)
            },
            "decay_speed": decay_speed,
            "trend_direction": trend_direction,
            "insights": self._generate_insights(decline_percent, decay_speed, risk_level)
        }
    
    def _analyze_single_snapshot(self, data):
        """
        Analyze single snapshot of engagement data.
        
        Args:
            data (dict): Contains engagement metrics like likes, comments, shares, views
        
        Returns:
            dict: Engagement analysis
        """
        # Extract metrics
        likes = data.get("likes", 0)
        comments = data.get("comments", 0)
        shares = data.get("shares", 0)
        views = data.get("views", 1)  # Avoid division by zero
        
        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(data)
        
        # Estimate trend based on ratios
        engagement_rate = (likes + comments * 2 + shares * 3) / views
        
        return {
            "agent": self.name,
            "status": "success",
            "engagement_score": round(engagement_score, 2),
            "engagement_rate": round(engagement_rate, 4),
            "metrics": {
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "views": views
            },
            "insights": "Single snapshot analyzed. Time-series data recommended for decline detection."
        }
    
    def _calculate_decay_speed(self, engagement_rates, window=7):
        """
        Calculate the speed of engagement decay.
        
        Args:
            engagement_rates (np.array): Array of engagement rates over time
            window (int): Number of recent days to consider
        
        Returns:
            str: Decay speed category (slow, moderate, rapid)
        """
        if len(engagement_rates) < window:
            window = len(engagement_rates)
        
        # Compare recent average vs previous average
        recent_avg = np.mean(engagement_rates[-window:])
        previous_avg = np.mean(engagement_rates[:-window]) if len(engagement_rates) > window else recent_avg
        
        if previous_avg > 0:
            decay_rate = ((previous_avg - recent_avg) / previous_avg) * 100
        else:
            decay_rate = 0
        
        # Categorize decay speed
        if decay_rate < 10:
            return "slow"
        elif decay_rate < 30:
            return "moderate"
        else:
            return "rapid"
    
    def _detect_trend_direction(self, engagement_rates, window=10):
        """
        Detect the overall trend direction.
        
        Args:
            engagement_rates (np.array): Engagement rates over time
            window (int): Window for trend calculation
        
        Returns:
            str: Trend direction (increasing, stable, decreasing)
        """
        if len(engagement_rates) < window:
            window = len(engagement_rates)
        
        recent = engagement_rates[-window:]
        
        # Calculate linear regression slope
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        
        if slope > 0.0005:
            return "increasing"
        elif slope < -0.0005:
            return "decreasing"
        else:
            return "stable"
    
    def _assign_risk_level(self, decline_percent, decay_speed):
        """
        Assign risk level based on decline and decay speed.
        
        Args:
            decline_percent (float): Percentage decline from peak
            decay_speed (str): Speed of decay (slow, moderate, rapid)
        
        Returns:
            str: Risk level (Low, Medium, High)
        """
        # Risk matrix
        if decline_percent < 20:
            if decay_speed == "slow":
                return "Low"
            elif decay_speed == "moderate":
                return "Low"
            else:  # rapid
                return "Medium"
        
        elif decline_percent < 50:
            if decay_speed == "slow":
                return "Low"
            elif decay_speed == "moderate":
                return "Medium"
            else:  # rapid
                return "High"
        
        else:  # decline_percent >= 50
            if decay_speed == "slow":
                return "Medium"
            elif decay_speed == "moderate":
                return "High"
            else:  # rapid
                return "High"
    
    def _generate_insights(self, decline_percent, decay_speed, risk_level):
        """
        Generate human-readable insights.
        """
        if risk_level == "Low":
            return f"Engagement is healthy with {decline_percent:.1f}% decline and {decay_speed} decay. Trend is stable."
        elif risk_level == "Medium":
            return f"Moderate risk detected. Engagement declined {decline_percent:.1f}% with {decay_speed} decay. Monitor closely."
        else:  # High
            return f"High risk! Engagement dropped {decline_percent:.1f}% with {decay_speed} decay. Immediate action recommended."
    
    def _calculate_engagement_score(self, data):
        """
        Internal method to calculate engagement score from raw metrics.
        """
        likes = data.get("likes", 0)
        comments = data.get("comments", 0)
        shares = data.get("shares", 0)
        views = data.get("views", 1)
        
        # Weighted engagement score
        weighted_sum = (likes * 1) + (comments * 2) + (shares * 3)
        score = (weighted_sum / views) * 100
        
        return min(score, 100)  # Cap at 100


# Test the agent
if __name__ == "__main__":
    print("🧪 Testing Engagement Agent\n")
    
    # Test 1: Time-series data (simulated decline)
    print("Test 1: Time-series analysis")
    
    # Create sample declining engagement data
    sample_data = pd.DataFrame({
        'date': pd.date_range('2026-01-01', periods=30, freq='D'),
        'engagement_rate': np.concatenate([
            np.linspace(0.08, 0.12, 10),  # Growth
            np.linspace(0.12, 0.10, 10),  # Plateau
            np.linspace(0.10, 0.04, 10)   # Decline
        ])
    })
    
    agent = EngagementAgent()
    result = agent.analyze(sample_data)
    
    print(f"✅ Status: {result['status']}")
    print(f"📉 Engagement Decline: {result['engagement_decline_percent']}%")
    print(f"⚠️  Risk Level: {result['risk_level']}")
    print(f"🏃 Decay Speed: {result['decay_speed']}")
    print(f"📊 Trend Direction: {result['trend_direction']}")
    print(f"💡 Insights: {result['insights']}\n")
    
    # Test 2: Single snapshot
    print("Test 2: Single snapshot analysis")
    snapshot = {
        "likes": 1000,
        "comments": 200,
        "shares": 150,
        "views": 5000
    }
    
    result2 = agent.analyze(snapshot)
    print(f"✅ Status: {result2['status']}")
    print(f"📊 Engagement Score: {result2['engagement_score']}")
    print(f"💬 Engagement Rate: {result2['engagement_rate']}")
    
    print("\n✅ Engagement Agent tests complete!")
