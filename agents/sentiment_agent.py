"""
Sentiment Agent
Analyzes sentiment from text data (comments, reviews, social media posts).
Detects sentiment shifts and volatility to assess trend health.
"""

import numpy as np
import pandas as pd


class SentimentAgent:
    def __init__(self):
        self.name = "Sentiment Agent"
        self.description = "Analyzes sentiment polarity and emotional tone"
        
        # Sentiment thresholds
        self.POSITIVE_THRESHOLD = 0.6
        self.NEUTRAL_LOWER = 0.4
        self.NEUTRAL_UPPER = 0.6
    
    def analyze(self, data):
        """
        Analyzes sentiment from text content or time-series data.
        
        Args:
            data (pd.DataFrame or list or str): Sentiment data to analyze
        
        Returns:
            dict: Sentiment analysis results with polarity and emotion scores
        """
        print(f"[{self.name}] Processing sentiment analysis...")
        
        # Handle different input types
        if isinstance(data, pd.DataFrame):
            return self._analyze_timeseries(data)
        elif isinstance(data, (list, str)):
            return self._analyze_text(data)
        else:
            raise ValueError("Data must be a pandas DataFrame, list, or string")
    
    def _analyze_timeseries(self, df):
        """
        Analyze time-series sentiment data.
        
        Args:
            df (pd.DataFrame): Time-series data with sentiment_score column
        
        Returns:
            dict: Comprehensive sentiment analysis
        """
        if 'sentiment_score' not in df.columns:
            raise ValueError("DataFrame must contain 'sentiment_score' column")
        
        sentiment_scores = df['sentiment_score'].values
        
        # Current vs historical sentiment
        initial_sentiment = np.mean(sentiment_scores[:7])  # First week average
        current_sentiment = np.mean(sentiment_scores[-7:])  # Last week average
        overall_sentiment = np.mean(sentiment_scores)
        
        # Detect sentiment shift
        sentiment_shift = self._detect_sentiment_shift(sentiment_scores)
        
        # Calculate sentiment change percentage
        if initial_sentiment > 0:
            sentiment_change_percent = ((current_sentiment - initial_sentiment) / initial_sentiment) * 100
        else:
            sentiment_change_percent = 0
        
        # Calculate volatility
        volatility = self._calculate_volatility(sentiment_scores)
        
        # Assign impact level
        impact_level = self._assign_impact_level(sentiment_shift, volatility, sentiment_change_percent)
        
        # Categorize current sentiment
        current_category = self._categorize_sentiment(current_sentiment)
        initial_category = self._categorize_sentiment(initial_sentiment)
        
        # Generate shift description
        shift_description = self._generate_shift_description(
            initial_category, 
            current_category, 
            sentiment_change_percent
        )
        
        return {
            "agent": self.name,
            "status": "success",
            "sentiment_shift": sentiment_shift,
            "shift_description": shift_description,
            "impact_level": impact_level,
            "metrics": {
                "initial_sentiment": round(initial_sentiment, 4),
                "current_sentiment": round(current_sentiment, 4),
                "overall_sentiment": round(overall_sentiment, 4),
                "sentiment_change_percent": round(sentiment_change_percent, 2),
                "volatility": round(volatility, 4)
            },
            "sentiment_categories": {
                "initial": initial_category,
                "current": current_category
            },
            "trend_direction": "improving" if sentiment_change_percent > 5 else "declining" if sentiment_change_percent < -5 else "stable",
            "insights": self._generate_insights(
                shift_description, 
                impact_level, 
                volatility,
                sentiment_change_percent
            )
        }
    
    def _analyze_text(self, text_data):
        """
        Analyze sentiment from text content (placeholder for NLP integration).
        
        Args:
            text_data (list or str): Text content to analyze
        
        Returns:
            dict: Sentiment analysis results
        """
        # This is a placeholder - in production, integrate with NLP models
        # (e.g., VADER, TextBlob, Transformers)
        
        if isinstance(text_data, str):
            text_data = [text_data]
        
        # Mock sentiment calculation
        mock_score = 0.65  # Placeholder positive sentiment
        
        return {
            "agent": self.name,
            "status": "success",
            "overall_sentiment": "positive",
            "sentiment_score": mock_score,
            "emotions": {
                "positive": 0.45,
                "neutral": 0.35,
                "negative": 0.20
            },
            "key_themes": ["quality", "value", "experience"],
            "insights": "Text sentiment analysis placeholder. Integrate NLP model for production use."
        }
    
    def _detect_sentiment_shift(self, sentiment_scores):
        """
        Detect major sentiment shift pattern.
        
        Args:
            sentiment_scores (np.array): Array of sentiment scores over time
        
        Returns:
            str: Shift pattern description
        """
        # Divide timeline into thirds
        length = len(sentiment_scores)
        third = length // 3
        
        early_avg = np.mean(sentiment_scores[:third])
        mid_avg = np.mean(sentiment_scores[third:2*third])
        late_avg = np.mean(sentiment_scores[2*third:])
        
        early_cat = self._categorize_sentiment(early_avg)
        mid_cat = self._categorize_sentiment(mid_avg)
        late_cat = self._categorize_sentiment(late_avg)
        
        # Detect shift pattern
        if early_cat == "Positive" and late_cat == "Negative":
            return "Positive → Negative"
        elif early_cat == "Positive" and late_cat == "Neutral":
            return "Positive → Neutral"
        elif early_cat == "Neutral" and late_cat == "Negative":
            return "Neutral → Negative"
        elif early_cat == "Negative" and late_cat == "Positive":
            return "Negative → Positive"
        elif early_cat != late_cat:
            return f"{early_cat} → {late_cat}"
        else:
            return "Stable"
    
    def _categorize_sentiment(self, score):
        """
        Categorize sentiment score into Positive/Neutral/Negative.
        
        Args:
            score (float): Sentiment score (0-1 scale)
        
        Returns:
            str: Sentiment category
        """
        if score >= self.POSITIVE_THRESHOLD:
            return "Positive"
        elif score >= self.NEUTRAL_LOWER:
            return "Neutral"
        else:
            return "Negative"
    
    def _calculate_volatility(self, sentiment_scores):
        """
        Calculate sentiment volatility (standard deviation).
        
        Args:
            sentiment_scores (np.array): Sentiment scores over time
        
        Returns:
            float: Volatility measure
        """
        return np.std(sentiment_scores)
    
    def _assign_impact_level(self, shift, volatility, change_percent):
        """
        Assign impact level based on sentiment shift and volatility.
        
        Args:
            shift (str): Sentiment shift pattern
            volatility (float): Sentiment volatility
            change_percent (float): Percentage change in sentiment
        
        Returns:
            str: Impact level (Low, Medium, High, Critical)
        """
        # Critical shifts
        if "Positive → Negative" in shift or change_percent < -30:
            return "Critical"
        
        # High impact
        if "Negative" in shift and volatility > 0.15:
            return "High"
        
        if change_percent < -20 or volatility > 0.20:
            return "High"
        
        # Medium impact
        if "Neutral" in shift or (volatility > 0.10 and change_percent < -10):
            return "Medium"
        
        # Low impact
        return "Low"
    
    def _generate_shift_description(self, initial_cat, current_cat, change_percent):
        """
        Generate human-readable shift description.
        """
        if initial_cat == current_cat:
            return f"Sentiment remains {current_cat.lower()} with {abs(change_percent):.1f}% change"
        else:
            direction = "improved" if change_percent > 0 else "declined"
            return f"Sentiment {direction} from {initial_cat.lower()} to {current_cat.lower()} ({change_percent:+.1f}%)"
    
    def _generate_insights(self, shift_desc, impact_level, volatility, change_percent):
        """
        Generate actionable insights based on analysis.
        """
        if impact_level == "Critical":
            return f"⚠️ CRITICAL: {shift_desc}. High volatility ({volatility:.3f}). Immediate intervention required."
        
        elif impact_level == "High":
            return f"⚠️ HIGH RISK: {shift_desc}. Monitor closely and consider damage control strategies."
        
        elif impact_level == "Medium":
            return f"⚡ MODERATE: {shift_desc}. Keep monitoring sentiment trends."
        
        else:  # Low
            if change_percent > 0:
                return f"✅ HEALTHY: {shift_desc}. Sentiment is stable or improving."
            else:
                return f"ℹ️ STABLE: {shift_desc}. Minor fluctuations within acceptable range."


# Test the agent
if __name__ == "__main__":
    print("🧪 Testing Sentiment Agent\n")
    
    # Test 1: Time-series with sentiment decline
    print("Test 1: Time-series sentiment analysis")
    
    # Create sample sentiment decline data
    sample_data = pd.DataFrame({
        'date': pd.date_range('2026-01-01', periods=45, freq='D'),
        'sentiment_score': np.concatenate([
            np.random.normal(0.75, 0.05, 15),  # Positive phase
            np.random.normal(0.55, 0.08, 15),  # Neutral phase
            np.random.normal(0.35, 0.10, 15)   # Negative phase
        ])
    })
    
    agent = SentimentAgent()
    result = agent.analyze(sample_data)
    
    print(f"✅ Status: {result['status']}")
    print(f"📊 Sentiment Shift: {result['sentiment_shift']}")
    print(f"📝 Description: {result['shift_description']}")
    print(f"⚠️  Impact Level: {result['impact_level']}")
    print(f"📈 Volatility: {result['metrics']['volatility']}")
    print(f"🔄 Trend: {result['trend_direction']}")
    print(f"💡 Insights: {result['insights']}\n")
    
    # Test 2: Text analysis
    print("Test 2: Text sentiment analysis")
    text_sample = ["Great product!", "Love it!", "Amazing experience"]
    
    result2 = agent.analyze(text_sample)
    print(f"✅ Status: {result2['status']}")
    print(f"😊 Overall Sentiment: {result2['overall_sentiment']}")
    print(f"📊 Score: {result2['sentiment_score']}")
    
    print("\n✅ Sentiment Agent tests complete!")
