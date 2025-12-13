"""
Comprehensive pipeline statistics
"""

import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def get_comprehensive_stats():
    """Get detailed pipeline statistics"""
    conn = psycopg2.connect(
        host=os.getenv('RDS_ENDPOINT'),
        database=os.getenv('RDS_DATABASE'),
        user=os.getenv('RDS_USERNAME'),
        password=os.getenv('RDS_PASSWORD'),
        port=os.getenv('RDS_PORT', '5432')
    )
    
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("WEATHER PIPELINE - COMPREHENSIVE STATISTICS")
    print("="*80)
    
    # Total records
    cursor.execute("SELECT COUNT(*) FROM weather_observations")
    total = cursor.fetchone()[0]
    print(f"\n📊 TOTAL RECORDS: {total:,}")
    
    # Date range
    cursor.execute("""
        SELECT 
            MIN(timestamp) as first_observation,
            MAX(timestamp) as last_observation
        FROM weather_observations
    """)
    dates = cursor.fetchone()
    if dates[0]:
        print(f"\n📅 DATA RANGE:")
        print(f"   First observation: {dates[0].strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"   Last observation:  {dates[1].strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        duration = dates[1] - dates[0]
        hours = duration.total_seconds() / 3600
        print(f"   Duration: {duration.days} days, {duration.seconds//3600} hours ({hours:.1f} hours total)")
    
    # Records per city
    cursor.execute("""
        SELECT city, COUNT(*) as count, 
               MIN(timestamp) as first_seen,
               MAX(timestamp) as last_seen
        FROM weather_observations 
        GROUP BY city 
        ORDER BY count DESC
    """)
    print(f"\n🌍 RECORDS BY CITY:")
    for row in cursor.fetchall():
        print(f"   {row[0]:15s}: {row[1]:4,} records | Last: {row[3].strftime('%m/%d %H:%M')}")
    
    # Data quality breakdown
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            ROUND(AVG(data_quality_score), 3) as avg_quality,
            COUNT(*) FILTER (WHERE data_quality_score = 1.0) as perfect,
            COUNT(*) FILTER (WHERE data_quality_score >= 0.9 AND data_quality_score < 1.0) as excellent,
            COUNT(*) FILTER (WHERE data_quality_score >= 0.7 AND data_quality_score < 0.9) as good,
            COUNT(*) FILTER (WHERE data_quality_score < 0.7) as poor
        FROM weather_observations
    """)
    stats = cursor.fetchone()
    print(f"\n✅ DATA QUALITY:")
    print(f"   Average quality score: {stats[1]:.3f}")
    print(f"   Perfect (1.0):     {stats[2]:4,} ({stats[2]/stats[0]*100:5.1f}%)")
    print(f"   Excellent (0.9+):  {stats[3]:4,} ({stats[3]/stats[0]*100:5.1f}%)")
    print(f"   Good (0.7-0.9):    {stats[4]:4,} ({stats[4]/stats[0]*100:5.1f}%)")
    print(f"   Poor (<0.7):       {stats[5]:4,} ({stats[5]/stats[0]*100:5.1f}%)")
    
    # Hourly collection rate
    cursor.execute("""
        SELECT 
            DATE_TRUNC('hour', timestamp) as hour,
            COUNT(*) as records
        FROM weather_observations
        WHERE timestamp > NOW() - INTERVAL '24 hours'
        GROUP BY hour
        ORDER BY hour DESC
        LIMIT 10
    """)
    print(f"\n⏰ RECENT HOURLY ACTIVITY (Last 24 hours):")
    for row in cursor.fetchall():
        print(f"   {row[0].strftime('%m/%d %H:00')}: {row[1]:2} records")
    
    # Temperature insights
    cursor.execute("""
        SELECT 
            city,
            ROUND(AVG(temperature), 1) as avg_temp,
            ROUND(MIN(temperature), 1) as min_temp,
            ROUND(MAX(temperature), 1) as max_temp
        FROM weather_observations
        GROUP BY city
        ORDER BY avg_temp DESC
    """)
    print(f"\n🌡️  TEMPERATURE SUMMARY:")
    print(f"   {'City':<15} {'Avg':>6} {'Min':>6} {'Max':>6}")
    print(f"   {'-'*15} {'-'*6} {'-'*6} {'-'*6}")
    for row in cursor.fetchall():
        print(f"   {row[0]:<15} {row[1]:>5.1f}° {row[2]:>5.1f}° {row[3]:>5.1f}°")
    
    # Storage size
    cursor.execute("""
        SELECT pg_size_pretty(pg_total_relation_size('weather_observations'))
    """)
    size = cursor.fetchone()[0]
    print(f"\n💾 DATABASE SIZE:")
    print(f"   Table size: {size}")
    
    # Expected vs actual collections (assuming 15-min intervals)
    if dates[0]:
        expected_collections = int(hours / 0.25) * len(['San Diego', 'Los Angeles', 'San Francisco', 'Seattle', 'Portland'])
        print(f"\n📈 COLLECTION EFFICIENCY:")
        print(f"   Expected records (15-min intervals): ~{expected_collections:,}")
        print(f"   Actual records: {total:,}")
        if expected_collections > 0:
            efficiency = (total / expected_collections) * 100
            print(f"   Collection rate: {efficiency:.1f}%")
    
    print("\n" + "="*80 + "\n")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    get_comprehensive_stats()

