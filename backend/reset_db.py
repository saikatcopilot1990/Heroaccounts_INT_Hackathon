"""
Reset database script - drops all tables and recreates them with the current schema.
WARNING: This will delete all data in the database!
"""

from app.db import engine, Base
from app.models import User, Claim, Receipt, Approval, Budget, TravelPlan, Notification

def reset_database():
    print("WARNING: This will DROP ALL TABLES and delete all data!")
    print("Dropping all tables...")
    
    try:
        Base.metadata.drop_all(bind=engine)
        print("All tables dropped")
        
        print("\nCreating tables with new schema...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
        
        print("\nDatabase reset complete!")
        print("\nNext steps:")
        print("1. Run: python seed_db.py  # To add test data")
        print("2. Restart the server")
        
    except Exception as e:
        print(f"Error resetting database: {e}")

if __name__ == "__main__":
    response = input("Are you sure you want to reset the database? (yes/no): ")
    if response.lower() == "yes":
        reset_database()
    else:
        print("Operation cancelled.")
