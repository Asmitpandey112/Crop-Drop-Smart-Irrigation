from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
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
