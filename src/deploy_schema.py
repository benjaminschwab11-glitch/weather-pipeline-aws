"""
Deploy database schema to RDS
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def deploy_schema():
    """Deploy schema from schema.sql file"""
    print("=" * 60)
    print("DEPLOYING DATABASE SCHEMA")
    print("=" * 60)
    
    # Read schema file
    with open('database/schema.sql', 'r') as f:
        schema_sql = f.read()
    
    # Connect to database
    conn = psycopg2.connect(
        host=os.getenv('RDS_ENDPOINT'),
        database=os.getenv('RDS_DATABASE'),
        user=os.getenv('RDS_USERNAME'),
        password=os.getenv('RDS_PASSWORD'),
        port=os.getenv('RDS_PORT', '5432')
    )
    
    cursor = conn.cursor()
    
    try:
        print("\n📋 Executing schema SQL...")
        cursor.execute(schema_sql)
        conn.commit()
        
        print("✅ Schema deployed successfully!")
        
        # Verify tables created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print(f"\n📊 Tables created: {len(tables)}")
        for table in tables:
            print(f"  ✓ {table[0]}")
        
        # Verify indexes
        cursor.execute("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename = 'weather_observations'
        """)
        
        indexes = cursor.fetchall()
        print(f"\n🔍 Indexes created: {len(indexes)}")
        for index in indexes:
            print(f"  ✓ {index[0]}")
        
        # Verify views
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public'
        """)
        
        views = cursor.fetchall()
        print(f"\n👁️  Views created: {len(views)}")
        for view in views:
            print(f"  ✓ {view[0]}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Schema deployment failed: {e}")
        raise
        
    finally:
        cursor.close()
        conn.close()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE READY FOR DATA")
    print("=" * 60)

if __name__ == "__main__":
    deploy_schema()

