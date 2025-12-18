import os
import logging
import joblib 
import numpy as np
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.api.schemas import PredictResponse, HealthResponse, PredictRequest

logger = logging.getLogger(__name__)
api_router = APIRouter()

MODEL = None
try:
    model_path = os.getenv("MODEL_PATH", "models/model.pkl")
    MODEL = joblib.load(model_path) 
    logger.info(f"Model loaded from {model_path}")
except Exception as e:
    logger.error(f"Error loading model: {e}")

@api_router.get("/health")
async def health() -> HealthResponse:
    response = HealthResponse(status="ок", version=os.getenv("MODEL_VERSION", "v1.0.0"))
    return response

@api_router.post("/predict")
async def predict(request: PredictRequest) -> PredictResponse:
    if MODEL is None:
        return JSONResponse(content="Model not loaded", status_code=500)
    
    try:
        features_array = np.array(request.features).reshape(1, -1)
        
        prediction = MODEL.predict(features_array)[0]
        
        if hasattr(MODEL, 'predict_proba'):
            confidence = float(MODEL.predict_proba(features_array).max())
        else:
            confidence = 0.95
        
        predict_response = PredictResponse(
            prediction=float(prediction),
            confidence=confidence,
            version=os.getenv("MODEL_VERSION", "v1.0.0")
        )
        return predict_response
        
    except Exception as e:
        return JSONResponse(content={"error": f"Prediction error: {str(e)}"}, status_code=400)