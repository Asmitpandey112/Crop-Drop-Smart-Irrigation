import os
from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.models import domain
from app.database.database import Base

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(domain.Field).first():
        print("Database already seeded!")
        db.close()
        return

    # Create dummy user
    user = domain.User(name="Demo Farmer", email="farmer@cropdrop.com")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create fields
    field1 = domain.Field(id="1", user_id=user.id, name="North Field", crop="Tomato", growth_stage="Flowering", area=2.5)
    field2 = domain.Field(id="2", user_id=user.id, name="East Field", crop="Rice", growth_stage="Vegetative", area=5.0)
    field3 = domain.Field(id="3", user_id=user.id, name="South Field", crop="Wheat", growth_stage="Maturation", area=10.0)
    
    db.add_all([field1, field2, field3])
    db.commit()

    # Create sensor readings for Field 1
    readings = [
        domain.SensorReading(field_id="1", soil_moisture=42, temperature=33, humidity=58),
        domain.SensorReading(field_id="1", soil_moisture=39, temperature=33, humidity=58),
        domain.SensorReading(field_id="1", soil_moisture=35, temperature=33, humidity=58),
        domain.SensorReading(field_id="1", soil_moisture=30, temperature=33, humidity=58),
        domain.SensorReading(field_id="1", soil_moisture=27, temperature=33, humidity=58), # Latest
    ]
    
    # Create sensor readings for Field 2
    readings.append(domain.SensorReading(field_id="2", soil_moisture=70, temperature=28, humidity=80))

    # Create sensor readings for Field 3
    readings.append(domain.SensorReading(field_id="3", soil_moisture=45, temperature=25, humidity=60))
    
    db.add_all(readings)

    # Weather data
    w1 = domain.WeatherData(field_id="1", temperature=33, humidity=58, rain_probability=15)
    w2 = domain.WeatherData(field_id="2", temperature=28, humidity=80, rain_probability=40)
    w3 = domain.WeatherData(field_id="3", temperature=25, humidity=60, rain_probability=85)
    db.add_all([w1, w2, w3])

    db.commit()
    print("Database seeded with mock data successfully.")
    db.close()

if __name__ == "__main__":
    seed()
