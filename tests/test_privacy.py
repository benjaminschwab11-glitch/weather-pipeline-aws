"""
Unit tests for privacy handling functions
"""

import pytest
import sys
import os

# Add privacy module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from privacy.pii_handlers import PIIHandler
from privacy.data_classification import DataClassification, SensitivityLevel


class TestPIIHandler:
    """Test PII handling functions"""
    
    @pytest.fixture
    def handler(self):
        """Create PIIHandler instance for testing"""
        return PIIHandler(secret_key='test-secret-key')
    
    def test_hash_pii_returns_hash(self, handler):
        """Test that hashing returns a hash string"""
        email = "test@example.com"
        hashed = handler.hash_pii(email)
        
        assert hashed is not None
        assert ':' in hashed  # Contains salt and hash
        assert len(hashed) > 64  # SHA-256 is 64 chars + salt
    
    def test_hash_pii_different_values_different_hashes(self, handler):
        """Test that different values produce different hashes"""
        hash1 = handler.hash_pii("test1@example.com")
        hash2 = handler.hash_pii("test2@example.com")
        
        assert hash1 != hash2
    
    def test_verify_hash_correct_value(self, handler):
        """Test hash verification with correct value"""
        value = "test@example.com"
        hashed = handler.hash_pii(value)
        
        assert handler.verify_hash(value, hashed) is True
    
    def test_verify_hash_wrong_value(self, handler):
        """Test hash verification with wrong value"""
        value = "test@example.com"
        hashed = handler.hash_pii(value)
        
        assert handler.verify_hash("wrong@example.com", hashed) is False
    
    def test_hmac_hash_consistent(self, handler):
        """Test that HMAC hash is consistent for same value"""
        value = "test@example.com"
        hash1 = handler.hmac_hash(value)
        hash2 = handler.hmac_hash(value)
        
        assert hash1 == hash2
    
    def test_hmac_hash_different_keys(self):
        """Test that different keys produce different hashes"""
        value = "test@example.com"
        handler1 = PIIHandler(secret_key='key1')
        handler2 = PIIHandler(secret_key='key2')
        
        hash1 = handler1.hmac_hash(value)
        hash2 = handler2.hmac_hash(value)
        
        assert hash1 != hash2
    
    def test_tokenize_returns_token(self, handler):
        """Test that tokenization returns a token"""
        user_id = "user_12345"
        token = handler.tokenize(user_id, 'users', 'user_id')
        
        assert token is not None
        assert token.startswith('tok_')
        assert len(token) > 10
    
    def test_tokenize_reversible(self, handler):
        """Test that tokenization is reversible"""
        user_id = "user_12345"
        token = handler.tokenize(user_id, 'users', 'user_id')
        detokenized = handler.detokenize(token)
        
        assert detokenized == user_id
    
    def test_tokenize_same_value_same_token(self, handler):
        """Test that same value gets same token"""
        user_id = "user_12345"
        token1 = handler.tokenize(user_id, 'users', 'user_id')
        token2 = handler.tokenize(user_id, 'users', 'user_id')
        
        assert token1 == token2
    
    def test_generalize_location_known_city(self, handler):
        """Test location generalization for known cities"""
        assert handler.generalize_location('San Diego') == 'Southern California'
        assert handler.generalize_location('Seattle') == 'Pacific Northwest'
        assert handler.generalize_location('San Francisco') == 'Northern California'
    
    def test_generalize_location_unknown_city(self, handler):
        """Test location generalization for unknown city"""
        assert handler.generalize_location('Unknown City') == 'Unknown Region'
    
    def test_mask_email_preserves_domain(self, handler):
        """Test that email masking preserves domain"""
        email = "user@example.com"
        masked = handler.mask_email(email)
        
        assert '@example.com' in masked
        assert 'user' not in masked
        assert '*' in masked
    
    def test_mask_email_short_local(self, handler):
        """Test email masking with short local part"""
        email = "ab@example.com"
        masked = handler.mask_email(email)
        
        assert masked == 'a*@example.com'
    
    def test_mask_ip_preserves_subnet(self, handler):
        """Test that IP masking preserves subnet"""
        ip = "192.168.1.42"
        masked = handler.mask_ip(ip)
        
        assert masked == "192.168.1.0"
        assert masked.startswith("192.168.1")
    
    def test_add_noise_changes_value(self, handler):
        """Test that noise changes the value"""
        value = 100.0
        noisy = handler.add_noise(value, noise_percent=0.1)
        
        assert noisy != value
        # Should be within 10% of original
        assert 90.0 <= noisy <= 110.0
    
    def test_k_anonymize_age_buckets(self, handler):
        """Test age k-anonymization buckets"""
        assert handler.k_anonymize_age(15) == "0-17"
        assert handler.k_anonymize_age(20) == "18-24"
        assert handler.k_anonymize_age(30) == "25-34"
        assert handler.k_anonymize_age(40) == "35-44"
        assert handler.k_anonymize_age(50) == "45-54"
        assert handler.k_anonymize_age(60) == "55-64"
        assert handler.k_anonymize_age(70) == "65+"
    
    def test_hash_pii_null_value(self, handler):
        """Test hashing with null/empty value"""
        assert handler.hash_pii(None) is None
        assert handler.hash_pii("") is None
    
    def test_tokenize_null_value(self, handler):
        """Test tokenization with null/empty value"""
        assert handler.tokenize(None, 'users', 'id') is None
        assert handler.tokenize("", 'users', 'id') is None


class TestDataClassification:
    """Test data classification framework"""
    
    def test_get_field_classification_weather(self):
        """Test getting classification for weather fields"""
        classification = DataClassification.get_field_classification(
            'weather_observations', 
            'temperature'
        )
        
        assert classification is not None
        assert classification['sensitivity'] == SensitivityLevel.PUBLIC
        assert classification['pii'] is False
    
    def test_get_field_classification_unknown_field(self):
        """Test classification for unknown field"""
        classification = DataClassification.get_field_classification(
            'weather_observations',
            'unknown_field'
        )
        
        assert classification is None
    
    def test_get_pii_fields_weather(self):
        """Test getting PII fields from weather table"""
        pii_fields = DataClassification.get_pii_fields('weather_observations')
        
        # Weather data has no PII
        assert isinstance(pii_fields, list)
        assert len(pii_fields) == 0
    
    def test_get_retention_policy_weather(self):
        """Test retention policy for weather table"""
        retention = DataClassification.get_retention_policy('weather_observations')
        
        assert retention == 365  # 365 days
    
    def test_get_retention_policy_quality_metrics(self):
        """Test retention policy for quality metrics"""
        retention = DataClassification.get_retention_policy('quality_metrics')
        
        assert retention == 90  # 90 days
    
    def test_sensitivity_levels_defined(self):
        """Test that all sensitivity levels are defined"""
        levels = [
            SensitivityLevel.PUBLIC,
            SensitivityLevel.INTERNAL,
            SensitivityLevel.CONFIDENTIAL,
            SensitivityLevel.RESTRICTED_PII,
            SensitivityLevel.SENSITIVE_PII
        ]
        
        assert len(levels) == 5
        assert all(isinstance(level, SensitivityLevel) for level in levels)


class TestPrivacyIntegration:
    """Integration tests for privacy framework"""
    
    def test_end_to_end_anonymization(self):
        """Test complete anonymization workflow"""
        handler = PIIHandler()
        
        # Simulate user data
        user_email = "john.doe@example.com"
        user_ip = "192.168.1.42"
        user_age = 32
        city = "San Diego"
        
        # Apply privacy transformations
        hashed_email = handler.hash_pii(user_email)
        masked_ip = handler.mask_ip(user_ip)
        age_bucket = handler.k_anonymize_age(user_age)
        region = handler.generalize_location(city)
        
        # Verify transformations
        assert hashed_email != user_email
        assert masked_ip == "192.168.1.0"
        assert age_bucket == "25-34"
        assert region == "Southern California"
        
        # Verify irreversibility
        assert user_email not in hashed_email
        assert "42" not in masked_ip
    
    def test_privacy_preserving_analytics(self):
        """Test privacy-preserving analytics workflow"""
        handler = PIIHandler()
        
        # Simulate temperature data
        temperatures = [72.5, 68.3, 75.1, 70.8, 73.2]
        
        # Add differential privacy noise
        noisy_temps = [handler.add_noise(temp, 0.05) for temp in temperatures]
        
        # Verify noise added
        for original, noisy in zip(temperatures, noisy_temps):
            assert original != noisy
            # Within 5% range
            assert abs(noisy - original) <= original * 0.05
        
        # Verify statistical properties preserved (roughly)
        original_avg = sum(temperatures) / len(temperatures)
        noisy_avg = sum(noisy_temps) / len(noisy_temps)
        
        # Averages should be close (within 10%)
        assert abs(noisy_avg - original_avg) <= original_avg * 0.1

