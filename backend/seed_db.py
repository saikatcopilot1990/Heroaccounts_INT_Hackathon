"""
Seed script to populate the database with initial data for testing.
Run this script after initializing the database to create sample users, budgets, and travel plans.
"""

from app.db import SessionLocal
from app.models import User, UserRole, Budget, TravelPlan
from datetime import datetime, timedelta

def seed_data():
    db = SessionLocal()
    
    try:
        # Clear existing data first
        print("Clearing existing data...")
        db.query(TravelPlan).delete()
        db.query(Budget).delete()
        db.query(User).delete()
        db.commit()
        
        # Create Users
        print("Creating users...")
        finance_user = User(
            name="Finance Admin",
            email="finance@heroaccounts.com",
            role=UserRole.FINANCE
        )
        
        manager_user = User(
            name="John Manager",
            email="manager@heroaccounts.com",
            role=UserRole.MANAGER
        )
        
        employee_user = User(
            name="Alice Employee",
            email="employee@heroaccounts.com",
            role=UserRole.EMPLOYEE,
            manager_id=2  # Will be manager_user.id after commit
        )
        
        db.add_all([finance_user, manager_user, employee_user])
        db.commit()
        
        # Set manager relationship
        employee_user.manager_id = manager_user.id
        db.commit()
        
        print(f"Created {db.query(User).count()} users")
        
        # Create Budgets
        print("Creating budgets...")
        project_budget = Budget(
            name="Project Alpha",
            total_amount=50000.0,
            used_amount=0.0,
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=365)).date()
        )
        
        db.add(project_budget)
        db.commit()
        
        print(f"Created {db.query(Budget).count()} budgets")
        
        # Create Travel Plans
        print("Creating travel plans...")
        travel_plan = TravelPlan(
            employee_id=employee_user.id,
            destination="Mumbai Client Visit",
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=7)).date(),
            estimated_budget=15000.0,
            approved_budget=12000.0,
            status="approved"
        )
        
        db.add(travel_plan)
        db.commit()
        
        print(f"Created {db.query(TravelPlan).count()} travel plans")
        
        print("\n✅ Database seeded successfully!")
        print("\nTest Accounts:")
        print(f"  Employee: {employee_user.email} (ID: {employee_user.id})")
        print(f"  Manager: {manager_user.email} (ID: {manager_user.id})")
        print(f"  Finance: {finance_user.email} (ID: {finance_user.id})")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
