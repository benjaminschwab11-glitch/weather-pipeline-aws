"""
Query weather data from RDS
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def query_recent_weather():
    """Show recent weather observations"""
    conn = psycopg2.connect(
        host=os.getenv('RDS_ENDPOINT'),
        database=os.getenv('RDS_DATABASE'),
        user=os.getenv('RDS_USERNAME'),
        password=os.getenv('RDS_PASSWORD'),
        port=os.getenv('RDS_PORT', '5432')
    )
    
    cursor = conn.cursor()
    
    # Query last 20 observations
    cursor.execute("""
        SELECT 
            city,
            timestamp,
            temperature,
            feels_like,
            humidity,
            weather_condition,
            data_quality_score
        FROM weather_observations
        ORDER BY timestamp DESC
        LIMIT 20
    """)
    
    print("\n" + "="*90)
    print("RECENT WEATHER OBSERVATIONS")
    print("="*90)
    print(f"{'City':<15} {'Timestamp':<20} {'Temp':<8} {'Feels':<8} {'Humid':<7} {'Condition':<12} {'Quality':<7}")
    print("-"*90)
    
    for row in cursor.fetchall():
        print(f"{row[0]:<15} {row[1].strftime('%Y-%m-%d %H:%M'):<20} "
              f"{row[2]:>5.1f}°F {row[3]:>5.1f}°F {row[4]:>5}% "
              f"{row[5]:<12} {row[6]:>6.2f}")
    
    print("="*90 + "\n")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    query_recent_weather()

