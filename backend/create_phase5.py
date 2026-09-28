import os

base_dir = r"C:\Users\ASMIT PANDEY\.gemini\antigravity\scratch\cropdrop\backend"

files = {
    "app/services/crop_profiles.py": """# Configurable Crop Profiles for the Rule Engine

CROP_PROFILES = {
    "Tomato": {
        "moisture": {
            "min": 30.0,
            "optimal": 45.0,
            "max": 65.0
        },
        "water_requirement_base": 150.0, # base liters per acre
        "growth_stages": {
            "Seedling": 0.6,
            "Vegetative": 1.0,
            "Flowering": 1.5,
            "Fruiting": 1.3
        }
    },
    "Rice": {
        "moisture": {
            "min": 65.0,
            "optimal": 80.0,
            "max": 100.0
        },
        "water_requirement_base": 400.0,
        "growth_stages": {
            "Vegetative": 1.0,
            "Reproductive": 1.5,
            "Ripening": 0.7
        }
    },
    "Wheat": {
        "moisture": {
            "min": 35.0,
            "optimal": 55.0,
            "max": 75.0
        },
        "water_requirement_base": 120.0,
        "growth_stages": {
            "Tillering": 0.8,
            "Stem Extension": 1.2,
            "Heading": 1.5,
            "Maturation": 0.5
        }
    }
}
""",
    
    "app/services/rule_engine.py": """from app.services.crop_profiles import CROP_PROFILES

def evaluate_irrigation(crop: str, growth_stage: str, soil_moisture: float, rain_probability: float, area: float):
    # Default to Tomato if unknown
    profile = CROP_PROFILES.get(crop, CROP_PROFILES["Tomato"])
    
    min_moisture = profile["moisture"]["min"]
    optimal_moisture = profile["moisture"]["optimal"]
    stage_factor = profile["growth_stages"].get(growth_stage, 1.0)
    
    RAIN_THRESHOLD_HIGH = 60.0
    RAIN_THRESHOLD_LOW = 30.0
    
    status = "MONITOR"
    water = 0.0
    reasons = []

    # Ensure valid defaults if sensor data is missing
    if soil_moisture is None:
        return {"status": "MONITOR", "water_amount": 0.0, "reasons": ["Awaiting sensor data"]}
    if rain_probability is None:
        rain_probability = 0.0

    if soil_moisture < min_moisture:
        if rain_probability >= RAIN_THRESHOLD_HIGH:
            status = "WAIT_FOR_RAIN"
            reasons.append(f"Soil moisture ({soil_moisture}%) is critically low, but high rain probability ({rain_probability}%) means we should wait.")
        else:
            status = "IRRIGATE"
            water = profile["water_requirement_base"] * stage_factor * area
            reasons.append(f"Soil moisture ({soil_moisture}%) is below {crop} minimum target ({min_moisture}%).")
            if rain_probability < RAIN_THRESHOLD_LOW:
                reasons.append(f"Rain probability is currently low ({rain_probability}%).")
            reasons.append(f"Crop is in {growth_stage} stage, requiring calculated dose.")
            
    elif soil_moisture < optimal_moisture:
        if rain_probability >= RAIN_THRESHOLD_HIGH:
            status = "WAIT_FOR_RAIN"
            reasons.append(f"Moisture is sub-optimal, but heavy rain is expected ({rain_probability}%).")
        elif rain_probability >= RAIN_THRESHOLD_LOW:
            status = "MONITOR"
            reasons.append(f"Moderate rain expected ({rain_probability}%), monitoring conditions closely.")
        else:
            status = "IRRIGATE"
            water = (profile["water_requirement_base"] * stage_factor * area) * 0.5 # half dose for sub-optimal
            reasons.append(f"Soil moisture is sub-optimal ({soil_moisture}%) and no rain is expected.")
            
    else:
        status = "NO_IRRIGATION"
        reasons.append(f"Soil moisture ({soil_moisture}%) is optimal or above optimal for {crop}.")

    return {
        "status": status,
        "water_amount": round(water, 1),
        "reasons": reasons
    }
""",

    "app/routers/predictions.py": """from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.rule_engine import evaluate_irrigation

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_irrigation(request: PredictionRequest):
    # Phase 5: Rule Engine Analysis
    analysis = evaluate_irrigation(
        crop=request.crop,
        growth_stage=request.growthStage,
        soil_moisture=request.soilMoisture,
        rain_probability=request.rainProbability,
        area=request.fieldArea
    )
    
    return PredictionResponse(
        status=analysis["status"],
        waterAmount=analysis["water_amount"],
        recommendedTime="18:00" if analysis["status"] == "IRRIGATE" else "",
        reasons=analysis["reasons"]
    )
""",

    "app/routers/fields.py": """from fastapi import APIRouter, HTTPException, Depends
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
"""
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
print("Phase 5 files created successfully.")
