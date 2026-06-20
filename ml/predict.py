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
    """Prevê rendimento e sugere ações simples de irrigação e manejo."""
    model = load_model()
    frame = pd.DataFrame([{k: row[k] for k in FEATURES}])
    rendimento = float(model.predict(frame)[0])
    umidade = float(row.get("umidade_solo", 50))
    ph = float(row.get("ph_solo", 6.5))
    nitrogenio = float(row.get("nitrogenio", 60))
    fosforo = float(row.get("fosforo", 40))
    potassio = float(row.get("potassio", 100))
    irrigacao_litros = max(50, min(1200, 800 - 6 * umidade))

    if umidade < 35:
        acao = "Aumentar irrigação nas próximas 24h"
        irrigacao = "alta"
    elif umidade > 70:
        acao = "Reduzir irrigação e monitorar drenagem"
        irrigacao = "baixa"
    else:
        acao = "Manter irrigação atual"
        irrigacao = "moderada"

    manejo_nutrientes: list[str] = []
    if ph < 5.5:
        manejo_nutrientes.append("corrigir acidez do solo antes de intensificar adubação")
    elif ph > 7.4:
        manejo_nutrientes.append("monitorar alcalinidade e disponibilidade de nutrientes")

    if nitrogenio < 45:
        manejo_nutrientes.append("avaliar reforço de nitrogênio")
    if fosforo < 25:
        manejo_nutrientes.append("avaliar reforço de fósforo")
    if potassio < 70:
        manejo_nutrientes.append("avaliar reforço de potássio")

    if manejo_nutrientes:
        manejo = "; ".join(manejo_nutrientes).capitalize()
    else:
        manejo = "Manter plano de fertilização atual e seguir monitoramento"

    return {
        "rendimento_previsto_t_ha": round(rendimento, 2),
        "irrigacao_recomendada": irrigacao,
        "irrigacao_litros_estimados": round(irrigacao_litros, 0),
        "acao_manejo": acao,
        "manejo_nutrientes": manejo,
    }
