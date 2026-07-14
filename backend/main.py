from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.predict import predict_with_explanation

app = FastAPI(
    title="FinSecure AI",
    description="Explainable AI Credit Risk Assessment API",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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