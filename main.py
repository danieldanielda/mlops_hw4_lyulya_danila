import uvicorn
import time
from fastapi import FastAPI, Request
from prometheus_client import Histogram, start_http_server, CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from src.api.router import api_router

# Создаём гистограмму для latency
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"]
)

app = FastAPI(
    title="ML Service API",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json"
)

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.middleware("http")
async def add_latency_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(latency)
    return response

app.include_router(api_router, prefix="/api/v1", tags=["ML Service"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8080,
    )