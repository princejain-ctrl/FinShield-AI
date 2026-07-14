from fastapi import FastAPI
from model.predict import predict_with_explanation

app = FastAPI(
    title="FinSecure AI",
    description="Explainable AI Credit Risk Assessment API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to FinSecure AI 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    data: dict


@app.post("/predict")
def predict(request: PredictionRequest):
    result = predict_with_explanation(request.data)
    return result