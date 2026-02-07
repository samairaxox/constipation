"""
Influencer Agent
Identifies and analyzes key influencers driving trend momentum.
Detects influencer disengagement and participation changes.
"""

import numpy as np
import pandas as pd


class InfluencerAgent:
    def __init__(self):
        self.name = "Influencer Agent"
        self.description = "Identifies key influencers and their impact on trends"
    
    def analyze(self, data):
        """
        Analyzes influencer impact on trend propagation.
        
        Args:
            data (pd.DataFrame or dict): Influencer data or time-series trend data
        
        Returns:
            dict: Influencer impact analysis
        """
        print(f"[{self.name}] Analyzing influencer impact...")
        
        # Handle different input types
        if isinstance(data, pd.DataFrame):
            return self._analyze_timeseries(data)
        elif isinstance(data, dict):
            return self._analyze_snapshot(data)
        else:
            raise ValueError("Data must be a pandas DataFrame or dictionary")
    
    def _analyze_timeseries(self, df):
        """
        Analyze time-series influencer participation data.
        
        Args:
            df (pd.DataFrame): Time-series data with influencer_ratio column
        
        Returns:
            dict: Comprehensive influencer analysis
        """
        if 'influencer_ratio' not in df.columns:
            raise ValueError("DataFrame must contain 'influencer_ratio' column")
        
        influencer_ratios = df['influencer_ratio'].values
        
        # Calculate key metrics
        initial_ratio = np.mean(influencer_ratios[:7])  # First week
        current_ratio = np.mean(influencer_ratios[-7:])  # Last week
        peak_ratio = np.max(influencer_ratios)
        overall_avg = np.mean(influencer_ratios)
        
        # Calculate participation drop
        if initial_ratio > 0:
            participation_drop_percent = ((initial_ratio - current_ratio) / initial_ratio) * 100
        else:
            participation_drop_percent = 0
        
        # Detect disengagement pattern
        disengagement_status = self._detect_disengagement(influencer_ratios)
        
        # Calculate trend
        trend_direction = self._calculate_trend(influencer_ratios)
        
        # Assign influence impact score (0-100)
        influence_impact_score = self._calculate_impact_score(
            current_ratio, 
            participation_drop_percent,
            trend_direction
        )
        
        # Assign risk level
        risk_level = self._assign_risk_level(
            participation_drop_percent,
            disengagement_status,
            current_ratio
        )
        
        return {
            "agent": self.name,
            "status": "success",
            "participation_drop_percent": round(participation_drop_percent, 2),
            "influence_impact_score": round(influence_impact_score, 2),
            "disengagement_status": disengagement_status,
            "risk_level": risk_level,
            "metrics": {
                "initial_ratio": round(initial_ratio, 4),
                "current_ratio": round(current_ratio, 4),
                "peak_ratio": round(peak_ratio, 4),
                "overall_average": round(overall_avg, 4)
            },
            "trend_direction": trend_direction,
            "influencer_activity": self._categorize_activity(current_ratio),
            "insights": self._generate_insights(
                disengagement_status,
                participation_drop_percent,
                risk_level,
                current_ratio
            )
        }
    
    def _analyze_snapshot(self, data):
        """
        Analyze single snapshot of influencer data.
        
        Args:
            data (dict): Dictionary containing influencer information
        
        Returns:
            dict: Influencer snapshot analysis
        """
        top_influencers = data.get("influencers", [])
        total_reach = data.get("total_reach", 0)
        
        return {
            "agent": self.name,
            "status": "success",
            "top_influencers": top_influencers,
            "influencer_count": len(top_influencers),
            "total_reach": total_reach,
            "insights": "Snapshot analysis. Time-series data recommended for trend detection."
        }
    
    def _detect_disengagement(self, influencer_ratios):
        """
        Detect influencer disengagement pattern.
        
        Args:
            influencer_ratios (np.array): Array of influencer ratios over time
        
        Returns:
            str: Disengagement status
        """
        length = len(influencer_ratios)
        
        # Divide into thirds
        third = length // 3
        early_avg = np.mean(influencer_ratios[:third])
        mid_avg = np.mean(influencer_ratios[third:2*third])
        late_avg = np.mean(influencer_ratios[2*third:])
        
        # Calculate decline across phases
        early_to_mid = ((early_avg - mid_avg) / early_avg * 100) if early_avg > 0 else 0
        mid_to_late = ((mid_avg - late_avg) / mid_avg * 100) if mid_avg > 0 else 0
        
        if early_to_mid > 30 and mid_to_late > 30:
            return "Severe Disengagement"
        elif early_to_mid > 20 or mid_to_late > 20:
            return "Moderate Disengagement"
        elif early_to_mid > 10 or mid_to_late > 10:
            return "Slight Disengagement"
        elif early_to_mid < -10 or mid_to_late < -10:
            return "Increasing Engagement"
        else:
            return "Stable Engagement"
    
    def _calculate_trend(self, ratios, window=10):
        """
        Calculate influencer participation trend.
        
        Args:
            ratios (np.array): Influencer ratios over time
            window (int): Window for trend calculation
        
        Returns:
            str: Trend direction
        """
        if len(ratios) < window:
            window = len(ratios)
        
        recent = ratios[-window:]
        
        # Linear regression to detect trend
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        
        if slope > 0.001:
            return "increasing"
        elif slope < -0.001:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_impact_score(self, current_ratio, drop_percent, trend):
        """
        Calculate influence impact score (0-100).
        Higher score = stronger influencer presence.
        
        Args:
            current_ratio (float): Current influencer participation ratio
            drop_percent (float): Participation drop percentage
            trend (str): Trend direction
        
        Returns:
            float: Impact score 0-100
        """
        # Base score from current ratio (0-1 mapped to 0-50)
        base_score = current_ratio * 500  # Max 50 points
        
        # Penalty for drop
        drop_penalty = min(drop_percent * 0.5, 30)  # Max 30 point penalty
        
        # Bonus/penalty for trend
        trend_modifier = 0
        if trend == "increasing":
            trend_modifier = 20
        elif trend == "decreasing":
            trend_modifier = -20
        
        final_score = base_score - drop_penalty + trend_modifier
        
        return max(0, min(100, final_score))  # Clamp to 0-100
    
    def _assign_risk_level(self, drop_percent, disengagement, current_ratio):
        """
        Assign risk level based on influencer metrics.
        
        Args:
            drop_percent (float): Participation drop percentage
            disengagement (str): Disengagement status
            current_ratio (float): Current influencer ratio
        
        Returns:
            str: Risk level
        """
        # Critical risk conditions
        if "Severe" in disengagement or drop_percent > 60:
            return "Critical"
        
        # High risk
        if "Moderate" in disengagement or drop_percent > 40:
            return "High"
        
        # Medium risk
        if drop_percent > 20 or current_ratio < 0.05:
            return "Medium"
        
        # Low risk
        return "Low"
    
    def _categorize_activity(self, ratio):
        """
        Categorize influencer activity level based on ratio.
        
        Args:
            ratio (float): Current influencer ratio
        
        Returns:
            str: Activity level
        """
        if ratio >= 0.20:
            return "Very High"
        elif ratio >= 0.15:
            return "High"
        elif ratio >= 0.10:
            return "Moderate"
        elif ratio >= 0.05:
            return "Low"
        else:
            return "Very Low"
    
    def _generate_insights(self, disengagement, drop_percent, risk_level, current_ratio):
        """
        Generate actionable insights.
        """
        activity = self._categorize_activity(current_ratio)
        
        if risk_level == "Critical":
            return f"🚨 CRITICAL: {disengagement} detected with {drop_percent:.1f}% drop. Influencer exodus underway. Urgent re-engagement needed."
        
        elif risk_level == "High":
            return f"⚠️ HIGH RISK: {disengagement}. Participation dropped {drop_percent:.1f}%. Major influencers leaving the trend."
        
        elif risk_level == "Medium":
            return f"⚡ MEDIUM RISK: {drop_percent:.1f}% drop in influencer participation. Activity level: {activity}. Monitor key influencers."
        
        else:  # Low
            if "Increasing" in disengagement:
                return f"✅ POSITIVE: Influencer engagement is increasing. Current activity: {activity}. Trend gaining momentum."
            else:
                return f"✅ STABLE: Influencer participation is healthy at {activity} level. Continue current strategy."
    
    def _identify_top_influencers(self, data):
        """
        Internal method to identify top influencers (placeholder).
        In production, integrate with social media APIs.
        """
        # Placeholder
        return [
            {"name": "Influencer_A", "followers": 250000, "impact_score": 8.5},
            {"name": "Influencer_B", "followers": 180000, "impact_score": 7.2},
            {"name": "Influencer_C", "followers": 150000, "impact_score": 6.8}
        ]


# Test the agent
if __name__ == "__main__":
    print("🧪 Testing Influencer Agent\n")
    
    # Test 1: Time-series with influencer decline
    print("Test 1: Time-series influencer analysis")
    
    # Create sample influencer participation decline
    sample_data = pd.DataFrame({
        'date': pd.date_range('2026-01-01', periods=45, freq='D'),
        'influencer_ratio': np.concatenate([
            np.random.normal(0.25, 0.02, 15),  # High participation
            np.random.normal(0.15, 0.03, 15),  # Declining
            np.random.normal(0.08, 0.02, 15)   # Low participation
        ])
    })
    
    agent = InfluencerAgent()
    result = agent.analyze(sample_data)
    
    print(f"✅ Status: {result['status']}")
    print(f"📉 Participation Drop: {result['participation_drop_percent']}%")
    print(f"📊 Impact Score: {result['influence_impact_score']}")
    print(f"🔍 Disengagement: {result['disengagement_status']}")
    print(f"⚠️  Risk Level: {result['risk_level']}")
    print(f"📈 Trend: {result['trend_direction']}")
    print(f"🎯 Activity: {result['influencer_activity']}")
    print(f"💡 Insights: {result['insights']}\n")
    
    # Test 2: Snapshot analysis
    print("Test 2: Snapshot analysis")
    snapshot = {
        "influencers": [
            {"name": "Influencer_A", "reach": 100000},
            {"name": "Influencer_B", "reach": 75000}
        ],
        "total_reach": 175000
    }
    
    result2 = agent.analyze(snapshot)
    print(f"✅ Status: {result2['status']}")
    print(f"👥 Influencer Count: {result2['influencer_count']}")
    print(f"📡 Total Reach: {result2['total_reach']}")
    
    print("\n✅ Influencer Agent tests complete!")
