from pydantic import BaseModel
from typing import List

class HealthResponse(BaseModel):
    status: str
    version: str

class PredictRequest(BaseModel):
    features: List[float]

class PredictResponse(BaseModel):
    prediction: float
    confidence: float
    version: str