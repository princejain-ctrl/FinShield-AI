from fastapi import FastAPI

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