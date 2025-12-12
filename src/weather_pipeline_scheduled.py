"""
Day 5: Scheduled Weather Data Pipeline with Logging
Production-ready version with professional logging
"""

import requests
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
import os
from dotenv import load_dotenv
import time
from logger_config import setup_logger

load_dotenv()

class WeatherPipeline:
    """
    Production weather data pipeline with logging
    """
    
    def __init__(self):
        self.logger = setup_logger('weather_pipeline')
        
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
        
        self.logger.info("WeatherPipeline initialized")
        self.logger.info(f"Tracking {len(self.cities)} cities")
    
    def validate_record(self, record):
        """Data quality validation"""
        score = 1.0
        issues = []
        
        if not (-50 <= record['temperature'] <= 150):
            score -= 0.3
            issues.append(f"Temperature {record['temperature']} out of range")
        
        if not (0 <= record['humidity'] <= 100):
            score -= 0.3
            issues.append(f"Humidity {record['humidity']} out of range")
        
        if not (900 <= record['pressure'] <= 1100):
            score -= 0.3
            issues.append(f"Pressure {record['pressure']} out of range")
        
        if record['wind_speed'] < 0 or record['wind_speed'] > 200:
            score -= 0.1
            issues.append(f"Wind speed {record['wind_speed']} suspicious")
        
        final_score = max(score, 0.0)
        
        if issues:
            self.logger.warning(f"Quality issues for {record['city']}: {', '.join(issues)} (score: {final_score:.2f})")
        
        return final_score
    
    def fetch_weather(self, city):
        """Fetch weather data from API"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'imperial'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
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
            
            record['data_quality_score'] = self.validate_record(record)
            
            self.logger.info(f"Collected {city}: {record['temperature']:.1f}°F, {record['weather_description']}")
            return record
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout fetching {city}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API error for {city}: {e}")
            return None
        except KeyError as e:
            self.logger.error(f"Unexpected data structure for {city}: missing {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error for {city}: {e}")
            return None
    
    def collect_all_weather(self):
        """Collect weather data for all cities"""
        self.logger.info("="*70)
        self.logger.info("Starting weather data collection")
        
        results = []
        for city in self.cities:
            record = self.fetch_weather(city)
            
            if record:
                results.append(record)
            
            time.sleep(1)  # Rate limiting
        
        self.logger.info(f"Collection complete: {len(results)}/{len(self.cities)} cities successful")
        return results
    
    def store_weather_data(self, records):
        """Store weather records in RDS"""
        if not records:
            self.logger.warning("No records to store")
            return 0
        
        self.logger.info("Storing data to RDS")
        
        conn = None
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            
            insert_query = '''
                INSERT INTO weather_observations 
                (city, timestamp, temperature, feels_like, humidity, 
                 pressure, wind_speed, weather_condition, weather_description,
                 data_quality_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (city, timestamp) DO NOTHING
            '''
            
            data = [
                (
                    r['city'], r['timestamp'], r['temperature'], r['feels_like'],
                    r['humidity'], r['pressure'], r['wind_speed'],
                    r['weather_condition'], r['weather_description'],
                    r['data_quality_score']
                )
                for r in records
            ]
            
            execute_batch(cursor, insert_query, data)
            conn.commit()
            
            inserted_count = cursor.rowcount
            self.logger.info(f"Successfully stored {inserted_count} records")
            
            cursor.close()
            return inserted_count
            
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Database error: {e}")
            return 0
            
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Unexpected error storing data: {e}")
            return 0
            
        finally:
            if conn:
                conn.close()
    
    def get_pipeline_stats(self):
        """Get quick pipeline statistics"""
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM weather_observations")
            total_records = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) 
                FROM weather_observations 
                WHERE timestamp > NOW() - INTERVAL '1 hour'
            """)
            recent_records = cursor.fetchone()[0]
            
            self.logger.info(f"Total records: {total_records:,} | Last hour: {recent_records}")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
    
    def run(self):
        """Execute complete pipeline"""
        start_time = time.time()
        self.logger.info("="*70)
        self.logger.info("PIPELINE EXECUTION STARTED")
        self.logger.info("="*70)
        
        try:
            # Collect data
            records = self.collect_all_weather()
            
            # Store data
            if records:
                stored = self.store_weather_data(records)
                
                if stored > 0:
                    self.get_pipeline_stats()
            
            execution_time = time.time() - start_time
            self.logger.info(f"Pipeline execution completed in {execution_time:.2f} seconds")
            self.logger.info("="*70)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {e}")
            self.logger.info("="*70)
            return False


if __name__ == "__main__":
    pipeline = WeatherPipeline()
    pipeline.run()

