"""Prediction module with SHAP-based explainability for single records."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import shap

from model.config import (
    CATEGORICAL_FEATURES,
    METADATA_PATH,
    NUMERIC_FEATURES,
    POSITIVE_CLASS,
    PREPROCESSOR_PATH,
    TARGET_COLUMN,
    TRAINED_MODEL_PATH,
)
from model.utils import load_metadata, load_pickle

logger = logging.getLogger(__name__)

_model: Any | None = None
_preprocessor: Any | None = None
_explainer: shap.Explainer | None = None
_metadata: dict[str, Any] | None = None


def load_model(model_dir: Path | None = None) -> tuple[Any, Any, dict[str, Any]]:
    """
    Load trained model, preprocessor, and metadata from disk.

    Args:
        model_dir: Optional directory containing saved artifacts.
            Defaults to ``model/saved_model/``.

    Returns:
        Tuple of (model, preprocessor, metadata).
    """
    global _model, _preprocessor, _metadata, _explainer

    base = model_dir or TRAINED_MODEL_PATH.parent
    model_path = base / "trained_model.pkl"
    preprocessor_path = base / "preprocessor.pkl"
    metadata_path = base / "metadata.json"
    explainer_path = base / "shap_explainer.pkl"

    _model = load_pickle(model_path)
    _preprocessor = load_pickle(preprocessor_path)
    _metadata = load_metadata() if metadata_path == METADATA_PATH else _load_json(metadata_path)

    if explainer_path.exists():
        _explainer = load_pickle(explainer_path)
    else:
        _explainer = shap.TreeExplainer(_model)
        logger.warning("SHAP explainer not found; created TreeExplainer on the fly.")

    logger.info("Loaded model artifacts from %s", base)
    return _model, _preprocessor, _metadata


def _load_json(path: Path) -> dict[str, Any]:
    import json

    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _ensure_loaded() -> tuple[Any, Any, dict[str, Any]]:
    if _model is None or _preprocessor is None or _metadata is None:
        return load_model()
    return _model, _preprocessor, _metadata


def _to_dataframe(input_data: dict[str, Any] | pd.DataFrame) -> pd.DataFrame:
    """Convert a single-record dict or DataFrame to a one-row DataFrame."""
    if isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
    else:
        df = pd.DataFrame([input_data])

    required = set(NUMERIC_FEATURES + CATEGORICAL_FEATURES)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required features: {sorted(missing)}")

    if TARGET_COLUMN in df.columns:
        df = df.drop(columns=[TARGET_COLUMN])

    return df


def preprocess_input(input_data: dict[str, Any] | pd.DataFrame) -> np.ndarray:
    """
    Apply the fitted preprocessing pipeline to raw applicant data.

    Args:
        input_data: Dictionary or DataFrame with raw feature values.

    Returns:
        Preprocessed feature matrix as a numpy array.
    """
    _, preprocessor, _ = _ensure_loaded()
    df = _to_dataframe(input_data)
    return preprocessor.transform(df)


def predict_probability(input_data: dict[str, Any] | pd.DataFrame) -> float:
    """
    Return the probability of bad credit (class 1).

    Args:
        input_data: Raw applicant features.

    Returns:
        Float probability in [0, 1].
    """
    model, _, _ = _ensure_loaded()
    features = preprocess_input(input_data)
    proba = float(model.predict_proba(features)[0, 1])
    return proba


def predict_class(
    input_data: dict[str, Any] | pd.DataFrame,
    threshold: float = 0.5,
) -> str:
    """
    Return the predicted credit class label.

    Args:
        input_data: Raw applicant features.
        threshold: Decision threshold for positive (bad) class.

    Returns:
        ``bad`` or ``good``.
    """
    proba = predict_probability(input_data)
    return POSITIVE_CLASS if proba >= threshold else "good"


def explain_prediction(
    input_data: dict[str, Any] | pd.DataFrame,
    top_n: int = 10,
) -> list[dict[str, float | str]]:
    """
    Compute SHAP values for a single prediction.

    Args:
        input_data: Raw applicant features.
        top_n: Number of top contributing features to return.

    Returns:
        List of dicts with feature name, SHAP value, and feature value.
    """
    _, _, metadata = _ensure_loaded()
    features = preprocess_input(input_data)
    feature_names: list[str] = metadata.get("feature_names", [])

    if _explainer is None:
        load_model()

    shap_values = _explainer.shap_values(features)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    contributions = []
    for idx, shap_val in enumerate(shap_values[0]):
        name = feature_names[idx] if idx < len(feature_names) else f"feature_{idx}"
        contributions.append(
            {
                "feature": name,
                "shap_value": float(shap_val),
                "feature_value": float(features[0, idx]),
            }
        )

    contributions.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    return contributions[:top_n]


def predict_with_explanation(
    input_data: dict[str, Any] | pd.DataFrame,
    threshold: float = 0.5,
    top_n: int = 10,
) -> dict[str, Any]:
    """
    Run a full prediction with probability, class label, and SHAP explanation.

    Args:
        input_data: Raw applicant features.
        threshold: Decision threshold for positive class.
        top_n: Number of top SHAP contributors to include.

    Returns:
        Structured dictionary suitable for API or UI consumption.
    """
    proba = predict_probability(input_data)
    predicted_class = POSITIVE_CLASS if proba >= threshold else "good"
    risk_level = _risk_level(proba)
    shap_contributions = explain_prediction(input_data, top_n=top_n)

    return {
        "prediction": {
            "class": predicted_class,
            "probability_bad": round(proba, 4),
            "probability_good": round(1 - proba, 4),
            "risk_level": risk_level,
            "threshold": threshold,
        },
        "explanation": {
            "method": "SHAP",
            "top_contributors": shap_contributions,
        },
        "input_features": {
            k: (v.item() if hasattr(v, "item") else v)
            for k, v in dict(_to_dataframe(input_data).iloc[0]).items()
        },
    }


def _risk_level(probability_bad: float) -> str:
    """Map probability to a human-readable risk tier."""
    if probability_bad >= 0.7:
        return "high"
    if probability_bad >= 0.4:
        return "medium"
    return "low"
