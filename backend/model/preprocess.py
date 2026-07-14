"""Preprocessing and feature engineering for credit risk modeling."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from model.config import (
    CATEGORICAL_FEATURES,
    ENGINEERED_FEATURES,
    MATURE_AGE_THRESHOLD,
    NUMERIC_FEATURES,
    YOUNG_AGE_THRESHOLD,
)

logger = logging.getLogger(__name__)


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Create simple, interview-friendly engineered features.

    All transformations are easy to explain to stakeholders:
    - credit_per_duration: monthly payment burden proxy
    - long_term_loan: duration above dataset median
    - high_credit_amount: loan size above dataset median
    - young_applicant / mature_applicant: age-based risk segments
    """

    def fit(
        self,
        X: pd.DataFrame,
        y: np.ndarray | pd.Series | None = None,
    ) -> FeatureEngineer:
        self.duration_median_ = float(X["duration"].median())
        self.credit_median_ = float(X["credit_amount"].median())
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        safe_duration = X["duration"].replace(0, 1)
        X["credit_per_duration"] = X["credit_amount"] / safe_duration
        X["long_term_loan"] = (X["duration"] > self.duration_median_).astype(int)
        X["high_credit_amount"] = (X["credit_amount"] > self.credit_median_).astype(
            int
        )
        X["young_applicant"] = (X["age"] < YOUNG_AGE_THRESHOLD).astype(int)
        X["mature_applicant"] = (X["age"] >= MATURE_AGE_THRESHOLD).astype(int)
        return X

    def get_feature_names_out(self, input_features: list[str] | None = None) -> np.ndarray:
        base = list(input_features) if input_features is not None else []
        return np.array(base + ENGINEERED_FEATURES)


def _numeric_pipeline(scale: bool) -> Pipeline:
    steps: list[tuple[str, Any]] = [
        ("imputer", SimpleImputer(strategy="median")),
    ]
    if scale:
        steps.append(("scaler", StandardScaler()))
    return Pipeline(steps)


def _categorical_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )


def build_preprocessor(scale_numeric: bool = False) -> Pipeline:
    """
    Build a reusable preprocessing pipeline.

    Args:
        scale_numeric: Apply StandardScaler to numeric columns.
            Recommended for Logistic Regression; optional for tree models.

    Returns:
        Fitted-ready sklearn Pipeline with feature engineering and encoding.
    """
    numeric_cols = NUMERIC_FEATURES + ENGINEERED_FEATURES
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", _numeric_pipeline(scale_numeric), numeric_cols),
            ("cat", _categorical_pipeline(), CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )

    pipeline = Pipeline(
        [
            ("feature_engineering", FeatureEngineer()),
            ("column_transformer", preprocessor),
        ]
    )
    logger.debug(
        "Built preprocessor (scale_numeric=%s) with %d numeric and %d categorical columns",
        scale_numeric,
        len(numeric_cols),
        len(CATEGORICAL_FEATURES),
    )
    return pipeline


def get_feature_names(preprocessor: Pipeline) -> list[str]:
    """Extract output feature names from a fitted preprocessing pipeline."""
    column_transformer: ColumnTransformer = preprocessor.named_steps["column_transformer"]
    return list(column_transformer.get_feature_names_out())


def split_features_target(
    df: pd.DataFrame,
    target_column: str,
) -> tuple[pd.DataFrame, pd.Series]:
    """Separate feature matrix and target vector."""
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y
