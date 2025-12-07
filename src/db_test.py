"""
Day 3: Test RDS PostgreSQL connection
Goal: Verify we can connect to our cloud database
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test basic connection to RDS"""
    print("=" * 60)
    print("TESTING RDS POSTGRESQL CONNECTION")
    print("=" * 60)
    
    # Get credentials from environment
    db_params = {
        'host': os.getenv('RDS_ENDPOINT'),
        'database': os.getenv('RDS_DATABASE'),
        'user': os.getenv('RDS_USERNAME'),
        'password': os.getenv('RDS_PASSWORD'),
        'port': os.getenv('RDS_PORT', '5432')
    }
    
    print(f"\nConnection parameters:")
    print(f"  Host: {db_params['host']}")
    print(f"  Database: {db_params['database']}")
    print(f"  User: {db_params['user']}")
    print(f"  Port: {db_params['port']}")
    print("-" * 60)
    
    try:
        print("\n🔌 Connecting to RDS...")
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        
        print("✅ CONNECTION SUCCESSFUL!")
        print(f"\nPostgreSQL version:")
        print(f"  {db_version}")
        
        # Check current database
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()[0]
        print(f"\nConnected to database: {current_db}")
        
        # List existing tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        print(f"\nExisting tables: {len(tables)}")
        if tables:
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("  (none - database is empty, ready for schema)")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ RDS CONNECTION TEST PASSED")
        print("=" * 60)
        
        return True
        
    except psycopg2.OperationalError as e:
        print("❌ CONNECTION FAILED")
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("  1. Check RDS instance is 'Available' in AWS Console")
        print("  2. Verify endpoint in .env matches RDS Console")
        print("  3. Check security group allows your IP on port 5432")
        print("  4. Verify username/password are correct")
        return False
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False

if __name__ == "__main__":
    test_connection()

