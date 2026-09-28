import os

base_dir = r"C:\Users\ASMIT PANDEY\.gemini\antigravity\scratch\cropdrop\backend"

files = {
    "requirements.txt": """fastapi==0.110.0
uvicorn==0.27.1
pydantic==2.6.4
""",
    "app/__init__.py": "",
    "app/models/__init__.py": "",
    "app/schemas/__init__.py": "",
    "app/routers/__init__.py": "",
    "app/services/__init__.py": "",
    "app/database/__init__.py": "",
    
    "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import fields, predictions

app = FastAPI(
    title="CropDrop API",
    description="AI-Powered Smart Irrigation & Water Optimization",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fields.router, prefix="/api/fields", tags=["Fields"])
app.include_router(predictions.router, prefix="/api", tags=["Predictions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the CropDrop API prototype"}
""",
    
    "app/schemas/field.py": """from pydantic import BaseModel
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
""",
    
    "app/schemas/prediction.py": """from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    soilMoisture: float
    temperature: float
    humidity: float
    rainProbability: float
    crop: str
    growthStage: str
    fieldArea: float

class PredictionResponse(BaseModel):
    status: str
    waterAmount: float
    recommendedTime: str
    reasons: List[str]
""",
    
    "app/routers/fields.py": """from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.field import FieldResponse, FieldCreate, SensorReading

router = APIRouter()

# Temporary mock data until Phase 3 (Database integration)
mock_fields = [
    {
        "id": "1",
        "name": "North Field",
        "crop": "Tomato",
        "growth_stage": "Flowering",
        "area": 2.5,
        "soil_moisture": 27.0,
        "temperature": 33.0,
        "humidity": 58.0,
        "rain_probability": 15.0,
        "status": "IRRIGATE",
        "recommended_water": 420.0,
        "recommended_time": "18:00"
    },
    {
        "id": "2",
        "name": "East Field",
        "crop": "Rice",
        "growth_stage": "Vegetative",
        "area": 5.0,
        "soil_moisture": 70.0,
        "temperature": 28.0,
        "humidity": 80.0,
        "rain_probability": 40.0,
        "status": "GOOD",
        "recommended_water": 0.0,
        "recommended_time": None
    }
]

@router.get("/", response_model=List[FieldResponse])
def get_fields():
    return mock_fields

@router.get("/{field_id}", response_model=FieldResponse)
def get_field(field_id: str):
    for field in mock_fields:
        if field["id"] == field_id:
            return field
    raise HTTPException(status_code=404, detail="Field not found")

@router.post("/", response_model=FieldResponse)
def create_field(field: FieldCreate):
    new_field = field.model_dump()
    new_field["id"] = str(len(mock_fields) + 1)
    mock_fields.append(new_field)
    return new_field

@router.put("/{field_id}")
def update_field(field_id: str):
    return {"message": "Update not implemented in prototype mock"}

@router.delete("/{field_id}")
def delete_field(field_id: str):
    return {"message": "Delete not implemented in prototype mock"}

@router.get("/{field_id}/readings")
def get_readings(field_id: str):
    return [
        {"time": "09:00", "moisture": 42},
        {"time": "11:00", "moisture": 39},
        {"time": "13:00", "moisture": 35},
        {"time": "15:00", "moisture": 30},
        {"time": "17:00", "moisture": 27}
    ]

@router.post("/{field_id}/readings")
def post_reading(field_id: str, reading: SensorReading):
    # Simulates IoT ingestion
    return {"status": "success", "reading_saved": reading}

@router.get("/{field_id}/weather")
def get_weather(field_id: str):
    return {"rain_probability": 15.0, "temperature": 33.0}

@router.get("/{field_id}/recommendation")
def get_recommendation(field_id: str):
    return {
        "status": "IRRIGATE",
        "waterAmount": 420.0,
        "recommendedTime": "18:00",
        "reasons": ["Soil moisture is below target"]
    }
""",
    
    "app/routers/predictions.py": """from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest, PredictionResponse

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_irrigation(request: PredictionRequest):
    # Dummy mock logic for Phase 2. To be replaced by ML in Phase 6.
    status = "MONITOR"
    water = 0.0
    reasons = []

    if request.soilMoisture < 35 and request.rainProbability < 40:
        status = "IRRIGATE"
        water = 420.0
        reasons.append("Soil moisture is below the configured target")
        reasons.append("Rain probability is currently low")
    elif request.rainProbability >= 70:
        status = "WAIT_FOR_RAIN"
        reasons.append("High probability of rain coming")
    elif request.soilMoisture >= 60:
        status = "NO_IRRIGATION"
        reasons.append("Soil moisture is completely sufficient")
    
    return PredictionResponse(
        status=status,
        waterAmount=water,
        recommendedTime="18:00" if status == "IRRIGATE" else "",
        reasons=reasons or ["Conditions are currently stable"]
    )
"""
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
print("Backend files created successfully.")
