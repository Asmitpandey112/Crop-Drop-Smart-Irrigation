from fastapi import APIRouter
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
