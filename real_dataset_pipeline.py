"""
Real Dataset Integration Pipeline
Complete pipeline for loading, cleaning, and analyzing real Kaggle data.
Integrates dataset with AI intelligence layer.
"""

import sys
sys.path.append('.')

import pandas as pd
from typing import Dict, List, Optional

from utils.kaggle_loader import KaggleDatasetLoader
from utils.data_preprocessor import DataPreprocessor
from utils.timeseries_transformer import TimeSeriesTransformer
from ai_api import analyze_trend, AIIntelligenceLayer


class RealDatasetPipeline:
    """
    End-to-end pipeline for real dataset analysis.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.name = "Real Dataset Pipeline"
        self.loader = KaggleDatasetLoader()
        self.preprocessor = DataPreprocessor()
        self.transformer = TimeSeriesTransformer()
        self.ai_layer = AIIntelligenceLayer(featherless_api_key=api_key)
        
        self.raw_data = None
        self.clean_data = None
        self.trend_timeseries = None
    
    def run_complete_pipeline(self, force_download: bool = False) -> Dict:
        """
        Run complete data pipeline from download to analysis.
        
        Args:
            force_download (bool): Force re-download of dataset
        
        Returns:
            dict: Pipeline results and summary
        """
        print(f"\n{'='*70}")
        print(f"  {self.name.upper()} - COMPLETE EXECUTION")
        print('='*70)
        
        results = {}
        
        try:
            # STEP 5: Load Kaggle dataset
            print(f"\n🔄 STEP 5: Loading Kaggle Dataset")
            self.raw_data = self.loader.load_dataset(force_download=force_download)
            results['load_status'] = 'success'
            results['total_rows'] = len(self.raw_data)
            
            # Display schema
            self.loader.display_schema()
            
            # STEP 6: Clean dataset
            print(f"\n🔄 STEP 6: Cleaning Dataset")
            self.clean_data = self.preprocessor.clean_dataset(self.raw_data)
            results['clean_status'] = 'success'
            results['clean_rows'] = len(self.clean_data)
            
            # STEP 7: Engineer features
            print(f"\n🔄 STEP 7: Engineering Features")
            self.clean_data = self.preprocessor.engineer_features(self.clean_data)
            results['feature_status'] = 'success'
            
            # STEP 8: Transform to time-series
            print(f"\n🔄 STEP 8: Time-Series Transformation")
            self.trend_timeseries = self.transformer.transform_to_lifecycle(self.clean_data)
            results['transform_status'] = 'success'
            results['trends_found'] = len(self.trend_timeseries)
            
            # STEP 9-11: Analyze with AI layer
            print(f"\n🔄 STEP 9-11: AI Analysis on Real Data")
            results['analyses'] = self._run_ai_analysis()
            
            print(f"\n{'='*70}")
            print("  ✅ PIPELINE COMPLETE")
            print('='*70)
            
            return results
            
        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            results['status'] = 'failed'
            results['error'] = str(e)
            return results
    
    def _run_ai_analysis(self) -> Dict:
        """
        Run AI analysis on transformed trends.
        """
        analyses = {}
        
        # Analyze first 3 trends as examples
        trend_names = list(self.trend_timeseries.keys())[:3]
        
        for i, trend_name in enumerate(trend_names, 1):
            print(f"\n  Analyzing Trend {i}/{len(trend_names)}: {trend_name}")
            
            try:
                # Get time-series data
                lifecycle_df = self.trend_timeseries[trend_name]
                
                # Convert to agent format
                agent_df = self.transformer.aggregate_to_agent_format(lifecycle_df)
                
                # Run AI analysis
                analysis = self.ai_layer.analyze_trend(agent_df, trend_name)
                
                # Store results
                analyses[trend_name] = {
                    'decline_probability': analysis['decline_probability'],
                    'lifecycle_stage': analysis['lifecycle_stage'],
                    'early_warning': analysis['early_warning']['warning_level'],
                    'narrative_preview': analysis['narrative_explanation'][:200] + "..."
                }
                
                print(f"    ✅ Decline: {analysis['decline_probability']}%")
                print(f"    ✅ Stage: {analysis['lifecycle_stage']}")
                print(f"    ✅ Warning: {analysis['early_warning']['warning_level']}")
                
            except Exception as e:
                print(f"    ❌ Analysis failed: {e}")
                analyses[trend_name] = {'error': str(e)}
        
        return analyses
    
    def analyze_single_trend(self, trend_name: str) -> Dict:
        """
        Analyze a single trend by name.
        
        Args:
            trend_name (str): Name of trend to analyze
        
        Returns:
            dict: Complete analysis results
        """
        if self.trend_timeseries is None:
            raise ValueError("Pipeline not run. Call run_complete_pipeline() first.")
        
        if trend_name not in self.trend_timeseries:
            raise ValueError(f"Trend '{trend_name}' not found in dataset")
        
        # Get time-series  data
        lifecycle_df = self.trend_timeseries[trend_name]
        
        # Convert to agent format
        agent_df = self.transformer.aggregate_to_agent_format(lifecycle_df)
        
        # Run complete analysis
        analysis = self.ai_layer.analyze_trend(agent_df, trend_name)
        
        return analysis
    
    def get_available_trends(self) -> List[str]:
        """
        Get list of available trends in dataset.
        
        Returns:
            list: Trend names
        """
        if self.trend_timeseries is None:
            return []
        
        return list(self.trend_timeseries.keys())
    
    def export_analysis_results(self, filepath: str):
        """
        Export all analysis results to JSON.
        
        Args:
            filepath (str): Output file path
        """
        if self.trend_timeseries is None:
            raise ValueError("No data to export. Run pipeline first.")
        
        import json
        
        export_data = {
            'dataset_info': {
                'total_rows': len(self.raw_data) if self.raw_data is not None else 0,
                'clean_rows': len(self.clean_data) if self.clean_data is not None else 0,
                'trends_count': len(self.trend_timeseries)
            },
            'trends': list(self.trend_timeseries.keys())
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Exported results to: {filepath}")


def run_demo():
    """
    Demo function for real dataset integration.
    """
    print("\n🚀 REAL DATASET INTEGRATION DEMO\n")
    
    try:
        # Initialize pipeline
        pipeline = RealDatasetPipeline()
        
        # Run complete pipeline
        results = pipeline.run_complete_pipeline()
        
        # Display summary
        print(f"\n📊 PIPELINE SUMMARY:")
        print(f"  • Dataset Loaded: {results.get('load_status', 'N/A')}")
        print(f"  • Total Rows: {results.get('total_rows', 0)}")
        print(f"  • Clean Rows: {results.get('clean_rows', 0)}")
        print(f"  • Trends Found: {results.get('trends_found', 0)}")
        
        if 'analyses' in results:
            print(f"\n📈 TREND ANALYSES:")
            for trend_name, analysis in results['analyses'].items():
                if 'error' not in analysis:
                    print(f"\n  Trend: {trend_name}")
                    print(f"    Decline: {analysis['decline_probability']}%")
                    print(f"    Stage: {analysis['lifecycle_stage']}")
                    print(f"    Warning: {analysis['early_warning']}")
        
        # Get available trends
        available = pipeline.get_available_trends()
        print(f"\n📋 Available Trends ({len(available)}):")
        for i, trend in enumerate(available[:10], 1):
            print(f"  {i}. {trend}")
        
        if len(available) > 10:
            print(f"  ... and {len(available) - 10} more")
        
        print("\n✅ Real Dataset Integration Demo Complete!")
        
    except ImportError as e:
        print(f"\n⚠️  Missing dependency: {e}")
        print("Install with: pip install kagglehub scikit-learn")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


# Test pipeline
if __name__ == "__main__":
    run_demo()
