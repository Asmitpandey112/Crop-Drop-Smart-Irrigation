import os

base_dir = r"C:\Users\ASMIT PANDEY\.gemini\antigravity\scratch\cropdrop\backend"

files = {
    ".env.example": """# Database configuration
DATABASE_URL=postgresql://user:password@localhost:5432/cropdrop
# Or if using Supabase:
# DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
""",
    
    ".env": """DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cropdrop
""",

    "app/database/database.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cropdrop.db")

# For SQLite, we need connect_args={"check_same_thread": False}. For PostgreSQL we don't.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # Supabase / PostgreSQL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
    
    "app/models/domain.py": """from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    fields = relationship("Field", back_populates="owner")

class Field(Base):
    __tablename__ = "fields"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    crop = Column(String, nullable=False)
    growth_stage = Column(String, nullable=False)
    area = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="fields")
    readings = relationship("SensorReading", back_populates="field")
    weather = relationship("WeatherData", back_populates="field")
    irrigation_records = relationship("IrrigationRecord", back_populates="field")

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(String, primary_key=True, default=generate_uuid)
    field_id = Column(String, ForeignKey("fields.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    soil_moisture = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)

    field = relationship("Field", back_populates="readings")

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(String, primary_key=True, default=generate_uuid)
    field_id = Column(String, ForeignKey("fields.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    rain_probability = Column(Float, nullable=False)

    field = relationship("Field", back_populates="weather")

class IrrigationRecord(Base):
    __tablename__ = "irrigation_records"

    id = Column(String, primary_key=True, default=generate_uuid)
    field_id = Column(String, ForeignKey("fields.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    recommended_amount = Column(Float, nullable=False)
    actual_amount = Column(Float, nullable=True)
    status = Column(String, nullable=False) # e.g., 'COMPLETED', 'PENDING'

    field = relationship("Field", back_populates="irrigation_records")
""",

    "app/database/init_db.py": """from app.database.database import engine, Base
from app.models import domain

def init_db():
    # In a real app, use Alembic for migrations.
    # For this prototype, we'll just create all tables if they don't exist.
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
"""
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
print("Phase 3 files created successfully.")
