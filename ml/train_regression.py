#!/usr/bin/env python3
"""Treina regressão para prever rendimento agrícola (Cap 1)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import sys

TASK_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TASK_ROOT / "scripts"))
from paths import DEFAULT_CSV, METRICS_JSON, MODEL_PATH, MODELS_DIR  # noqa: E402

FEATURES = [
    "umidade_solo",
    "ph_solo",
    "nitrogenio",
    "fosforo",
    "potassio",
    "temperatura_c",
]
TARGET = "rendimento_t_ha"


def train(csv_path: Path = DEFAULT_CSV, model_path: Path = MODEL_PATH) -> dict:
    if not csv_path.is_file():
        raise FileNotFoundError(f"Dataset ausente: {csv_path}")

    df = pd.read_csv(csv_path)
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", RandomForestRegressor(n_estimators=120, random_state=42)),
        ]
    )
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    mae = float(mean_absolute_error(y_test, preds))
    mse = float(mean_squared_error(y_test, preds))
    rmse = float(mse**0.5)
    r2 = float(r2_score(y_test, preds))

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)

    metrics = {
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "model": "RandomForestRegressor",
        "target": TARGET,
        "features": FEATURES,
        "mae": round(mae, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4),
        "r2": round(r2, 4),
        "rows_train": len(X_train),
        "rows_test": len(X_test),
    }
    METRICS_JSON.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()
    train(args.csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
