from app.database.database import engine, Base
from app.models import domain

def init_db():
    # In a real app, use Alembic for migrations.
    # For this prototype, we'll just create all tables if they don't exist.
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
