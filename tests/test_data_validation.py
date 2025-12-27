"""
Unit tests for data validation logic
"""

import pytest
from datetime import datetime


class TestDataValidation:
    """Test data quality validation"""
    
    def validate_record(self, record):
        """
        Data quality validation
        (Extracted from Lambda function for testing)
        """
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
        
        return max(score, 0.0), issues
    
    def test_valid_weather_data(self, sample_weather_record):
        """Test that valid data gets perfect score"""
        score, issues = self.validate_record(sample_weather_record)
        
        assert score == 1.0
        assert len(issues) == 0
    
    def test_invalid_temperature(self):
        """Test temperature out of range detection"""
        record = {
            'temperature': 200.0,  # Too high
            'humidity': 50,
            'pressure': 1000,
            'wind_speed': 10.0
        }
        
        score, issues = self.validate_record(record)
        
        assert score == 0.7  # 1.0 - 0.3
        assert len(issues) == 1
        assert 'Temperature' in issues[0]
    
    def test_invalid_humidity(self):
        """Test humidity out of range detection"""
        record = {
            'temperature': 70.0,
            'humidity': 150,  # Over 100%
            'pressure': 1000,
            'wind_speed': 10.0
        }
        
        score, issues = self.validate_record(record)
        
        assert score == 0.7  # 1.0 - 0.3
        assert len(issues) == 1
        assert 'Humidity' in issues[0]
    
    def test_invalid_pressure(self):
        """Test pressure out of range detection"""
        record = {
            'temperature': 70.0,
            'humidity': 50,
            'pressure': 500,  # Too low
            'wind_speed': 10.0
        }
        
        score, issues = self.validate_record(record)
        
        assert score == 0.7
        assert 'Pressure' in issues[0]
    
    def test_negative_wind_speed(self):
        """Test negative wind speed detection"""
        record = {
            'temperature': 70.0,
            'humidity': 50,
            'pressure': 1000,
            'wind_speed': -5.0  # Negative
        }
        
        score, issues = self.validate_record(record)
        
        assert score == 0.9  # 1.0 - 0.1
        assert 'Wind speed' in issues[0]
    
    def test_multiple_invalid_fields(self, invalid_weather_data):
        """Test multiple validation failures"""
        score, issues = self.validate_record(invalid_weather_data)
        
        assert score == 0.0  # Maximum penalty
        assert len(issues) == 4  # All fields invalid
    
    def test_score_never_negative(self):
        """Test that score is capped at 0.0"""
        record = {
            'temperature': 200.0,
            'humidity': 150,
            'pressure': 500,
            'wind_speed': -10.0
        }
        
        score, issues = self.validate_record(record)
        
        assert score >= 0.0
        assert score <= 1.0
    
    def test_boundary_values(self):
        """Test boundary conditions"""
        # Test minimum valid values
        record = {
            'temperature': -50.0,  # Min valid
            'humidity': 0,  # Min valid
            'pressure': 900,  # Min valid
            'wind_speed': 0.0  # Min valid
        }
        
        score, issues = self.validate_record(record)
        assert score == 1.0
        
        # Test maximum valid values
        record = {
            'temperature': 150.0,  # Max valid
            'humidity': 100,  # Max valid
            'pressure': 1100,  # Max valid
            'wind_speed': 200.0  # Max valid
        }
        
        score, issues = self.validate_record(record)
        assert score == 1.0

