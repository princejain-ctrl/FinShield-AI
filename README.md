# FinSecure AI

An **Explainable AI Credit Risk Assessment Platform** — a production-ready portfolio project that combines machine learning with transparent, interpretable predictions for credit risk evaluation.

## Overview

FinSecure AI helps assess credit risk using an XGBoost classifier trained on the German Credit dataset. Predictions are accompanied by **SHAP-based explanations**, so users can understand *why* a particular risk score was assigned — not just *what* the score is.

## Tech Stack

| Layer      | Technologies                          |
| ---------- | ------------------------------------- |
| Frontend   | React, Vite, Tailwind CSS             |
| Backend    | FastAPI                               |
| ML         | XGBoost, Scikit-learn, Pandas, NumPy, SHAP |

**Not included:** database, authentication, or Docker — keeping the stack focused and deployable as a lightweight demo.

## Repository Structure

```
FinSecure-AI/
├── frontend/              # React + Vite + Tailwind CSS client
├── backend/               # FastAPI application (Phase 3)
├── model/                 # Machine learning pipeline
│   ├── config.py          # Constants and paths
│   ├── utils.py           # Data loading and I/O helpers
│   ├── preprocess.py      # Feature engineering + sklearn Pipeline
│   ├── evaluate.py        # Metrics and model comparison
│   ├── train.py           # Training orchestration
│   ├── predict.py         # Inference with SHAP explanations
│   └── saved_model/       # Trained artifacts (generated)
├── data/                  # Local dataset copy (generated)
├── docs/                  # EDA notebook and visualizations
│   ├── EDA.ipynb
│   ├── feature_importance.png
│   └── shap_summary.png
├── requirements.txt
└── README.md
```

## Machine Learning Pipeline

The ML pipeline is modular and interview-friendly. Each module has a single responsibility:

| Module | Purpose |
| ------ | ------- |
| `config.py` | Paths, hyperparameters, feature lists |
| `utils.py` | OpenML download, logging, artifact I/O |
| `preprocess.py` | Feature engineering, imputation, encoding |
| `evaluate.py` | Accuracy, Precision, Recall, F1, ROC-AUC |
| `train.py` | End-to-end training and artifact generation |
| `predict.py` | Load model and predict with explanations |

### Dataset

The pipeline automatically downloads the **German Credit Dataset** from OpenML:

```python
from sklearn.datasets import fetch_openml
fetch_openml(name="credit-g", version=1, as_frame=True)
```

A local CSV copy is saved to `data/credit_g.csv`. The target column is `class` (`good` / `bad`).

### Model Selection

Two models are trained and compared:

1. **Logistic Regression** (baseline) — linear, interpretable, with scaled numeric features
2. **XGBoost Classifier** (production model) — captures non-linear patterns and feature interactions

| Metric | Purpose |
| ------ | ------- |
| Accuracy | Overall correctness |
| Precision | Minimize false positives (approving bad credit) |
| Recall | Minimize false negatives (rejecting good credit) |
| F1 | Harmonic mean of precision and recall |
| ROC-AUC | Threshold-independent ranking quality |

XGBoost is selected as the production model because it typically achieves higher ROC-AUC and F1 on this dataset, handles mixed feature types without strict linearity assumptions, and provides native feature importance plus SHAP explainability.

### Evaluation Metrics

Both models are evaluated on an 80/20 stratified hold-out split (`random_state=42`). Reports include classification reports, confusion matrices, and a side-by-side comparison table stored in `model/saved_model/metadata.json`.

### How to Retrain

From the project root:

```bash
# Install dependencies
pip install -r requirements.txt

# Run full training pipeline
python -m model.train
```

This will:

1. Download (or load) the German Credit dataset
2. Engineer explainable features
3. Train Logistic Regression and XGBoost
4. Print evaluation metrics and model comparison
5. Save artifacts to `model/saved_model/`
6. Generate `docs/feature_importance.png` and `docs/shap_summary.png`

### Making Predictions

```python
from model.predict import load_model, predict_with_explanation

load_model()
result = predict_with_explanation({
    "checking_status": "no checking",
    "duration": 12,
    "credit_history": "existing paid",
    "purpose": "radio/tv",
    "credit_amount": 2500,
    "savings_status": "little",
    "employment": "1<=X<4",
    "installment_commitment": 2,
    "personal_status": "male single",
    "other_parties": "none",
    "residence_since": 3,
    "property_magnitude": "real estate",
    "age": 32,
    "other_payment_plans": "none",
    "housing": "own",
    "existing_credits": 1,
    "job": "skilled",
    "num_dependents": 1,
    "own_telephone": "yes",
    "foreign_worker": "yes",
})
print(result)
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
| 2     | Complete    | ML model training and persistence        |
| 3     | Planned     | Backend API endpoints                    |
| 4     | Planned     | Frontend UI and integration              |

## License

This project is built for portfolio and educational purposes.
