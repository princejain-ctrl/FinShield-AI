"""Configuration constants for the FinSecure AI ML pipeline."""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
MODEL_DIR = Path(__file__).resolve().parent
SAVED_MODEL_DIR = MODEL_DIR / "saved_model"

DATASET_CSV = DATA_DIR / "credit_g.csv"
TRAINED_MODEL_PATH = SAVED_MODEL_DIR / "trained_model.pkl"
PREPROCESSOR_PATH = SAVED_MODEL_DIR / "preprocessor.pkl"
METADATA_PATH = SAVED_MODEL_DIR / "metadata.json"

FEATURE_IMPORTANCE_PATH = DOCS_DIR / "feature_importance.png"
SHAP_SUMMARY_PATH = DOCS_DIR / "shap_summary.png"

# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------
OPENML_NAME = "credit-g"
OPENML_VERSION = 1
TARGET_COLUMN = "class"
POSITIVE_CLASS = "bad"  # Higher credit risk
NEGATIVE_CLASS = "good"

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
RANDOM_STATE = 42
TEST_SIZE = 0.2

# ---------------------------------------------------------------------------
# Feature groups (original columns from the German Credit dataset)
# ---------------------------------------------------------------------------
CATEGORICAL_FEATURES: list[str] = [
    "checking_status",
    "credit_history",
    "purpose",
    "savings_status",
    "employment",
    "personal_status",
    "other_parties",
    "property_magnitude",
    "other_payment_plans",
    "housing",
    "job",
    "own_telephone",
    "foreign_worker",
]

NUMERIC_FEATURES: list[str] = [
    "duration",
    "credit_amount",
    "installment_commitment",
    "residence_since",
    "age",
    "existing_credits",
    "num_dependents",
]

ENGINEERED_FEATURES: list[str] = [
    "credit_per_duration",
    "long_term_loan",
    "high_credit_amount",
    "young_applicant",
    "mature_applicant",
]

# ---------------------------------------------------------------------------
# Model hyperparameters (reasonable defaults, no expensive tuning)
# ---------------------------------------------------------------------------
LOGISTIC_REGRESSION_PARAMS: dict = {
    "max_iter": 1000,
    "class_weight": "balanced",
    "random_state": RANDOM_STATE,
}

XGBOOST_PARAMS: dict = {
    "n_estimators": 100,
    "max_depth": 4,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "eval_metric": "logloss",
    "random_state": RANDOM_STATE,
    "use_label_encoder": False,
}

# ---------------------------------------------------------------------------
# Feature engineering thresholds
# ---------------------------------------------------------------------------
YOUNG_AGE_THRESHOLD = 25
MATURE_AGE_THRESHOLD = 50
