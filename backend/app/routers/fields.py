from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.field import FieldResponse, FieldCreate, SensorReading
from app.database.database import get_db
from app.models import domain
from app.services.rule_engine import evaluate_irrigation

router = APIRouter()

def format_field_response(field, db: Session):
    latest_reading = db.query(domain.SensorReading).filter(domain.SensorReading.field_id == field.id).order_by(domain.SensorReading.timestamp.desc()).first()
    latest_weather = db.query(domain.WeatherData).filter(domain.WeatherData.field_id == field.id).order_by(domain.WeatherData.date.desc()).first()
    
    soil_m = latest_reading.soil_moisture if latest_reading else None
    temp = latest_reading.temperature if latest_reading else None
    hum = latest_reading.humidity if latest_reading else None
    rain_p = latest_weather.rain_probability if latest_weather else 0.0

    # Phase 5: Evaluate via rule engine
    analysis = evaluate_irrigation(
        crop=field.crop,
        growth_stage=field.growth_stage,
        soil_moisture=soil_m,
        rain_probability=rain_p,
        area=field.area
    )

    return {
        "id": field.id,
        "name": field.name,
        "crop": field.crop,
        "growth_stage": field.growth_stage,
        "area": field.area,
        "soil_moisture": soil_m,
        "temperature": temp,
        "humidity": hum,
        "rain_probability": rain_p,
        "status": analysis["status"],
        "recommended_water": analysis["water_amount"],
        "recommended_time": "18:00" if analysis["status"] == "IRRIGATE" else None
    }

@router.get("/", response_model=List[FieldResponse])
def get_fields(db: Session = Depends(get_db)):
    fields = db.query(domain.Field).all()
    return [format_field_response(f, db) for f in fields]

@router.get("/{field_id}", response_model=FieldResponse)
def get_field(field_id: str, db: Session = Depends(get_db)):
    field = db.query(domain.Field).filter(domain.Field.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return format_field_response(field, db)

@router.post("/", response_model=FieldResponse)
def create_field(field: FieldCreate, db: Session = Depends(get_db)):
    user = db.query(domain.User).first()
    if not user:
        user = domain.User(name="Demo", email="demo@demo.com")
        db.add(user)
        db.commit()
        db.refresh(user)

    db_field = domain.Field(**field.model_dump(), user_id=user.id)
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return format_field_response(db_field, db)

@router.put("/{field_id}")
def update_field(field_id: str):
    return {"message": "Update not implemented"}

@router.delete("/{field_id}")
def delete_field(field_id: str, db: Session = Depends(get_db)):
    field = db.query(domain.Field).filter(domain.Field.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    db.delete(field)
    db.commit()
    return {"message": "Field deleted"}

@router.get("/{field_id}/readings")
def get_readings(field_id: str, db: Session = Depends(get_db)):
    readings = db.query(domain.SensorReading).filter(domain.SensorReading.field_id == field_id).order_by(domain.SensorReading.timestamp.asc()).all()
    result = []
    base_hour = 9
    for r in readings:
        time_str = f"{base_hour:02d}:00"
        result.append({"time": time_str, "moisture": r.soil_moisture})
        base_hour += 2
        if base_hour > 23: base_hour = 9
    return result

@router.post("/{field_id}/readings")
def post_reading(field_id: str, reading: SensorReading, db: Session = Depends(get_db)):
    db_reading = domain.SensorReading(
        field_id=field_id,
        soil_moisture=reading.soil_moisture,
        temperature=reading.temperature,
        humidity=reading.humidity
    )
    db.add(db_reading)
    if reading.rain_probability is not None:
        db_weather = domain.WeatherData(
            field_id=field_id,
            temperature=reading.temperature,
            humidity=reading.humidity,
            rain_probability=reading.rain_probability
        )
        db.add(db_weather)
    db.commit()
    return {"status": "success"}

@router.get("/{field_id}/recommendation")
def get_recommendation(field_id: str, db: Session = Depends(get_db)):
    field = db.query(domain.Field).filter(domain.Field.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    
    # Phase 5: Get full analysis
    latest_reading = db.query(domain.SensorReading).filter(domain.SensorReading.field_id == field.id).order_by(domain.SensorReading.timestamp.desc()).first()
    latest_weather = db.query(domain.WeatherData).filter(domain.WeatherData.field_id == field.id).order_by(domain.WeatherData.date.desc()).first()
    
    soil_m = latest_reading.soil_moisture if latest_reading else None
    rain_p = latest_weather.rain_probability if latest_weather else 0.0

    analysis = evaluate_irrigation(
        crop=field.crop,
        growth_stage=field.growth_stage,
        soil_moisture=soil_m,
        rain_probability=rain_p,
        area=field.area
    )

    return {
        "status": analysis["status"],
        "waterAmount": analysis["water_amount"],
        "recommendedTime": "18:00" if analysis["status"] == "IRRIGATE" else "",
        "reasons": analysis["reasons"]
    }
