# FinSecure AI

An **Explainable AI Credit Risk Assessment Platform** — a production-ready portfolio project that combines machine learning with transparent, interpretable predictions for credit risk evaluation.

## Overview

FinSecure AI helps assess credit risk using an XGBoost classifier trained on financial applicant data. Predictions are accompanied by **SHAP-based explanations**, so users can understand *why* a particular risk score was assigned — not just *what* the score is.

## Tech Stack

| Layer      | Technologies                          |
| ---------- | ------------------------------------- |
| Frontend   | React, Vite, Tailwind CSS             |
| Backend    | FastAPI                               |
| ML         | XGBoost, Scikit-learn, Pandas, NumPy, SHAP |

**Not included:** database, authentication, or Docker — keeping the stack focused and deployable as a lightweight demo.

## Project Structure

```
FinSecure-AI/
├── frontend/          # React + Vite + Tailwind CSS client
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── hooks/
│       ├── utils/
│       └── assets/
├── backend/           # FastAPI application
│   ├── app/
│   ├── routes/
│   ├── services/
│   ├── ml/
│   ├── schemas/
│   ├── utils/
│   └── main.py
├── model/             # Trained model artifacts
├── data/              # Datasets
├── docs/              # Documentation
├── requirements.txt   # Root Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The client will be available at `http://localhost:5173`.

## Development Phases

| Phase | Status      | Description                              |
| ----- | ----------- | ---------------------------------------- |
| 1     | Complete    | Project scaffold and tooling setup       |
| 2     | Planned     | ML model training and persistence        |
| 3     | Planned     | Backend API endpoints                    |
| 4     | Planned     | Frontend UI and integration              |

## License

This project is built for portfolio and educational purposes.
