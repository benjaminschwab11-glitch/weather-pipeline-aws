"""
Day 4: Integrated Weather Data Pipeline
Connects API → Database with data quality checks
"""

import requests
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
import os
from dotenv import load_dotenv
import time

load_dotenv()

class WeatherPipeline:
    """
    Production-grade weather data pipeline
    Demonstrates: API integration, data validation, database operations, error handling
    """
    
    def __init__(self):
        # API Configuration
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.cities = [
            'San Diego',
            'Los Angeles', 
            'San Francisco',
            'Seattle',
            'Portland'
        ]
        
        # Database Configuration
        self.db_params = {
            'host': os.getenv('RDS_ENDPOINT'),
            'database': os.getenv('RDS_DATABASE'),
            'user': os.getenv('RDS_USERNAME'),
            'password': os.getenv('RDS_PASSWORD'),
            'port': os.getenv('RDS_PORT', '5432')
        }
    
    def validate_record(self, record):
        """
        Data quality validation - DBA discipline
        Returns quality score from 0.0 to 1.0
        """
        score = 1.0
        issues = []
        
        # Temperature range check
        if not (-50 <= record['temperature'] <= 150):
            score -= 0.3
            issues.append(f"Temperature {record['temperature']} out of range")
        
        # Humidity range check
        if not (0 <= record['humidity'] <= 100):
            score -= 0.3
            issues.append(f"Humidity {record['humidity']} out of range")
        
        # Pressure range check
        if not (900 <= record['pressure'] <= 1100):
            score -= 0.3
            issues.append(f"Pressure {record['pressure']} out of range")
        
        # Wind speed sanity check
        if record['wind_speed'] < 0 or record['wind_speed'] > 200:
            score -= 0.1
            issues.append(f"Wind speed {record['wind_speed']} suspicious")
        
        final_score = max(score, 0.0)
        
        if issues:
            print(f"  ⚠️  Quality issues for {record['city']}: {', '.join(issues)}")
            print(f"      Quality score: {final_score:.2f}")
        
        return final_score
    
    def fetch_weather(self, city):
        """
        Fetch weather data from API with error handling
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'imperial'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract and structure data
            record = {
                'city': city,
                'timestamp': datetime.utcnow(),
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'weather_condition': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description']
            }
            
            # Add quality score
            record['data_quality_score'] = self.validate_record(record)
            
            return record
            
        except requests.exceptions.Timeout:
            print(f"  ❌ Timeout fetching {city}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"  ❌ API error for {city}: {e}")
            return None
        except KeyError as e:
            print(f"  ❌ Unexpected data structure for {city}: missing {e}")
            return None
        except Exception as e:
            print(f"  ❌ Unexpected error for {city}: {e}")
            return None
    
    def collect_all_weather(self):
        """
        Collect weather data for all cities
        """
        print(f"\n{'='*70}")
        print(f"🌤️  WEATHER DATA COLLECTION")
        print(f"{'='*70}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Cities: {len(self.cities)}")
        print(f"{'-'*70}")
        
        results = []
        for city in self.cities:
            print(f"\n📍 Collecting {city}...")
            record = self.fetch_weather(city)
            
            if record:
                results.append(record)
                print(f"  ✅ {record['temperature']:.1f}°F | "
                      f"{record['humidity']}% humidity | "
                      f"{record['weather_description']}")
            
            # Rate limiting courtesy - don't hammer the API
            time.sleep(1)
        
        print(f"\n{'-'*70}")
        print(f"✅ Collected {len(results)}/{len(self.cities)} cities successfully")
        
        return results
    
    def store_weather_data(self, records):
        """
        Store weather records in RDS with proper error handling
        """
        if not records:
            print("⚠️  No records to store")
            return 0
        
        print(f"\n{'='*70}")
        print(f"💾 STORING DATA TO RDS")
        print(f"{'='*70}")
        
        conn = None
        try:
            # Connect to database
            print("🔌 Connecting to RDS...")
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            
            # Prepare insert query
            insert_query = '''
                INSERT INTO weather_observations 
                (city, timestamp, temperature, feels_like, humidity, 
                 pressure, wind_speed, weather_condition, weather_description,
                 data_quality_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (city, timestamp) DO NOTHING
            '''
            
            # Prepare data tuples
            data = [
                (
                    r['city'],
                    r['timestamp'],
                    r['temperature'],
                    r['feels_like'],
                    r['humidity'],
                    r['pressure'],
                    r['wind_speed'],
                    r['weather_condition'],
                    r['weather_description'],
                    r['data_quality_score']
                )
                for r in records
            ]
            
            # Batch insert for efficiency
            execute_batch(cursor, insert_query, data)
            conn.commit()
            
            inserted_count = cursor.rowcount
            
            print(f"✅ Successfully stored {inserted_count} records")
            
            # Query to show what we just inserted
            cursor.execute("""
                SELECT city, temperature, weather_condition 
                FROM weather_observations 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            
            recent = cursor.fetchall()
            print(f"\n📊 Most recent records:")
            for row in recent:
                print(f"  • {row[0]:15s} | {row[1]:5.1f}°F | {row[2]}")
            
            cursor.close()
            
            return inserted_count
            
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"❌ Database error: {e}")
            return 0
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Unexpected error storing data: {e}")
            return 0
            
        finally:
            if conn:
                conn.close()
                print("🔌 Database connection closed")
    
    def get_statistics(self):
        """
        Query database for pipeline statistics
        """
        print(f"\n{'='*70}")
        print(f"📈 PIPELINE STATISTICS")
        print(f"{'='*70}")
        
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            
            # Total records
            cursor.execute("SELECT COUNT(*) FROM weather_observations")
            total_records = cursor.fetchone()[0]
            print(f"Total records in database: {total_records:,}")
            
            # Records per city
            cursor.execute("""
                SELECT city, COUNT(*) as count 
                FROM weather_observations 
                GROUP BY city 
                ORDER BY count DESC
            """)
            print(f"\nRecords by city:")
            for row in cursor.fetchall():
                print(f"  {row[0]:15s}: {row[1]:,} records")
            
            # Data quality summary
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(*) FILTER (WHERE data_quality_score >= 0.9) as excellent,
                    COUNT(*) FILTER (WHERE data_quality_score >= 0.7 AND data_quality_score < 0.9) as good,
                    COUNT(*) FILTER (WHERE data_quality_score < 0.7) as poor
                FROM weather_observations
            """)
            stats = cursor.fetchone()
            print(f"\nData quality:")
            print(f"  Excellent (≥0.9): {stats[1]:,} ({stats[1]/stats[0]*100:.1f}%)")
            print(f"  Good (0.7-0.9):  {stats[2]:,} ({stats[2]/stats[0]*100:.1f}%)")
            print(f"  Poor (<0.7):     {stats[3]:,} ({stats[3]/stats[0]*100:.1f}%)")
            
            # Latest observation time
            cursor.execute("SELECT MAX(timestamp) FROM weather_observations")
            latest = cursor.fetchone()[0]
            if latest:
                print(f"\nLatest observation: {latest.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
    
    def run(self):
        """
        Execute complete pipeline: Collect → Validate → Store → Report
        """
        print("\n" + "="*70)
        print("🚀 WEATHER PIPELINE EXECUTION")
        print("="*70)
        print(f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Collect data from API
        records = self.collect_all_weather()
        
        # Step 2: Store data in database
        if records:
            stored = self.store_weather_data(records)
            
            # Step 3: Show statistics
            if stored > 0:
                self.get_statistics()
        
        print(f"\n{'='*70}")
        print(f"✅ PIPELINE EXECUTION COMPLETE")
        print(f"{'='*70}\n")


if __name__ == "__main__":
    pipeline = WeatherPipeline()
    pipeline.run()

