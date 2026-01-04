"""
Data Classification Framework
Categorizes data by privacy sensitivity level
"""

from enum import Enum
from typing import Dict, List

class SensitivityLevel(Enum):
    """Data sensitivity classifications"""
    PUBLIC = "PUBLIC"                    # No privacy concerns
    INTERNAL = "INTERNAL"                # Internal use only
    CONFIDENTIAL = "CONFIDENTIAL"        # Limited access
    RESTRICTED_PII = "RESTRICTED_PII"    # Personal Identifiable Information
    SENSITIVE_PII = "SENSITIVE_PII"      # Highly sensitive PII

class DataClassification:
    """
    Data classification for weather pipeline
    Defines sensitivity levels and retention policies
    """
    
    # Field classifications for weather_observations table
    WEATHER_FIELDS = {
        'id': {
            'sensitivity': SensitivityLevel.INTERNAL,
            'description': 'System-generated identifier',
            'retention_days': None,  # Keep indefinitely
            'pii': False
        },
        'city': {
            'sensitivity': SensitivityLevel.PUBLIC,
            'description': 'City name - publicly available',
            'retention_days': None,  # Keep indefinitely
            'pii': False
        },
        'timestamp': {
            'sensitivity': SensitivityLevel.INTERNAL,
            'description': 'Collection timestamp',
            'retention_days': 365,  # 1 year retention
            'pii': False
        },
        'temperature': {
            'sensitivity': SensitivityLevel.PUBLIC,
            'description': 'Weather measurement - public data',
            'retention_days': 365,
            'pii': False
        },
        'feels_like': {
            'sensitivity': SensitivityLevel.PUBLIC,
            'description': 'Weather measurement - public data',
            'retention_days': 365,
            'pii': False
        },
        'humidity': {
            'sensitivity': SensitivityLevel.PUBLIC,
            'description': 'Weather measurement - public data',
            'retention_days': 365,
            'pii': False
        },
        'pressure': {
            'sensitivity': SensitivityLevel.PUBLIC,
            'description': 'Weather measurement - public data',
            'retention_days': 365,
            'pii': False
        },
        'wind_speed': {
            'sensitivity': SensitivityLevel.PUBLIC,
            'description': 'Weather measurement - public data',
            'retention_days': 365,
            'pii': False
        },
        'weather_condition': {
            'sensitivity': SensitivityLevel.PUBLIC,
            'description': 'Weather measurement - public data',
            'retention_days': 365,
            'pii': False
        },
        'weather_description': {
            'sensitivity': SensitivityLevel.PUBLIC,
            'description': 'Weather measurement - public data',
            'retention_days': 365,
            'pii': False
        },
        'data_quality_score': {
            'sensitivity': SensitivityLevel.INTERNAL,
            'description': 'Internal quality metric',
            'retention_days': 365,
            'pii': False
        },
        'created_at': {
            'sensitivity': SensitivityLevel.INTERNAL,
            'description': 'Record creation timestamp',
            'retention_days': 365,
            'pii': False
        }
    }
    
    # Quality metrics table classification
    QUALITY_METRICS_FIELDS = {
        'collection_timestamp': {
            'sensitivity': SensitivityLevel.INTERNAL,
            'description': 'Metrics timestamp',
            'retention_days': 90,  # 3 months for metrics
            'pii': False
        },
        'total_records': {
            'sensitivity': SensitivityLevel.INTERNAL,
            'description': 'Quality metric',
            'retention_days': 90,
            'pii': False
        },
        'avg_quality_score': {
            'sensitivity': SensitivityLevel.INTERNAL,
            'description': 'Quality metric',
            'retention_days': 90,
            'pii': False
        }
    }
    
    @classmethod
    def get_field_classification(cls, table: str, field: str) -> Dict:
        """
        Get classification for a specific field
        
        Args:
            table: Table name
            field: Field name
            
        Returns:
            Classification dict or None
        """
        if table == 'weather_observations':
            return cls.WEATHER_FIELDS.get(field)
        elif table == 'quality_metrics':
            return cls.QUALITY_METRICS_FIELDS.get(field)
        return None
    
    @classmethod
    def get_pii_fields(cls, table: str) -> List[str]:
        """
        Get list of PII fields for a table
        
        Args:
            table: Table name
            
        Returns:
            List of field names containing PII
        """
        fields_dict = None
        if table == 'weather_observations':
            fields_dict = cls.WEATHER_FIELDS
        elif table == 'quality_metrics':
            fields_dict = cls.QUALITY_METRICS_FIELDS
        
        if not fields_dict:
            return []
        
        return [
            field for field, info in fields_dict.items()
            if info.get('pii', False)
        ]
    
    @classmethod
    def get_retention_policy(cls, table: str) -> int:
        """
        Get retention policy for table (minimum retention across fields)
        
        Args:
            table: Table name
            
        Returns:
            Retention days (None = indefinite)
        """
        fields_dict = None
        if table == 'weather_observations':
            fields_dict = cls.WEATHER_FIELDS
        elif table == 'quality_metrics':
            fields_dict = cls.QUALITY_METRICS_FIELDS
        
        if not fields_dict:
            return None
        
        retention_days = [
            info['retention_days'] 
            for info in fields_dict.values() 
            if info.get('retention_days') is not None
        ]
        
        return min(retention_days) if retention_days else None

# Example usage
if __name__ == "__main__":
    # Show classification for weather data
    print("Weather Observations Classification:")
    print("=" * 60)
    
    for field, info in DataClassification.WEATHER_FIELDS.items():
        print(f"{field:25} | {info['sensitivity'].value:20} | "
              f"Retention: {info['retention_days'] or 'Indefinite':>10}")
    
    print("\n" + "=" * 60)
    print(f"PII Fields: {DataClassification.get_pii_fields('weather_observations')}")
    print(f"Table Retention: {DataClassification.get_retention_policy('weather_observations')} days")

