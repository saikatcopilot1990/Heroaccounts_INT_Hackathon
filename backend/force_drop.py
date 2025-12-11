"""
Force drop all tables including old schema tables.
"""

from app.db import engine
from sqlalchemy import text

def force_drop_all_tables():
    print("Dropping all tables with CASCADE...")
    
    # List of all known tables (old and new)
    tables = [
        'notifications',
        'approvals', 
        'receipts',
        'claims',
        'travel_plans',
        'budgets',
        'users',
        'receipt_status_history',  # Old table
        'approval_routes',  # Old table
        'employees',  # Old table
        'travel_requests',  # Old table
        'project_budgets'  # Old table
    ]
    
    with engine.connect() as conn:
        for table in tables:
            try:
                conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                conn.commit()
                print(f"Dropped {table}")
            except Exception as e:
                print(f"Could not drop {table}: {e}")
    
    print("\nAll tables dropped. Now run:")
    print("1. python init_db.py")
    print("2. python seed_db.py")

if __name__ == "__main__":
    force_drop_all_tables()
