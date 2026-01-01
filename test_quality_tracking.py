"""
Test quality metrics tracking
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append('lambda')

from lambda_function import WeatherPipelineLambda
from datetime import datetime

# Initialize pipeline
pipeline = WeatherPipelineLambda()

# Run collection
print("Running weather collection with quality tracking...")
result = pipeline.run()

print("\n" + "="*70)
print("RESULTS")
print("="*70)
print(f"Records collected: {result['records_collected']}")
print(f"Records stored: {result['records_stored']}")
print(f"Execution time: {result['execution_time_ms']:.0f}ms")

if 'quality_metrics' in result and result['quality_metrics']:
    metrics = result['quality_metrics']
    print(f"\nQuality Metrics:")
    print(f"  Average score: {metrics['avg_quality_score']}")
    print(f"  Perfect quality: {metrics['perfect_quality_count']}/{metrics['total_records']}")
    print(f"  Degraded quality: {metrics['degraded_quality_count']}/{metrics['total_records']}")
    print(f"  Failed quality: {metrics['failed_quality_count']}/{metrics['total_records']}")
    
    if metrics['temperature_failures'] > 0:
        print(f"  Temperature failures: {metrics['temperature_failures']}")
    if metrics['humidity_failures'] > 0:
        print(f"  Humidity failures: {metrics['humidity_failures']}")
    if metrics['pressure_failures'] > 0:
        print(f"  Pressure failures: {metrics['pressure_failures']}")
    if metrics['wind_speed_failures'] > 0:
        print(f"  Wind speed failures: {metrics['wind_speed_failures']}")

print("\n✓ Quality tracking test complete")

