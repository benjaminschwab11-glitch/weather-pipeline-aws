"""
API Gateway Lambda Handler for Weather Data
Provides REST API endpoints to query weather data
"""

import json
import os
import psycopg2
from datetime import datetime, timedelta
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal types"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DecimalEncoder, self).default(obj)

class WeatherAPI:
    """Weather data API handler"""
    
    def __init__(self):
        self.db_params = {
            'host': os.environ['RDS_ENDPOINT'],
            'database': os.environ['RDS_DATABASE'],
            'user': os.environ['RDS_USERNAME'],
            'password': os.environ['RDS_PASSWORD'],
            'port': int(os.environ.get('RDS_PORT', '5432'))
        }
    
    def get_db_connection(self):
        """Create database connection"""
        return psycopg2.connect(**self.db_params, connect_timeout=5)
    
    def get_current_weather(self, city=None):
        """
        Get most recent weather data
        
        Args:
            city: Optional city filter
            
        Returns:
            list: Weather records
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            if city:
                # Get latest for specific city
                query = '''
                    SELECT city, timestamp, temperature, feels_like, humidity,
                           pressure, wind_speed, weather_condition, 
                           weather_description, data_quality_score
                    FROM weather_observations
                    WHERE city = %s
                    ORDER BY timestamp DESC
                    LIMIT 1
                '''
                cursor.execute(query, (city,))
            else:
                # Get latest for each city
                query = '''
                    SELECT DISTINCT ON (city)
                        city, timestamp, temperature, feels_like, humidity,
                        pressure, wind_speed, weather_condition, 
                        weather_description, data_quality_score
                    FROM weather_observations
                    ORDER BY city, timestamp DESC
                '''
                cursor.execute(query)
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
            
        finally:
            cursor.close()
            conn.close()
    
    def get_weather_history(self, city=None, hours=24, limit=100):
        """
        Get historical weather data
        
        Args:
            city: Optional city filter
            hours: Hours of history (default 24)
            limit: Max records to return (default 100)
            
        Returns:
            list: Weather records
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            if city:
                query = '''
                    SELECT city, timestamp, temperature, feels_like, humidity,
                           pressure, wind_speed, weather_condition, 
                           weather_description, data_quality_score
                    FROM weather_observations
                    WHERE city = %s 
                      AND timestamp >= NOW() - INTERVAL '%s hours'
                    ORDER BY timestamp DESC
                    LIMIT %s
                '''
                cursor.execute(query, (city, hours, limit))
            else:
                query = '''
                    SELECT city, timestamp, temperature, feels_like, humidity,
                           pressure, wind_speed, weather_condition, 
                           weather_description, data_quality_score
                    FROM weather_observations
                    WHERE timestamp >= NOW() - INTERVAL '%s hours'
                    ORDER BY timestamp DESC
                    LIMIT %s
                '''
                cursor.execute(query, (hours, limit))
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
            
        finally:
            cursor.close()
            conn.close()
    
    def get_quality_metrics(self, hours=24):
        """
        Get quality metrics
        
        Args:
            hours: Hours of history (default 24)
            
        Returns:
            list: Quality metrics
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = '''
                SELECT collection_timestamp, total_records,
                       perfect_quality_count, degraded_quality_count,
                       failed_quality_count, avg_quality_score,
                       min_quality_score, max_quality_score,
                       temperature_failures, humidity_failures,
                       pressure_failures, wind_speed_failures
                FROM quality_metrics
                WHERE collection_timestamp >= NOW() - INTERVAL '%s hours'
                ORDER BY collection_timestamp DESC
            '''
            cursor.execute(query, (hours,))
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
            
        finally:
            cursor.close()
            conn.close()

def lambda_handler(event, context):
    """
    API Gateway Lambda handler
    Routes requests to appropriate methods
    """
    print(f"Event: {json.dumps(event)}")
    
    api = WeatherAPI()
    
    # Extract request details
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    query_params = event.get('queryStringParameters') or {}
    path_params = event.get('pathParameters') or {}
    
    try:
        # Route requests
        if path == '/weather' and http_method == 'GET':
            # Get current weather (all cities or filtered)
            city = query_params.get('city')
            data = api.get_current_weather(city)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'count': len(data),
                    'data': data
                }, cls=DecimalEncoder)
            }
        
        elif path == '/weather/history' and http_method == 'GET':
            # Get historical weather data
            city = query_params.get('city')
            hours = int(query_params.get('hours', 24))
            limit = int(query_params.get('limit', 100))
            
            data = api.get_weather_history(city, hours, limit)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'count': len(data),
                    'hours': hours,
                    'data': data
                }, cls=DecimalEncoder)
            }
        
        elif path == '/quality' and http_method == 'GET':
            # Get quality metrics
            hours = int(query_params.get('hours', 24))
            data = api.get_quality_metrics(hours)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'count': len(data),
                    'hours': hours,
                    'data': data
                }, cls=DecimalEncoder)
            }
        
        else:
            # Unknown endpoint
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Not Found',
                    'message': f'Endpoint {path} not found'
                })
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            })
        }

# For local testing
if __name__ == "__main__":
    import sys
    import os
    
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from dotenv import load_dotenv
    
    # Load .env from project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_root, '.env')
    load_dotenv(env_path)
    
    print(f"Loaded .env from: {env_path}")
    print(f"RDS_ENDPOINT: {os.environ.get('RDS_ENDPOINT', 'NOT FOUND')}")
    
    # Test current weather
    test_event = {
        'httpMethod': 'GET',
        'path': '/weather',
        'queryStringParameters': None
    }
    
    result = lambda_handler(test_event, None)
    print("\nResult:")
    print(json.dumps(json.loads(result['body']), indent=2))

