"""Dashboard FarmTech Cap 1 — integração ML + Streamlit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

TASK_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TASK_ROOT))

from ml.predict import FEATURES, predict_yield  # noqa: E402

DATA_CSV = TASK_ROOT / "data" / "leituras_sensores.csv"
METRICS_JSON = TASK_ROOT / "models" / "regression_metrics.json"


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_CSV.is_file():
        raise FileNotFoundError("Execute: python scripts/run_pipeline.py")
    return pd.read_csv(DATA_CSV)


def main() -> None:
    st.set_page_config(page_title="FarmTech Cap 1", layout="wide")
    st.title("Assistente Agrícola Inteligente — Cap 1")
    st.caption("Regressão + métricas + recomendações de manejo")

    try:
        df = load_data()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    if METRICS_JSON.is_file():
        metrics = json.loads(METRICS_JSON.read_text(encoding="utf-8"))
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("MAE", metrics.get("mae", "-"))
        c2.metric("RMSE", metrics.get("rmse", "-"))
        c3.metric("R²", metrics.get("r2", "-"))
        c4.metric("Linhas", len(df))

    tab_prev, tab_corr, tab_raw = st.tabs(["Previsão", "Correlação", "Dados"])

    with tab_prev:
        st.subheader("Simulador de previsão")
        row = {}
        cols = st.columns(3)
        for i, feat in enumerate(FEATURES):
            default = float(df[feat].median())
            row[feat] = cols[i % 3].number_input(feat, value=default)
        if st.button("Prever rendimento"):
            result = predict_yield(row)
            st.success(
                f"Rendimento previsto: **{result['rendimento_previsto_t_ha']} t/ha**"
            )
            st.info(f"Ação: {result['acao_manejo']} ({result['irrigacao_recomendada']})")

    with tab_corr:
        st.subheader("Correlação entre variáveis")
        st.dataframe(df[FEATURES + ["rendimento_t_ha"]].corr(), use_container_width=True)
        st.line_chart(df[["umidade_solo", "rendimento_t_ha"]].tail(80))

    with tab_raw:
        st.dataframe(df.head(100), use_container_width=True)


if __name__ == "__main__":
    main()
