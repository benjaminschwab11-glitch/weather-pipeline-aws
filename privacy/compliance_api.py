"""
GDPR/CCPA Compliance API
Handles Data Subject Access Requests and Right to be Forgotten
"""

import psycopg2
from typing import Dict, List, Optional
from datetime import datetime
import json
import uuid


class ComplianceAPI:
    """
    Compliance operations for GDPR/CCPA
    """
    
    def __init__(self, db_params: Dict):
        """
        Initialize compliance API
        
        Args:
            db_params: Database connection parameters
        """
        self.db_params = db_params
    
    def get_db_connection(self):
        """Create database connection"""
        return psycopg2.connect(**self.db_params, connect_timeout=5)
    
    def record_consent(self, user_id: str, consent_type: str, 
                      granted: bool, version: str = '1.0',
                      ip_address: Optional[str] = None) -> int:
        """
        Record user consent
        
        Args:
            user_id: User identifier
            consent_type: Type of consent (e.g., 'MARKETING', 'ANALYTICS', 'DATA_PROCESSING')
            granted: Whether consent was granted
            version: Consent version
            ip_address: User's IP address
            
        Returns:
            Consent ID
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT record_user_consent(%s, %s, %s, %s, %s)",
                (user_id, consent_type, granted, version, ip_address)
            )
            
            consent_id = cursor.fetchone()[0]
            conn.commit()
            
            return consent_id
            
        finally:
            cursor.close()
            conn.close()
    
    def get_user_consents(self, user_id: str) -> List[Dict]:
        """
        Get all consents for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of consent records
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = '''
                SELECT 
                    consent_type,
                    consent_granted,
                    consent_timestamp,
                    consent_version,
                    consent_status
                FROM active_user_consents
                WHERE user_id = %s
                ORDER BY consent_timestamp DESC
            '''
            
            cursor.execute(query, (user_id,))
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
            
        finally:
            cursor.close()
            conn.close()
    
    def create_dsar_request(self, user_id: str, request_type: str,
                           requester_email: Optional[str] = None) -> str:
        """
        Create Data Subject Access Request
        
        Args:
            user_id: User identifier
            request_type: 'ACCESS', 'DELETION', 'RECTIFICATION', 'PORTABILITY'
            requester_email: Email address of requester
            
        Returns:
            Request ID (UUID)
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT create_dsar_request(%s, %s, %s)",
                (user_id, request_type, requester_email)
            )
            
            request_id = cursor.fetchone()[0]
            conn.commit()
            
            return str(request_id)
            
        finally:
            cursor.close()
            conn.close()
    
    def get_dsar_status(self, request_id: str) -> Optional[Dict]:
        """
        Get status of DSAR request
        
        Args:
            request_id: Request ID (UUID)
            
        Returns:
            Request status dict or None
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = '''
                SELECT 
                    request_id,
                    user_id,
                    request_type,
                    request_status,
                    request_timestamp,
                    completed_timestamp,
                    requester_email
                FROM data_subject_requests
                WHERE request_id = %s
            '''
            
            cursor.execute(query, (request_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
            
        finally:
            cursor.close()
            conn.close()
    
    def export_user_data(self, user_id: str) -> Dict:
        """
        Export all data for a user (DSAR - Data Portability)
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary containing all user data
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # In a real system, this would collect data from all tables
            # For weather pipeline (no user data yet), return structure
            
            user_data = {
                'user_id': user_id,
                'export_timestamp': datetime.utcnow().isoformat(),
                'data_categories': {
                    'consents': [],
                    'dsar_requests': [],
                    'weather_preferences': []  # Future: if user has preferences
                }
            }
            
            # Get consents
            cursor.execute('''
                SELECT 
                    consent_type,
                    consent_granted,
                    consent_timestamp,
                    consent_version
                FROM user_consent
                WHERE user_id = %s
                ORDER BY consent_timestamp DESC
            ''', (user_id,))
            
            for row in cursor.fetchall():
                user_data['data_categories']['consents'].append({
                    'consent_type': row[0],
                    'granted': row[1],
                    'timestamp': row[2].isoformat() if row[2] else None,
                    'version': row[3]
                })
            
            # Get DSAR requests
            cursor.execute('''
                SELECT 
                    request_id,
                    request_type,
                    request_status,
                    request_timestamp
                FROM data_subject_requests
                WHERE user_id = %s
                ORDER BY request_timestamp DESC
            ''', (user_id,))
            
            for row in cursor.fetchall():
                user_data['data_categories']['dsar_requests'].append({
                    'request_id': str(row[0]),
                    'type': row[1],
                    'status': row[2],
                    'timestamp': row[3].isoformat() if row[3] else None
                })
            
            return user_data
            
        finally:
            cursor.close()
            conn.close()
    
    def delete_user_data(self, user_id: str, request_id: str,
                        hard_delete: bool = False) -> Dict:
        """
        Delete user data (Right to be Forgotten)
        
        Args:
            user_id: User identifier
            request_id: DSAR request ID
            hard_delete: If True, permanently delete. If False, anonymize.
            
        Returns:
            Deletion summary
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            deletion_summary = {
                'user_id': user_id,
                'request_id': request_id,
                'deletion_timestamp': datetime.utcnow().isoformat(),
                'method': 'HARD_DELETE' if hard_delete else 'ANONYMIZE',
                'tables_affected': [],
                'total_records_deleted': 0
            }
            
            # Tables to process (add more as needed)
            tables_to_clean = [
                'user_consent',
                'data_subject_requests',
                # Future: Add user-specific tables
            ]
            
            for table in tables_to_clean:
                if hard_delete:
                    # Permanent deletion
                    cursor.execute(
                        f"DELETE FROM {table} WHERE user_id = %s",
                        (user_id,)
                    )
                else:
                    # Anonymization (replace user_id with hash)
                    cursor.execute(
                        f"UPDATE {table} SET user_id = 'DELETED_' || encode(digest(user_id, 'sha256'), 'hex') WHERE user_id = %s",
                        (user_id,)
                    )
                
                rows_affected = cursor.rowcount
                
                if rows_affected > 0:
                    deletion_summary['tables_affected'].append({
                        'table': table,
                        'records': rows_affected
                    })
                    deletion_summary['total_records_deleted'] += rows_affected
                    
                    # Log deletion
                    cursor.execute('''
                        INSERT INTO data_deletion_log (
                            user_id,
                            request_id,
                            table_name,
                            records_deleted,
                            deletion_method
                        ) VALUES (%s, %s, %s, %s, %s)
                    ''', (
                        user_id,
                        request_id,
                        table,
                        rows_affected,
                        'HARD_DELETE' if hard_delete else 'ANONYMIZE'
                    ))
            
            # Update DSAR request status
            cursor.execute('''
                UPDATE data_subject_requests
                SET request_status = 'COMPLETED',
                    completed_timestamp = NOW(),
                    data_deleted_at = NOW()
                WHERE request_id = %s
            ''', (request_id,))
            
            conn.commit()
            
            return deletion_summary
            
        except Exception as e:
            conn.rollback()
            raise
            
        finally:
            cursor.close()
            conn.close()
    
    def get_pending_requests(self) -> List[Dict]:
        """
        Get all pending DSAR requests
        
        Returns:
            List of pending requests with SLA status
        """
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT 
                    request_id,
                    user_id,
                    request_type,
                    request_status,
                    request_timestamp,
                    days_pending,
                    sla_status
                FROM pending_dsar_requests
                ORDER BY days_pending DESC
            ''')
            
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
            
        finally:
            cursor.close()
            conn.close()


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Database parameters
    db_params = {
        'host': os.environ['RDS_ENDPOINT'],
        'database': os.environ['RDS_DATABASE'],
        'user': os.environ['RDS_USERNAME'],
        'password': os.environ['RDS_PASSWORD'],
        'port': int(os.environ.get('RDS_PORT', '5432'))
    }
    
    compliance = ComplianceAPI(db_params)
    
    print("Compliance API Examples")
    print("=" * 60)
    
    # Example 1: Record consent
    print("\n1. RECORD USER CONSENT:")
    test_user = "test_user_123"
    consent_id = compliance.record_consent(
        test_user,
        'DATA_PROCESSING',
        True,
        version='1.0',
        ip_address='192.168.1.100'
    )
    print(f"Consent recorded with ID: {consent_id}")
    
    # Example 2: Get user consents
    print("\n2. GET USER CONSENTS:")
    consents = compliance.get_user_consents(test_user)
    print(f"User has {len(consents)} consent(s)")
    for consent in consents:
        print(f"  - {consent['consent_type']}: {consent['consent_granted']}")
    
    # Example 3: Create DSAR request
    print("\n3. CREATE DSAR REQUEST (ACCESS):")
    request_id = compliance.create_dsar_request(
        test_user,
        'ACCESS',
        'test@example.com'
    )
    print(f"DSAR request created: {request_id}")
    
    # Example 4: Get DSAR status
    print("\n4. GET DSAR STATUS:")
    status = compliance.get_dsar_status(request_id)
    print(f"Status: {status['request_status']}")
    print(f"Type: {status['request_type']}")
    
    # Example 5: Export user data
    print("\n5. EXPORT USER DATA:")
    user_data = compliance.export_user_data(test_user)
    print(f"Exported data for user: {user_data['user_id']}")
    print(f"Consents: {len(user_data['data_categories']['consents'])}")
    print(f"Requests: {len(user_data['data_categories']['dsar_requests'])}")
    
    # Example 6: Get pending requests
    print("\n6. GET PENDING REQUESTS:")
    pending = compliance.get_pending_requests()
    print(f"Total pending requests: {len(pending)}")
    
    print("\n" + "=" * 60)
    print("✓ All compliance API examples complete")

