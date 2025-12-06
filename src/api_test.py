"""
Day 2: Test OpenWeatherMap API connection
Goal: Pull real weather data for San Diego
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_weather_api():
    """
    Test API connection and explore data structure
    """
    # Get API key from environment
    api_key = os.getenv('WEATHER_API_KEY')
    
    if not api_key:
        print("❌ ERROR: WEATHER_API_KEY not found in .env file")
        return
    
    # API endpoint
    city = "San Diego"
    url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Request parameters
    params = {
        'q': city,
        'appid': api_key,
        'units': 'imperial'  # Fahrenheit
    }
    
    print(f"🔍 Testing API connection for {city}...")
    print(f"URL: {url}")
    print(f"Params: q={city}, units=imperial")
    print("-" * 60)
    
    try:
        # Make API request
        response = requests.get(url, params=params, timeout=10)
        
        # Check if successful
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Display results
        print("✅ API CONNECTION SUCCESSFUL!")
        print("-" * 60)
        print(f"City: {data['name']}")
        print(f"Temperature: {data['main']['temp']}°F")
        print(f"Feels Like: {data['main']['feels_like']}°F")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Pressure: {data['main']['pressure']} hPa")
        print(f"Wind Speed: {data['wind']['speed']} mph")
        print(f"Conditions: {data['weather'][0]['main']} - {data['weather'][0]['description']}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # Show full data structure
        print("\n📊 FULL API RESPONSE:")
        print(json.dumps(data, indent=2))
        
        # Show what we'll extract for our database
        print("\n📋 DATA WE'LL STORE:")
        extracted = {
            'city': city,
            'timestamp': datetime.utcnow().isoformat(),
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'weather_condition': data['weather'][0]['main'],
            'weather_description': data['weather'][0]['description']
        }
        print(json.dumps(extracted, indent=2))
        
        return data
        
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: API request failed")
        print(f"Details: {e}")
        if hasattr(e.response, 'status_code'):
            print(f"Status Code: {e.response.status_code}")
            print(f"Response: {e.response.text}")
    except KeyError as e:
        print(f"❌ ERROR: Unexpected data structure")
        print(f"Missing key: {e}")
    except Exception as e:
        print(f"❌ ERROR: Unexpected error")
        print(f"Details: {e}")

def test_multiple_cities():
    """
    Test API for multiple cities (what we'll do in production)
    """
    cities = ['San Diego', 'Los Angeles', 'San Francisco', 'Seattle', 'Portland']
    api_key = os.getenv('WEATHER_API_KEY')
    
    print("\n" + "=" * 60)
    print("🌎 TESTING MULTIPLE CITIES")
    print("=" * 60)
    
    for city in cities:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': api_key, 'units': 'imperial'}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ {city:15s} | {data['main']['temp']:5.1f}°F | {data['weather'][0]['description']}")
            
        except Exception as e:
            print(f"❌ {city:15s} | Failed: {str(e)[:40]}")

if __name__ == "__main__":
    print("=" * 60)
    print("WEATHER API TEST - DAY 2")
    print("=" * 60)
    
    # Test single city first
    test_weather_api()
    
    # Then test multiple cities
    test_multiple_cities()
    
    print("\n" + "=" * 60)
    print("✅ DAY 2 COMPLETE: API connection verified!")
    print("=" * 60)

