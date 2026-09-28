from pydantic import BaseModel
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
