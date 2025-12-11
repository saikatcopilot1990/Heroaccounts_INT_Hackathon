from app.db import engine, Base
from app.models import User, Claim, Receipt, Approval, Budget, TravelPlan, Notification

def init_db():
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
