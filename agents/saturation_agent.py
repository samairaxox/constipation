"""
Saturation Agent
Detects market or trend saturation levels using growth curves and velocity.
Analyzes content fatigue and repetition risk.
"""

import numpy as np
import pandas as pd


class SaturationAgent:
    def __init__(self):
        self.name = "Saturation Agent"
        self.description = "Detects trend saturation and market penetration"
        
        # Saturation thresholds
        self.FATIGUE_THRESHOLD = 70.0  # Content fatigue kicks in
        self.CRITICAL_THRESHOLD = 85.0  # Critical saturation
        self.SAFE_THRESHOLD = 50.0     # Safe zone
    
    def analyze(self, data):
        """
        Analyzes saturation levels based on growth metrics.
        
        Args:
            data (pd.DataFrame or dict): Time-series growth data or snapshot
        
        Returns:
            dict: Saturation analysis with penetration metrics
        """
        print(f"[{self.name}] Calculating saturation levels...")
        
        # Handle different input types
        if isinstance(data, pd.DataFrame):
            return self._analyze_timeseries(data)
        elif isinstance(data, dict):
            return self._analyze_snapshot(data)
        else:
            raise ValueError("Data must be a pandas DataFrame or dictionary")
    
    def _analyze_timeseries(self, df):
        """
        Analyze time-series saturation data.
        
        Args:
            df (pd.DataFrame): Time-series data with saturation_score column
        
        Returns:
            dict: Comprehensive saturation analysis
        """
        if 'saturation_score' not in df.columns:
            raise ValueError("DataFrame must contain 'saturation_score' column")
        
        saturation_scores = df['saturation_score'].values
        
        # Current saturation metrics
        current_saturation = saturation_scores[-1]
        peak_saturation = np.max(saturation_scores)
        avg_saturation = np.mean(saturation_scores)
        initial_saturation = saturation_scores[0]
        
        # Calculate saturation velocity (rate of increase)
        saturation_velocity = self._calculate_velocity(saturation_scores)
        
        # Detect threshold breaches
        threshold_breaches = self._detect_threshold_breaches(saturation_scores)
        
        # Measure repetition risk
        repetition_risk = self._measure_repetition_risk(
            current_saturation,
            saturation_velocity
        )
        
        # Calculate market penetration percentage
        market_penetration = current_saturation  # Already 0-100
        
        # Detect saturation stage
        saturation_stage = self._detect_saturation_stage(current_saturation)
        
        # Assign impact level
        saturation_impact_level = self._assign_impact_level(
            current_saturation,
            saturation_velocity,
            threshold_breaches
        )
        
        # Time to peak estimation
        time_to_peak = self._estimate_time_to_peak(
            saturation_scores,
            saturation_velocity
        )
        
        return {
            "agent": self.name,
            "status": "success",
            "saturation_score": round(current_saturation, 2),
            "saturation_impact_level": saturation_impact_level,
            "market_penetration": round(market_penetration, 2),
            "repetition_risk": repetition_risk,
            "metrics": {
                "current_saturation": round(current_saturation, 2),
                "peak_saturation": round(peak_saturation, 2),
                "average_saturation": round(avg_saturation, 2),
                "initial_saturation": round(initial_saturation, 2),
                "saturation_velocity": round(saturation_velocity, 4)
            },
            "saturation_stage": saturation_stage,
            "threshold_breaches": threshold_breaches,
            "time_to_peak": time_to_peak,
            "fatigue_detected": current_saturation >= self.FATIGUE_THRESHOLD,
            "insights": self._generate_insights(
                current_saturation,
                saturation_stage,
                saturation_impact_level,
                repetition_risk,
                threshold_breaches
            )
        }
    
    def _analyze_snapshot(self, data):
        """
        Analyze single snapshot of saturation data.
        
        Args:
            data (dict): Saturation snapshot data
        
        Returns:
            dict: Snapshot analysis
        """
        saturation_level = data.get("saturation_level", "unknown")
        penetration = data.get("penetration", 0)
        
        return {
            "agent": self.name,
            "status": "success",
            "saturation_level": saturation_level,
            "market_penetration": penetration,
            "insights": "Snapshot analysis. Time-series data recommended for velocity tracking."
        }
    
    def _calculate_velocity(self, scores, window=7):
        """
        Calculate saturation velocity (rate of saturation increase).
        
        Args:
            scores (np.array): Saturation scores over time
            window (int): Window for velocity calculation
        
        Returns:
            float: Velocity (points per day)
        """
        if len(scores) < window:
            window = len(scores)
        
        recent = scores[-window:]
        
        # Linear regression slope
        x = np.arange(len(recent))
        velocity = np.polyfit(x, recent, 1)[0]
        
        return velocity
    
    def _detect_threshold_breaches(self, scores):
        """
        Detect when saturation crosses critical thresholds.
        
        Args:
            scores (np.array): Saturation scores over time
        
        Returns:
            list: List of threshold breaches
        """
        breaches = []
        
        # Check if fatigue threshold was breached
        if np.any(scores >= self.FATIGUE_THRESHOLD):
            first_breach_idx = np.where(scores >= self.FATIGUE_THRESHOLD)[0][0]
            breaches.append({
                "threshold": "Content Fatigue",
                "value": self.FATIGUE_THRESHOLD,
                "day": int(first_breach_idx + 1)
            })
        
        # Check if critical threshold was breached
        if np.any(scores >= self.CRITICAL_THRESHOLD):
            first_breach_idx = np.where(scores >= self.CRITICAL_THRESHOLD)[0][0]
            breaches.append({
                "threshold": "Critical Saturation",
                "value": self.CRITICAL_THRESHOLD,
                "day": int(first_breach_idx + 1)
            })
        
        return breaches
    
    def _measure_repetition_risk(self, current_saturation, velocity):
        """
        Measure content repetition risk.
        
        Args:
            current_saturation (float): Current saturation score
            velocity (float): Rate of saturation increase
        
        Returns:
            str: Risk level (Low, Moderate, High, Extreme)
        """
        # High saturation + fast velocity = extreme risk
        if current_saturation >= 85 and velocity > 1.5:
            return "Extreme"
        
        if current_saturation >= 70:
            if velocity > 1.0:
                return "High"
            else:
                return "Moderate"
        
        if current_saturation >= 50:
            return "Moderate"
        
        return "Low"
    
    def _detect_saturation_stage(self, score):
        """
        Detect current saturation stage.
        
        Args:
            score (float): Current saturation score
        
        Returns:
            str: Saturation stage
        """
        if score >= 90:
            return "Peak Saturation"
        elif score >= 70:
            return "High Saturation"
        elif score >= 50:
            return "Moderate Saturation"
        elif score >= 30:
            return "Growing Market"
        else:
            return "Early Stage"
    
    def _assign_impact_level(self, saturation, velocity, breaches):
        """
        Assign saturation impact level.
        
        Args:
            saturation (float): Current saturation score
            velocity (float): Saturation velocity
            breaches (list): Threshold breaches
        
        Returns:
            str: Impact level
        """
        # Critical impact
        if saturation >= self.CRITICAL_THRESHOLD or len(breaches) >= 2:
            return "Critical"
        
        # High impact
        if saturation >= self.FATIGUE_THRESHOLD or (saturation >= 60 and velocity > 1.5):
            return "High"
        
        # Medium impact
        if saturation >= self.SAFE_THRESHOLD or velocity > 1.0:
            return "Medium"
        
        # Low impact
        return "Low"
    
    def _estimate_time_to_peak(self, scores, velocity, peak_threshold=95):
        """
        Estimate days until peak saturation.
        
        Args:
            scores (np.array): Saturation scores
            velocity (float): Current velocity
            peak_threshold (float): Peak definition
        
        Returns:
            str or int: Estimated days or status
        """
        current = scores[-1]
        
        if current >= peak_threshold:
            return "Already Peaked"
        
        if velocity <= 0:
            return "Not Trending to Peak"
        
        remaining = peak_threshold - current
        days_to_peak = int(remaining / velocity)
        
        if days_to_peak > 100:
            return "100+ days"
        
        return f"{days_to_peak} days"
    
    def _generate_insights(self, saturation, stage, impact, risk, breaches):
        """
        Generate actionable insights.
        """
        breach_text = f" Breached {len(breaches)} threshold(s)." if breaches else ""
        
        if impact == "Critical":
            return f"🚨 CRITICAL: {stage} at {saturation:.1f}%. {breach_text} Market is oversaturated. Trend collapse imminent."
        
        elif impact == "High":
            return f"⚠️ HIGH IMPACT: {stage} at {saturation:.1f}%. Content fatigue setting in. Repetition risk: {risk}."
        
        elif impact == "Medium":
            return f"⚡ MODERATE: {stage} at {saturation:.1f}%. Market approaching saturation. Monitor for fatigue signals."
        
        else:  # Low
            return f"✅ HEALTHY: {stage} at {saturation:.1f}%. Plenty of room for growth. Repetition risk: {risk}."


# Test the agent
if __name__ == "__main__":
    print("🧪 Testing Saturation Agent\n")
    
    # Test 1: Time-series with increasing saturation
    print("Test 1: Time-series saturation analysis")
    
    # Create sample saturation data (0 to 95)
    sample_data = pd.DataFrame({
        'date': pd.date_range('2026-01-01', periods=60, freq='D'),
        'saturation_score': np.concatenate([
            np.linspace(0, 40, 20),    # Early growth
            np.linspace(40, 75, 20),   # Acceleration
            np.linspace(75, 95, 20)    # Near peak
        ])
    })
    
    agent = SaturationAgent()
    result = agent.analyze(sample_data)
    
    print(f"✅ Status: {result['status']}")
    print(f"📊 Saturation Score: {result['saturation_score']}/100")
    print(f"⚠️  Impact Level: {result['saturation_impact_level']}")
    print(f"📈 Market Penetration: {result['market_penetration']}%")
    print(f"🔄 Repetition Risk: {result['repetition_risk']}")
    print(f"🎯 Stage: {result['saturation_stage']}")
    print(f"⏰ Time to Peak: {result['time_to_peak']}")
    print(f"🚨 Fatigue Detected: {result['fatigue_detected']}")
    print(f"🔔 Threshold Breaches: {len(result['threshold_breaches'])}")
    print(f"💡 Insights: {result['insights']}\n")
    
    # Test 2: Snapshot analysis
    print("Test 2: Snapshot analysis")
    snapshot = {
        "saturation_level": "moderate",
        "penetration": 0.65
    }
    
    result2 = agent.analyze(snapshot)
    print(f"✅ Status: {result2['status']}")
    print(f"📊 Saturation Level: {result2['saturation_level']}")
    print(f"📈 Penetration: {result2['market_penetration']}")
    
    print("\n✅ Saturation Agent tests complete!")
