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
TARGETS = [
    "rendimento_t_ha",
    "irrigacao_sugerida_l",
    "fertilizacao_sugerida_kg_ha",
]


def train(csv_path: Path = DEFAULT_CSV, model_path: Path = MODEL_PATH) -> dict:
    if not csv_path.is_file():
        raise FileNotFoundError(f"Dataset ausente: {csv_path}")

    df = pd.read_csv(csv_path)
    X = df[FEATURES]
    y = df[TARGETS]
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

    mae_values = mean_absolute_error(y_test, preds, multioutput="raw_values")
    mse_values = mean_squared_error(y_test, preds, multioutput="raw_values")
    rmse_values = mse_values**0.5
    r2_values = r2_score(y_test, preds, multioutput="raw_values")
    target_metrics = {
        target: {
            "mae": round(float(mae_values[i]), 4),
            "mse": round(float(mse_values[i]), 4),
            "rmse": round(float(rmse_values[i]), 4),
            "r2": round(float(r2_values[i]), 4),
        }
        for i, target in enumerate(TARGETS)
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)

    metrics = {
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "model": "RandomForestRegressor multi-output",
        "target": TARGET,
        "targets": TARGETS,
        "features": FEATURES,
        "mae": target_metrics[TARGET]["mae"],
        "mse": target_metrics[TARGET]["mse"],
        "rmse": target_metrics[TARGET]["rmse"],
        "r2": target_metrics[TARGET]["r2"],
        "target_metrics": target_metrics,
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
