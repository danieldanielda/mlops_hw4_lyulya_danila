import uvicorn
from fastapi import FastAPI
from src.api.router import api_router

app = FastAPI(
    title="ML Service API",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json"
)
app.include_router(api_router, prefix="/api/v1", tags=["ML Service"])

if __name__ == "__main__":
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1", 
        port=8744,
    )