from pydantic import BaseModel
from typing import Optional, List

class FieldBase(BaseModel):
    name: str
    crop: str
    growth_stage: str
    area: float

class FieldCreate(FieldBase):
    pass

class FieldResponse(FieldBase):
    id: str
    soil_moisture: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    rain_probability: Optional[float] = None
    status: Optional[str] = None
    recommended_water: Optional[float] = None
    recommended_time: Optional[str] = None

class SensorReading(BaseModel):
    soil_moisture: float
    temperature: float
    humidity: float
    rain_probability: Optional[float] = None
