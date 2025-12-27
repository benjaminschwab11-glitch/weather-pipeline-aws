"""
Pytest configuration and shared fixtures
"""

import pytest
from datetime import datetime


@pytest.fixture
def sample_weather_data():
    """Sample weather data from API"""
    return {
        'main': {
            'temp': 65.5,
            'feels_like': 63.2,
            'humidity': 72,
            'pressure': 1013
        },
        'wind': {
            'speed': 8.5
        },
        'weather': [
            {
                'main': 'Clouds',
                'description': 'scattered clouds'
            }
        ]
    }


@pytest.fixture
def sample_weather_record():
    """Sample processed weather record"""
    return {
        'city': 'San Diego',
        'timestamp': datetime(2024, 12, 25, 12, 0, 0),
        'temperature': 65.5,
        'feels_like': 63.2,
        'humidity': 72,
        'pressure': 1013,
        'wind_speed': 8.5,
        'weather_condition': 'Clouds',
        'weather_description': 'scattered clouds'
    }


@pytest.fixture
def invalid_weather_data():
    """Invalid weather data for testing edge cases"""
    return {
        'city': 'TestCity',
        'timestamp': datetime(2024, 12, 25, 12, 0, 0),
        'temperature': 200.0,  # Invalid - too high
        'feels_like': 195.0,
        'humidity': 150,  # Invalid - over 100%
        'pressure': 500,  # Invalid - too low
        'wind_speed': -5.0,  # Invalid - negative
        'weather_condition': 'Test',
        'weather_description': 'test conditions'
    }

