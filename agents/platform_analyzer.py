"""
Platform Comparison Analyzer
Cross-platform trend analysis for TikTok, Instagram, Twitter, YouTube.
Identifies platform-specific decline patterns and resilience.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


class PlatformAnalyzer:
    """
    Analyzes trend performance across multiple social media platforms.
    """
    
    def __init__(self):
        self.name = "Platform Analyzer"
        
        # Platform characteristics
        self.PLATFORM_PROFILES = {
            'TikTok': {
                'typical_lifespan': 14,  # days
                'virality_factor': 'high',
                'decay_speed': 'rapid'
            },
            'Instagram': {
                'typical_lifespan': 30,
                'virality_factor': 'medium',
                'decay_speed': 'moderate'
            },
            'Twitter': {
                'typical_lifespan': 7,
                'virality_factor': 'very_high',
                'decay_speed': 'very_rapid'
            },
            'YouTube': {
                'typical_lifespan': 60,
                'virality_factor': 'low',
                'decay_speed': 'slow'
            },
            'Facebook': {
                'typical_lifespan': 45,
                'virality_factor': 'low',
                'decay_speed': 'slow'
            }
        }
    
    def compare_platforms(self, data: pd.DataFrame, trend_name: Optional[str] = None) -> Dict:
        """
        Compare trend performance across platforms.
        
        Args:
            data (pd.DataFrame): Multi-platform trend data
            trend_name (str): Optional trend name filter
        
        Returns:
            dict: Platform comparison insights
        """
        print(f"[{self.name}] Comparing platform performance...")
        
        # Check if platform column exists
        platform_col = self._find_platform_column(data)
        
        if not platform_col:
            return {
                "status": "unavailable",
                "message": "No platform data found in dataset"
            }
        
        # Filter by trend if specified
        if trend_name and 'trend_name' in data.columns:
            data = data[data['trend_name'] == trend_name]
        
        # Group by platform
        platform_stats = self._calculate_platform_stats(data, platform_col)
        
        # Identify patterns
        decline_patterns = self._identify_decline_patterns(platform_stats)
        
        # Find resilient platforms
        resilience_ranking = self._rank_platform_resilience(platform_stats)
        
        # Platform-specific insights
        platform_insights = self._generate_platform_insights(platform_stats)
        
        return {
            "status": "success",
            "platforms_analyzed": list(platform_stats.keys()),
            "platform_statistics": platform_stats,
            "decline_patterns": decline_patterns,
            "resilience_ranking": resilience_ranking,
            "platform_insights": platform_insights,
            "recommended_focus_platform": resilience_ranking[0]['platform'] if resilience_ranking else None
        }
    
    def _find_platform_column(self, data: pd.DataFrame) -> Optional[str]:
        """
        Find platform column in dataset.
        """
        possible_names = ['platform', 'social_platform', 'channel', 'source']
        
        for col in data.columns:
            if col.lower() in possible_names:
                return col
        
        return None
    
    def _calculate_platform_stats(self, data: pd.DataFrame, platform_col: str) -> Dict:
        """
        Calculate statistics for each platform.
        """
        stats = {}
        
        for platform, group in data.groupby(platform_col):
            # Basic metrics
            avg_engagement = group.get('engagement_rate', pd.Series([0.5])).mean()
            avg_sentiment = group.get('sentiment_score', pd.Series([0.6])).mean()
            avg_saturation = group.get('saturation_score', pd.Series([50.0])).mean()
            
            # Trend metrics if available
            if 'engagement_rate' in group.columns and len(group) > 1:
                engagement_trend = group['engagement_rate'].pct_change().mean()
            else:
                engagement_trend = 0.0
            
            stats[platform] = {
                "sample_size": len(group),
                "avg_engagement_rate": round(avg_engagement, 3),
                "avg_sentiment_score": round(avg_sentiment, 3),
                "avg_saturation_score": round(avg_saturation, 2),
                "engagement_trend": round(engagement_trend, 3),
                "platform_health": self._calculate_platform_health(avg_engagement, avg_sentiment, avg_saturation)
            }
        
        return stats
    
    def _calculate_platform_health(self, engagement: float, sentiment: float, saturation: float) -> str:
        """
        Calculate overall platform health score.
        """
        # Health factors
        health_score = (
            engagement * 40 +
            sentiment * 30 +
            (100 - saturation) * 30
        )
        
        if health_score >= 70:
            return "Excellent"
        elif health_score >= 55:
            return "Good"
        elif health_score >= 40:
            return "Fair"
        else:
            return "Poor"
    
    def _identify_decline_patterns(self, platform_stats: Dict) -> Dict:
        """
        Identify platform-specific decline patterns.
        """
        patterns = {}
        
        for platform, stats in platform_stats.items():
            # Check for decline indicators
            declining = stats['engagement_trend'] < -0.05
            saturated = stats['avg_saturation_score'] > 70
            low_sentiment = stats['avg_sentiment_score'] < 0.5
            
            if declining and saturated:
                pattern = "Saturation-Driven Decline"
            elif declining and low_sentiment:
                pattern = "Sentiment-Driven Decline"
            elif saturated:
                pattern = "Early Saturation Signs"
            elif declining:
                pattern = "Organic Decline"
            else:
                pattern = "Stable/Growing"
            
            patterns[platform] = {
                "pattern": pattern,
                "is_declining": declining,
                "saturation_risk": saturated,
                "sentiment_risk": low_sentiment
            }
        
        return patterns
    
    def _rank_platform_resilience(self, platform_stats: Dict) -> List[Dict]:
        """
        Rank platforms by resilience (inverse of decline risk).
        """
        resilience_scores = []
        
        for platform, stats in platform_stats.items():
            # Calculate resilience score
            resilience = (
                stats['avg_engagement_rate'] * 100 * 0.4 +
                stats['avg_sentiment_score'] * 100 * 0.3 +
                (100 - stats['avg_saturation_score']) * 0.3
            )
            
            resilience_scores.append({
                "platform": platform,
                "resilience_score": round(resilience, 2),
                "health": stats['platform_health']
            })
        
        # Sort by resilience score (descending)
        resilience_scores.sort(key=lambda x: x['resilience_score'], reverse=True)
        
        # Add ranks
        for i, item in enumerate(resilience_scores, 1):
            item['rank'] = i
        
        return resilience_scores
    
    def _generate_platform_insights(self, platform_stats: Dict) -> Dict:
        """
        Generate actionable insights per platform.
        """
        insights = {}
        
        for platform, stats in platform_stats.items():
            recommendations = []
            
            # Engagement-based insights
            if stats['avg_engagement_rate'] < 0.1:
                recommendations.append(f"Low engagement on {platform} - boost with interactive content")
            elif stats['avg_engagement_rate'] > 0.3:
                recommendations.append(f"Strong engagement on {platform} - scale investment here")
            
            # Saturation-based insights
            if stats['avg_saturation_score'] > 75:
                recommendations.append(f"{platform} showing saturation - introduce fresh variations")
            
            # Sentiment-based insights
            if stats['avg_sentiment_score'] < 0.5:
                recommendations.append(f"Negative sentiment on {platform} - address user concerns")
            
            # Trend-based insights
            if stats['engagement_trend'] < -0.1:
                recommendations.append(f"Rapid decline on {platform} - urgent intervention needed")
            
            # Platform-specific advice
            if platform in self.PLATFORM_PROFILES:
                profile = self.PLATFORM_PROFILES[platform]
                if profile['decay_speed'] == 'rapid' or profile['decay_speed'] == 'very_rapid':
                    recommendations.append(f"{platform} has rapid decay - maintain consistent posting")
            
            insights[platform] = {
                "health_status": stats['platform_health'],
                "key_metrics": {
                    "engagement": stats['avg_engagement_rate'],
                    "sentiment": stats['avg_sentiment_score'],
                    "saturation": stats['avg_saturation_score']
                },
                "recommendations": recommendations if recommendations else [f"{platform} performance is stable"]
            }
        
        return insights


# Test the analyzer
if __name__ == "__main__":
    print("🧪 Testing Platform Analyzer\n")
    
    # Create sample multi-platform data
    sample_data = pd.DataFrame({
        'platform': ['TikTok', 'TikTok', 'Instagram', 'Instagram', 'Twitter', 'YouTube'],
        'trend_name': ['Dance Challenge'] * 6,
        'engagement_rate': [0.25, 0.20, 0.18, 0.17, 0.15, 0.22],
        'sentiment_score': [0.8, 0.75, 0.7, 0.68, 0.6, 0.85],
        'saturation_score': [60, 70, 55, 58, 75, 45]
    })
    
    analyzer = PlatformAnalyzer()
    
    # Compare platforms
    comparison = analyzer.compare_platforms(sample_data, "Dance Challenge")
    
    print(f"✅ Status: {comparison['status']}")
    print(f"📊 Platforms Analyzed: {comparison['platforms_analyzed']}")
    
    print(f"\n🏆 Resilience Ranking:")
    for item in comparison['resilience_ranking']:
        print(f"  {item['rank']}. {item['platform']}: {item['resilience_score']} ({item['health']})")
    
    print(f"\n📈 Decline Patterns:")
    for platform, pattern in comparison['decline_patterns'].items():
        print(f"  {platform}: {pattern['pattern']}")
    
    print(f"\n💡 Recommended Focus: {comparison['recommended_focus_platform']}")
    
    print("\n✅ Platform Analyzer test complete!")
