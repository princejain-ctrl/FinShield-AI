"""Shared utility functions for the FinSecure AI ML pipeline."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.datasets import fetch_openml

from model.config import (
    DATASET_CSV,
    METADATA_PATH,
    OPENML_NAME,
    OPENML_VERSION,
    PREPROCESSOR_PATH,
    TARGET_COLUMN,
    TRAINED_MODEL_PATH,
)

logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger with a consistent format."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def ensure_directories(*paths: Path) -> None:
    """Create directories if they do not exist."""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def load_dataset(force_download: bool = False) -> pd.DataFrame:
    """
    Load the German Credit dataset from a local CSV or OpenML.

    Args:
        force_download: When True, re-fetch from OpenML even if CSV exists.

    Returns:
        DataFrame containing features and target column.
    """
    if DATASET_CSV.exists() and not force_download:
        logger.info("Loading dataset from %s", DATASET_CSV)
        return pd.read_csv(DATASET_CSV)

    logger.info(
        "Fetching dataset '%s' (version %s) from OpenML",
        OPENML_NAME,
        OPENML_VERSION,
    )
    bundle = fetch_openml(
        name=OPENML_NAME,
        version=OPENML_VERSION,
        as_frame=True,
    )
    df = pd.concat([bundle.data, bundle.target], axis=1)
    df.columns = [str(col) for col in df.columns]

    ensure_directories(DATASET_CSV.parent)
    df.to_csv(DATASET_CSV, index=False)
    logger.info("Saved dataset to %s (%d rows)", DATASET_CSV, len(df))
    return df


def encode_target(series: pd.Series) -> pd.Series:
    """
    Encode target labels to binary integers.

    ``bad`` (higher risk) -> 1, ``good`` -> 0.
    """
    mapping = {"bad": 1, "good": 0}
    encoded = series.map(mapping)
    if encoded.isna().any():
        unknown = series[encoded.isna()].unique()
        raise ValueError(f"Unknown target labels: {unknown}")
    return encoded.astype(int)


def save_pickle(obj: Any, path: Path) -> None:
    """Persist an object with joblib."""
    ensure_directories(path.parent)
    joblib.dump(obj, path)
    logger.info("Saved artifact to %s", path)


def load_pickle(path: Path) -> Any:
    """Load a joblib-serialized object."""
    if not path.exists():
        raise FileNotFoundError(f"Artifact not found: {path}")
    return joblib.load(path)


def save_metadata(metadata: dict[str, Any]) -> None:
    """Write model metadata as JSON."""
    ensure_directories(METADATA_PATH.parent)
    with METADATA_PATH.open("w", encoding="utf-8") as fh:
        json.dump(metadata, fh, indent=2)
    logger.info("Saved metadata to %s", METADATA_PATH)


def load_metadata() -> dict[str, Any]:
    """Load model metadata from disk."""
    if not METADATA_PATH.exists():
        raise FileNotFoundError(f"Metadata not found: {METADATA_PATH}")
    with METADATA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def artifacts_exist() -> bool:
    """Return True when all required model artifacts are present."""
    return all(
        path.exists()
        for path in (TRAINED_MODEL_PATH, PREPROCESSOR_PATH, METADATA_PATH)
    )
