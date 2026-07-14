"""Training pipeline for FinSecure AI credit risk models."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from model.config import (
    DATA_DIR,
    DOCS_DIR,
    FEATURE_IMPORTANCE_PATH,
    LOGISTIC_REGRESSION_PARAMS,
    PREPROCESSOR_PATH,
    RANDOM_STATE,
    METADATA_PATH,
    SAVED_MODEL_DIR,
    SHAP_SUMMARY_PATH,
    TARGET_COLUMN,
    TEST_SIZE,
    TRAINED_MODEL_PATH,
    XGBOOST_PARAMS,
)
from model.evaluate import (
    build_comparison_table,
    metrics_to_serializable,
    print_evaluation_report,
    select_final_model_rationale,
)
from model.preprocess import build_preprocessor, get_feature_names, split_features_target
from model.utils import (
    encode_target,
    ensure_directories,
    load_dataset,
    save_metadata,
    save_pickle,
    setup_logging,
)

logger = logging.getLogger(__name__)


def _train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """80/20 stratified train-test split."""
    return train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )


def train_baseline(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[Pipeline, dict[str, float]]:
    """Train and evaluate a Logistic Regression baseline."""
    pipeline = Pipeline(
        [
            ("preprocessor", build_preprocessor(scale_numeric=True)),
            (
                "classifier",
                LogisticRegression(**LOGISTIC_REGRESSION_PARAMS),
            ),
        ]
    )
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    metrics = print_evaluation_report("Logistic Regression (Baseline)", y_test, y_pred, y_proba)
    return pipeline, metrics


def train_xgboost(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[xgb.XGBClassifier, Any, dict[str, float]]:
    """Train and evaluate the final XGBoost classifier."""
    preprocessor = build_preprocessor(scale_numeric=False)
    X_train_processed = preprocessor.fit_transform(X_train, y_train)
    X_test_processed = preprocessor.transform(X_test)

    model = xgb.XGBClassifier(**XGBOOST_PARAMS)
    model.fit(X_train_processed, y_train)

    y_pred = model.predict(X_test_processed)
    y_proba = model.predict_proba(X_test_processed)[:, 1]
    metrics = print_evaluation_report("XGBoost (Final Model)", y_test, y_pred, y_proba)
    return model, preprocessor, metrics


def plot_feature_importance(
    model: xgb.XGBClassifier,
    feature_names: list[str],
    output_path: str | Any = FEATURE_IMPORTANCE_PATH,
    top_n: int = 20,
) -> None:
    """Generate and save a horizontal bar chart of feature importances."""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]

    fig, ax = plt.subplots(figsize=(10, 8))
    y_pos = np.arange(len(indices))
    ax.barh(
        y_pos,
        importances[indices],
        color="#2563eb",
        align="center",
    )
    ax.set_yticks(y_pos)
    ax.set_yticklabels([feature_names[i] for i in indices])
    ax.invert_yaxis()
    ax.set_xlabel("Importance")
    ax.set_title("XGBoost Feature Importance (Top 20)")
    plt.tight_layout()

    ensure_directories(output_path.parent)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved feature importance plot to %s", output_path)


def generate_shap_summary(
    model: xgb.XGBClassifier,
    X_sample: np.ndarray,
    feature_names: list[str],
    output_path: str | Any = SHAP_SUMMARY_PATH,
    max_samples: int = 200,
) -> shap.Explainer:
    """
    Generate SHAP summary plot and return a reusable explainer.

    Uses TreeExplainer for efficient computation on tree models.
    """
    if len(X_sample) > max_samples:
        rng = np.random.default_rng(RANDOM_STATE)
        sample_idx = rng.choice(len(X_sample), size=max_samples, replace=False)
        X_sample = X_sample[sample_idx]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)

    fig, ax = plt.subplots(figsize=(10, 8))
    shap.summary_plot(
        shap_values,
        X_sample,
        feature_names=feature_names,
        show=False,
        max_display=20,
    )
    plt.tight_layout()
    ensure_directories(output_path.parent)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info("Saved SHAP summary plot to %s", output_path)
    return explainer


def run_training() -> dict[str, Any]:
    """
    Execute the full training pipeline.

    Returns:
        Dictionary containing metrics, comparison table, and artifact paths.
    """
    setup_logging()
    ensure_directories(DATA_DIR, DOCS_DIR, SAVED_MODEL_DIR)

    logger.info("Starting FinSecure AI training pipeline")
    df = load_dataset()
    logger.info("Dataset shape: %s", df.shape)

    y = encode_target(df[TARGET_COLUMN])
    X, _ = split_features_target(df, TARGET_COLUMN)

    X_train, X_test, y_train, y_test = _train_test_split(X, y)
    logger.info(
        "Train size: %d | Test size: %d | Bad credit rate (train): %.2f%%",
        len(X_train),
        len(X_test),
        100 * y_train.mean(),
    )

    _, baseline_metrics = train_baseline(X_train, y_train, X_test, y_test)
    final_model, preprocessor, final_metrics = train_xgboost(
        X_train, y_train, X_test, y_test
    )

    comparison = build_comparison_table(baseline_metrics, final_metrics)
    logger.info("\n%s", comparison.to_string())
    rationale = select_final_model_rationale(baseline_metrics, final_metrics)
    logger.info("\n%s", rationale)

    feature_names = get_feature_names(preprocessor)
    plot_feature_importance(final_model, feature_names)

    X_train_processed = preprocessor.transform(X_train)
    explainer = generate_shap_summary(final_model, X_train_processed, feature_names)

    save_pickle(final_model, TRAINED_MODEL_PATH)
    save_pickle(preprocessor, PREPROCESSOR_PATH)
    save_pickle(explainer, SAVED_MODEL_DIR / "shap_explainer.pkl")

    metadata = {
        "model_type": "XGBClassifier",
        "target_column": TARGET_COLUMN,
        "positive_class": "bad",
        "negative_class": "good",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "feature_names": feature_names,
        "baseline_metrics": metrics_to_serializable(baseline_metrics),
        "final_metrics": metrics_to_serializable(final_metrics),
        "model_comparison": comparison.reset_index().to_dict(orient="records"),
        "selection_rationale": rationale,
        "xgboost_params": XGBOOST_PARAMS,
    }
    save_metadata(metadata)

    logger.info("Training complete. Artifacts saved to %s", SAVED_MODEL_DIR)
    return {
        "baseline_metrics": baseline_metrics,
        "final_metrics": final_metrics,
        "comparison": comparison,
        "rationale": rationale,
        "artifacts": {
            "model": str(TRAINED_MODEL_PATH),
            "preprocessor": str(PREPROCESSOR_PATH),
            "metadata": str(METADATA_PATH),
            "feature_importance": str(FEATURE_IMPORTANCE_PATH),
            "shap_summary": str(SHAP_SUMMARY_PATH),
        },
    }


if __name__ == "__main__":
    results = run_training()
    print("\n" + "=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)
    print("\nModel Comparison:")
    print(results["comparison"].to_string())
    print(f"\n{results['rationale']}")
    print("\nGenerated Artifacts:")
    for name, path in results["artifacts"].items():
        print(f"  - {name}: {path}")
