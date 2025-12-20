"""
AWS Lambda Handler for Weather Pipeline
Serverless version optimized for Lambda execution
FIXED: Uses single timestamp per collection run to avoid duplicate conflicts
"""

import json
import os
import boto3
import requests
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
import time

# Initialize CloudWatch client for custom metrics
cloudwatch = boto3.client('cloudwatch')

class WeatherPipelineLambda:
    """
    Lambda-optimized weather pipeline
    """
    
    def __init__(self):
        # API Configuration from Lambda environment variables
        self.api_key = os.environ['WEATHER_API_KEY']
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.cities = os.environ.get('CITIES', 'San Diego,Los Angeles,San Francisco,Seattle,Portland').split(',')
        
        # Database Configuration from Lambda environment variables
        self.db_params = {
            'host': os.environ['RDS_ENDPOINT'],
            'database': os.environ['RDS_DATABASE'],
            'user': os.environ['RDS_USERNAME'],
            'password': os.environ['RDS_PASSWORD'],
            'port': int(os.environ.get('RDS_PORT', '5432'))
        }
        
        print(f"Pipeline initialized for {len(self.cities)} cities")
    
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
            print(f"WARNING: Quality issues for {record['city']}: {', '.join(issues)} (score: {final_score:.2f})")
        
        return final_score
    
    def fetch_weather(self, city, collection_timestamp):
        """Fetch weather data from API with shared timestamp"""
        params = {
            'q': city.strip(),
            'appid': self.api_key,
            'units': 'imperial'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            record = {
                'city': city.strip(),
                'timestamp': collection_timestamp,  # FIXED: Use shared timestamp
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'weather_condition': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description']
            }
            
            record['data_quality_score'] = self.validate_record(record)
            
            print(f"✓ Collected {city}: {record['temperature']:.1f}°F, {record['weather_description']}")
            return record
            
        except requests.exceptions.Timeout:
            print(f"✗ Timeout fetching {city}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ API error for {city}: {e}")
            return None
        except KeyError as e:
            print(f"✗ Unexpected data structure for {city}: missing {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error for {city}: {e}")
            return None
    
    def collect_all_weather(self):
        """Collect weather data for all cities with single timestamp"""
        print(f"Starting collection for {len(self.cities)} cities")
        
        # FIXED: Create single timestamp for this entire collection run
        collection_timestamp = datetime.utcnow()
        print(f"Collection timestamp: {collection_timestamp.isoformat()}")
        
        results = []
        for city in self.cities:
            record = self.fetch_weather(city, collection_timestamp)
            if record:
                results.append(record)
            time.sleep(0.5)  # Rate limiting
        
        print(f"Collection complete: {len(results)}/{len(self.cities)} successful")
        return results
    
    def store_weather_data(self, records):
        """Store weather records in RDS"""
        if not records:
            print("WARNING: No records to store")
            return 0
        
        print("Connecting to RDS...")
        
        conn = None
        try:
            conn = psycopg2.connect(**self.db_params, connect_timeout=5)
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
            
            # cursor.rowcount is unreliable with execute_batch, use len(data) instead
            inserted_count = len(data)
            print(f"✓ Attempted to store {inserted_count} records in RDS")
            
            # Verify actual inserts
            cursor.execute("SELECT COUNT(*) FROM weather_observations WHERE timestamp = %s", (data[0][1],))
            actual_count = cursor.fetchone()[0]
            print(f"✓ Verified {actual_count} records in database with this timestamp")

            cursor.close()
            return inserted_count
            
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"✗ Database error: {e}")
            raise  # Re-raise to trigger Lambda retry
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"✗ Unexpected error: {e}")
            raise
            
        finally:
            if conn:
                conn.close()
    
    def publish_metrics(self, records_collected, execution_time_ms, records_stored):
        """Publish custom metrics to CloudWatch"""
        try:
            cloudwatch.put_metric_data(
                Namespace='WeatherPipeline',
                MetricData=[
                    {
                        'MetricName': 'RecordsCollected',
                        'Value': records_collected,
                        'Unit': 'Count',
                        'Timestamp': datetime.utcnow()
                    },
                    {
                        'MetricName': 'RecordsStored',
                        'Value': records_stored,
                        'Unit': 'Count',
                        'Timestamp': datetime.utcnow()
                    },
                    {
                        'MetricName': 'ExecutionTime',
                        'Value': execution_time_ms,
                        'Unit': 'Milliseconds',
                        'Timestamp': datetime.utcnow()
                    }
                ]
            )
            print(f"✓ Published CloudWatch metrics")
        except Exception as e:
            print(f"WARNING: Failed to publish metrics: {e}")
            # Don't fail the whole pipeline if metrics fail
    
    def run(self):
        """Execute pipeline"""
        start_time = time.time()
        
        print("="*70)
        print("LAMBDA WEATHER PIPELINE EXECUTION")
        print("="*70)
        
        # Collect data
        records = self.collect_all_weather()
        
        # Store data
        stored = 0
        if records:
            stored = self.store_weather_data(records)
        
        # Calculate execution time
        execution_time_ms = (time.time() - start_time) * 1000
        
        # Publish metrics
        self.publish_metrics(len(records), execution_time_ms, stored)
        
        print(f"Execution completed in {execution_time_ms:.0f}ms")
        print("="*70)
        
        return {
            'records_collected': len(records),
            'records_stored': stored,
            'execution_time_ms': execution_time_ms
        }


def lambda_handler(event, context):
    """
    AWS Lambda handler function
    This is the entry point that Lambda calls
    """
    print(f"Lambda invoked at {datetime.utcnow().isoformat()}")
    print(f"Event: {json.dumps(event)}")
    
    try:
        pipeline = WeatherPipelineLambda()
        result = pipeline.run()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Weather pipeline executed successfully',
                'result': result
            })
        }
        
    except Exception as e:
        print(f"CRITICAL ERROR: Pipeline failed: {e}")
        
        # Return error but with 200 status so Lambda doesn't retry
        # (We'll handle retries via EventBridge schedule)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Weather pipeline failed',
                'error': str(e)
            })
        }


# For local testing
if __name__ == "__main__":
    # Simulate Lambda invocation locally
    print("LOCAL TEST MODE")
    print("Loading environment from .env file...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Simulate Lambda event and context
    test_event = {}
    test_context = type('obj', (object,), {
        'function_name': 'weather-pipeline-local-test',
        'memory_limit_in_mb': 128,
        'invoked_function_arn': 'arn:aws:lambda:local:test',
        'aws_request_id': 'local-test-id'
    })
    
    result = lambda_handler(test_event, test_context)
    print(f"\nResult: {json.dumps(result, indent=2)}")

