"""
PII Handling Utilities
Functions for tokenization, hashing, and anonymization of sensitive data
"""

import hashlib
import hmac
import os
from typing import Optional, Dict
import secrets
import json
from datetime import datetime

class PIIHandler:
    """
    Privacy-preserving transformations for PII data
    Supports hashing, tokenization, and anonymization
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize PII handler
        
        Args:
            secret_key: Secret key for HMAC operations (uses env var if not provided)
        """
        self.secret_key = secret_key or os.environ.get('PII_SECRET_KEY', 'default-dev-key-change-in-prod')
        self.token_map = {}  # In-memory token storage (use database/vault in production)
    
    def hash_pii(self, value: str, salt: Optional[str] = None) -> str:
        """
        One-way hash of PII value (irreversible)
        Use for: Email addresses, phone numbers, IP addresses
        
        Args:
            value: PII value to hash
            salt: Optional salt (generates random if not provided)
            
        Returns:
            Hex-encoded hash
            
        Example:
            >>> handler = PIIHandler()
            >>> handler.hash_pii("user@example.com")
            'a3b2c1d4e5f6...'
        """
        if not value:
            return None
        
        # Use provided salt or generate random
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Combine value and salt
        salted = f"{value}{salt}".encode('utf-8')
        
        # SHA-256 hash
        hashed = hashlib.sha256(salted).hexdigest()
        
        # Return hash with salt (needed for verification)
        return f"{salt}:{hashed}"
    
    def verify_hash(self, value: str, hashed: str) -> bool:
        """
        Verify a value matches a hash
        
        Args:
            value: Original value
            hashed: Hash to verify against
            
        Returns:
            True if match, False otherwise
        """
        if not value or not hashed or ':' not in hashed:
            return False
        
        # Extract salt and hash
        salt, original_hash = hashed.split(':', 1)
        
        # Hash the value with same salt
        salted = f"{value}{salt}".encode('utf-8')
        computed_hash = hashlib.sha256(salted).hexdigest()
        
        # Constant-time comparison
        return hmac.compare_digest(computed_hash, original_hash)
    
    def hmac_hash(self, value: str) -> str:
        """
        HMAC-based hash using secret key (keyed hash)
        More secure than plain hashing, consistent across system
        
        Args:
            value: PII value to hash
            
        Returns:
            Hex-encoded HMAC hash
        """
        if not value:
            return None
        
        return hmac.new(
            self.secret_key.encode('utf-8'),
            value.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def tokenize(self, value: str, table: str, field: str) -> str:
        """
        Reversible tokenization (pseudonymization)
        Use for: User IDs, session IDs, identifiers that may need to be reversed
        
        Args:
            value: PII value to tokenize
            table: Table name (for namespacing)
            field: Field name (for namespacing)
            
        Returns:
            Token (reversible to original value)
            
        Note: In production, store token_map in encrypted database or vault
        """
        if not value:
            return None
        
        # Create namespace for this field
        namespace = f"{table}.{field}"
        
        # Check if already tokenized
        lookup_key = f"{namespace}:{value}"
        if lookup_key in self.token_map:
            return self.token_map[lookup_key]
        
        # Generate new token
        token = f"tok_{secrets.token_urlsafe(16)}"
        
        # Store mapping (both directions)
        self.token_map[lookup_key] = token
        self.token_map[f"reverse:{token}"] = value
        
        return token
    
    def detokenize(self, token: str) -> Optional[str]:
        """
        Reverse a token to original value
        
        Args:
            token: Token to reverse
            
        Returns:
            Original value or None
        """
        if not token:
            return None
        
        return self.token_map.get(f"reverse:{token}")
    
    def generalize_location(self, city: str, state: str = None) -> str:
        """
        Generalize location to region (k-anonymity)
        Use for: Privacy-preserving location analytics
        
        Args:
            city: City name
            state: State (optional)
            
        Returns:
            Generalized region
        """
        # City to region mapping (example)
        region_map = {
            'San Diego': 'Southern California',
            'Los Angeles': 'Southern California',
            'San Francisco': 'Northern California',
            'Seattle': 'Pacific Northwest',
            'Portland': 'Pacific Northwest',
            'San Jose': 'Northern California',
            'Oakland': 'Northern California'
        }
        
        return region_map.get(city, 'Unknown Region')
    
    def mask_email(self, email: str) -> str:
        """
        Partially mask email address
        Use for: Displaying email to users while preserving some privacy
        
        Args:
            email: Email address
            
        Returns:
            Masked email (e.g., "u***@example.com")
        """
        if not email or '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        
        if len(local) <= 2:
            masked_local = local[0] + '*'
        else:
            masked_local = local[0] + '*' * (len(local) - 1)
        
        return f"{masked_local}@{domain}"
    
    def mask_ip(self, ip_address: str) -> str:
        """
        Mask IP address (preserve subnet, hide host)
        Use for: Analytics while protecting individual identity
        
        Args:
            ip_address: IPv4 address
            
        Returns:
            Masked IP (e.g., "192.168.1.0")
        """
        if not ip_address or '.' not in ip_address:
            return ip_address
        
        # Split into octets
        octets = ip_address.split('.')
        
        # Mask last octet
        octets[-1] = '0'
        
        return '.'.join(octets)
    
    def add_noise(self, value: float, noise_percent: float = 0.05) -> float:
        """
        Add differential privacy noise to numeric value
        Use for: Privacy-preserving analytics
        
        Args:
            value: Original numeric value
            noise_percent: Noise as percentage (default 5%)
            
        Returns:
            Value with added noise
        """
        import random
        
        # Calculate noise range
        noise_range = value * noise_percent
        
        # Add random noise
        noise = random.uniform(-noise_range, noise_range)
        
        return value + noise
    
    def k_anonymize_age(self, age: int, k: int = 5) -> str:
        """
        K-anonymize age into buckets
        Use for: Preventing re-identification via age
        
        Args:
            age: Age in years
            k: Minimum group size
            
        Returns:
            Age range string
        """
        # Define age buckets
        if age < 18:
            return "0-17"
        elif age < 25:
            return "18-24"
        elif age < 35:
            return "25-34"
        elif age < 45:
            return "35-44"
        elif age < 55:
            return "45-54"
        elif age < 65:
            return "55-64"
        else:
            return "65+"
    
    def generate_audit_entry(self, operation: str, field: str, 
                            original_value: Optional[str] = None,
                            transformed_value: Optional[str] = None) -> Dict:
        """
        Generate audit log entry for PII operations
        
        Args:
            operation: Operation type (hash, tokenize, etc.)
            field: Field name
            original_value: Original value (optional, for logging)
            transformed_value: Transformed value
            
        Returns:
            Audit entry dict
        """
        return {
            'operation': operation,
            'field': field,
            'timestamp': datetime.utcnow().isoformat(),
            'original_present': original_value is not None,
            'transformed_present': transformed_value is not None,
            'reversible': operation == 'tokenize'
        }


# Example usage and testing
if __name__ == "__main__":
    print("PII Handler Examples")
    print("=" * 60)
    
    handler = PIIHandler()
    
    # 1. Hashing (irreversible)
    print("\n1. ONE-WAY HASHING:")
    email = "user@example.com"
    hashed = handler.hash_pii(email)
    print(f"Original: {email}")
    print(f"Hashed:   {hashed[:50]}...")
    print(f"Verify:   {handler.verify_hash(email, hashed)}")
    print(f"Verify wrong: {handler.verify_hash('wrong@email.com', hashed)}")
    
    # 2. HMAC hashing
    print("\n2. HMAC HASHING (keyed):")
    hmac_hash = handler.hmac_hash(email)
    print(f"Original: {email}")
    print(f"HMAC:     {hmac_hash}")
    
    # 3. Tokenization (reversible)
    print("\n3. TOKENIZATION (reversible):")
    user_id = "user_12345"
    token = handler.tokenize(user_id, 'users', 'user_id')
    detokenized = handler.detokenize(token)
    print(f"Original:     {user_id}")
    print(f"Token:        {token}")
    print(f"Detokenized:  {detokenized}")
    
    # 4. Location generalization
    print("\n4. LOCATION GENERALIZATION:")
    city = "San Diego"
    region = handler.generalize_location(city)
    print(f"City:   {city}")
    print(f"Region: {region}")
    
    # 5. Email masking
    print("\n5. EMAIL MASKING:")
    masked = handler.mask_email(email)
    print(f"Original: {email}")
    print(f"Masked:   {masked}")
    
    # 6. IP masking
    print("\n6. IP ADDRESS MASKING:")
    ip = "192.168.1.42"
    masked_ip = handler.mask_ip(ip)
    print(f"Original: {ip}")
    print(f"Masked:   {masked_ip}")
    
    # 7. Differential privacy
    print("\n7. DIFFERENTIAL PRIVACY (noise):")
    temperature = 72.5
    noisy = handler.add_noise(temperature, noise_percent=0.1)
    print(f"Original: {temperature}°F")
    print(f"Noisy:    {noisy:.2f}°F")
    
    # 8. K-anonymity
    print("\n8. K-ANONYMITY (age buckets):")
    age = 32
    bucket = handler.k_anonymize_age(age)
    print(f"Age:    {age}")
    print(f"Bucket: {bucket}")
    
    print("\n" + "=" * 60)
    print("✓ All PII handling examples complete")

