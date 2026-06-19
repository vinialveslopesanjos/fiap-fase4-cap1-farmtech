"""API de previsão para o dashboard (Cap 1)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

TASK_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = TASK_ROOT / "models" / "regression_model.joblib"

FEATURES = [
    "umidade_solo",
    "ph_solo",
    "nitrogenio",
    "fosforo",
    "potassio",
    "temperatura_c",
]


def load_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            "Modelo não treinado. Execute: python scripts/run_pipeline.py"
        )
    return joblib.load(MODEL_PATH)


def predict_yield(row: dict[str, Any]) -> dict[str, Any]:
    """Prevê rendimento e sugere ação de manejo simples."""
    model = load_model()
    frame = pd.DataFrame([{k: row[k] for k in FEATURES}])
    rendimento = float(model.predict(frame)[0])
    umidade = float(row.get("umidade_solo", 50))

    if umidade < 35:
        acao = "Aumentar irrigação nas próximas 24h"
        irrigacao = "alta"
    elif umidade > 70:
        acao = "Reduzir irrigação e monitorar drenagem"
        irrigacao = "baixa"
    else:
        acao = "Manter irrigação atual"
        irrigacao = "moderada"

    return {
        "rendimento_previsto_t_ha": round(rendimento, 2),
        "irrigacao_recomendada": irrigacao,
        "acao_manejo": acao,
    }
