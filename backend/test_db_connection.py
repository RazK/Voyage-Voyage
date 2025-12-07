#!/usr/bin/env python3
"""Test database connection with correct credentials.

This script verifies that the application can connect to the database
created by docker-compose.yml with the default credentials.
"""
import os
import sys
import time
from sqlalchemy import text

# Import after setting env if needed
from app.core.database import engine
from app.core.config import settings

def test_connection():
    """Test database connection and basic operations."""
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    print()
    print(f"Using DATABASE_URL: {settings.database_url}")
    print(f"Expected:           postgresql://voyage:voyage@localhost:5433/voyage")
    print()
    
    if settings.database_url != "postgresql://voyage:voyage@localhost:5433/voyage":
        print("✗ Configuration mismatch!")
        print(f"  Expected: postgresql://voyage:voyage@localhost:5433/voyage")
        print(f"  Got:      {settings.database_url}")
        return False
    
    print("✓ Configuration matches docker-compose.yml")
    print()
    print("Attempting to connect to database...")
    print()
    
    max_retries = 10
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                # Test 1: Version check
                result = conn.execute(text('SELECT version()'))
                version = result.fetchone()[0]
                print(f'✓ Connected to PostgreSQL: {version.split(",")[0]}')
                
                # Test 2: Database and user
                result = conn.execute(text('SELECT current_database(), current_user'))
                db_name, db_user = result.fetchone()
                print(f'✓ Database: {db_name}')
                print(f'✓ User: {db_user}')
                
                # Test 3: Table operations
                conn.execute(text('CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name TEXT)'))
                conn.commit()
                print('✓ Can create tables')
                
                # Test 4: Data operations
                conn.execute(text("INSERT INTO test_table (name) VALUES ('test') ON CONFLICT DO NOTHING"))
                result = conn.execute(text('SELECT COUNT(*) FROM test_table'))
                count = result.fetchone()[0]
                print(f'✓ Can insert and query data (test_table has {count} rows)')
                
                # Cleanup
                conn.execute(text('DROP TABLE IF EXISTS test_table'))
                conn.commit()
                print('✓ Can drop tables')
                
                print()
                print("=" * 60)
                print("🎉 ALL TESTS PASSED!")
                print("=" * 60)
                return True
                
        except Exception as e:
            if attempt < max_retries - 1:
                print(f'  Attempt {attempt + 1}/{max_retries}: Waiting for database...')
                time.sleep(retry_delay)
            else:
                print()
                print(f'✗ Connection failed after {max_retries} attempts')
                print(f'  Error: {e}')
                print()
                print("Troubleshooting:")
                print("  1. Make sure docker-compose is running:")
                print("     cd backend && docker compose up db -d")
                print()
                print("  2. Check if port 5432 is available:")
                print("     lsof -i :5432")
                print()
                print("  3. If another PostgreSQL is using port 5432, stop it:")
                print("     brew services stop postgresql@15  # Homebrew")
                print("     OR")
                print("     sudo lsof -ti:5432 | xargs kill -9")
                return False
    
    return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)

