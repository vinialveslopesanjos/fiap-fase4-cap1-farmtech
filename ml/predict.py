"""API de previsao para o dashboard (Cap 1)."""

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
TARGETS = [
    "rendimento_t_ha",
    "irrigacao_sugerida_l",
    "fertilizacao_sugerida_kg_ha",
]


def load_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError("Modelo nao treinado. Execute: python scripts/run_pipeline.py")
    return joblib.load(MODEL_PATH)


def predict_yield(row: dict[str, Any]) -> dict[str, Any]:
    """Preve rendimento, irrigacao e fertilizacao para o dashboard."""
    model = load_model()
    frame = pd.DataFrame([{k: row[k] for k in FEATURES}])
    prediction = model.predict(frame)[0]
    try:
        rendimento, irrigacao_litros, fertilizacao_kg_ha = [float(v) for v in prediction]
    except TypeError:
        rendimento = float(prediction)
        umidade_fallback = float(row.get("umidade_solo", 50))
        irrigacao_litros = max(50, min(1200, 800 - 6 * umidade_fallback))
        fertilizacao_kg_ha = 0.0

    umidade = float(row.get("umidade_solo", 50))
    ph = float(row.get("ph_solo", 6.5))
    nitrogenio = float(row.get("nitrogenio", 60))
    fosforo = float(row.get("fosforo", 35))
    potassio = float(row.get("potassio", 100))

    if irrigacao_litros >= 650 or umidade < 35:
        irrigacao = "alta"
        acao_irrigacao = "Aumentar irrigacao nas proximas 24h"
    elif irrigacao_litros <= 300 or umidade > 70:
        irrigacao = "baixa"
        acao_irrigacao = "Reduzir irrigacao e monitorar drenagem"
    else:
        irrigacao = "moderada"
        acao_irrigacao = "Manter irrigacao atual"

    if fertilizacao_kg_ha >= 35 or min(nitrogenio, fosforo, potassio) < 35:
        fertilizacao = "reforcar NPK"
        acao_fertilizacao = "Planejar reposicao de nutrientes"
    elif fertilizacao_kg_ha <= 8:
        fertilizacao = "manter"
        acao_fertilizacao = "Manter adubacao de manutencao"
    else:
        fertilizacao = "moderada"
        acao_fertilizacao = "Aplicar fertilizacao complementar"

    if ph < 5.5:
        acao_ph = "avaliar correcao de acidez do solo"
    elif ph > 7.2:
        acao_ph = "monitorar alcalinidade do solo"
    else:
        acao_ph = "pH dentro da faixa operacional"

    if rendimento >= 7:
        potencial = "alto"
    elif rendimento >= 5:
        potencial = "medio"
    else:
        potencial = "baixo"

    return {
        "rendimento_previsto_t_ha": round(rendimento, 2),
        "irrigacao_prevista_l": round(irrigacao_litros, 0),
        "fertilizacao_prevista_kg_ha": round(fertilizacao_kg_ha, 1),
        "irrigacao_recomendada": irrigacao,
        "fertilizacao_recomendada": fertilizacao,
        "potencial_produtivo": potencial,
        "acao_manejo": f"{acao_irrigacao}; {acao_fertilizacao}; {acao_ph}.",
    }
