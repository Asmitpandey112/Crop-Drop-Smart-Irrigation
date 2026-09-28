import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup DB connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./cropdrop.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models
from app.models.domain import Base, User, Field, SensorReading, WeatherData, IrrigationRecord

def generate_rich_db():
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create User
        print("Seeding User...")
        user = User(
            name="Demo Farmer",
            email="demo@cropdrop.io",
            
            created_at=datetime.utcnow() - timedelta(days=30)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create Fields
        print("Seeding Fields...")
        fields_data = [
            {"name": "North Field", "crop": "Tomato", "area": 2.5, "growth_stage": "Flowering"},
            {"name": "South Paddy", "crop": "Rice", "area": 5.0, "growth_stage": "Vegetative"},
            {"name": "East Block", "crop": "Wheat", "area": 10.0, "growth_stage": "Heading"},
            {"name": "West Greenhouse", "crop": "Tomato", "area": 1.5, "growth_stage": "Seedling"},
            {"name": "River Plot", "crop": "Rice", "area": 8.0, "growth_stage": "Ripening"},
        ]
        
        fields = []
        for fd in fields_data:
            field = Field(
                user_id=user.id,
                name=fd["name"],
                crop=fd["crop"],
                area=fd["area"],
                growth_stage=fd["growth_stage"],
                created_at=datetime.utcnow() - timedelta(days=30)
            )
            db.add(field)
            fields.append(field)
        
        db.commit()
        
        # Generate Time Series Data (24 hours of sensor data)
        print("Generating 24-hour sensor data for charts...")
        now = datetime.utcnow()
        for field in fields:
            # Different baseline moisture based on crop
            base_moisture = 40.0
            if field.crop == "Rice":
                base_moisture = 75.0
            elif field.crop == "Tomato":
                base_moisture = 35.0
            
            # Generate 24 hours of data
            for i in range(24):
                time_point = now - timedelta(hours=23-i)
                
                # Create a realistic curve (dips during day, rises a bit at night)
                hour = time_point.hour
                day_factor = -5.0 if 10 <= hour <= 16 else 2.0
                
                # Add random noise
                noise = random.uniform(-2.0, 2.0)
                
                # Current values
                current_moisture = max(0, min(100, base_moisture + day_factor + noise))
                current_temp = 20.0 + (10.0 if 10 <= hour <= 16 else 0) + random.uniform(-2, 2)
                current_humidity = 60.0 + (-15.0 if 10 <= hour <= 16 else 10.0) + random.uniform(-5, 5)
                
                reading = SensorReading(
                    field_id=field.id,
                    soil_moisture=round(current_moisture, 1),
                    temperature=round(current_temp, 1),
                    humidity=round(current_humidity, 1),
                    timestamp=time_point
                )
                db.add(reading)
                
                # Add weather data for the latest reading only (for simplicity)
                if i == 23:
                    rain_prob = 10.0
                    if field.name == "South Paddy": rain_prob = 85.0
                    if field.name == "East Block": rain_prob = 45.0
                    
                    weather = WeatherData(
                        field_id=field.id,
                        temperature=round(current_temp, 1),
                        humidity=round(current_humidity, 1),
                        rain_probability=rain_prob,
                        date=time_point.date()
                    )
                    db.add(weather)
                    
        db.commit()
        print("✅ Database successfully generated with rich demo data!")
        
    except Exception as e:
        print(f"Error generating DB: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_rich_db()
