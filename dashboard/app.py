"""Dashboard FarmTech Cap 1 — integração ML + Streamlit."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

TASK_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TASK_ROOT))

from ml.predict import FEATURES, predict_yield  # noqa: E402

DATA_CSV = TASK_ROOT / "data" / "leituras_sensores.csv"
DATA_DB = TASK_ROOT / "data" / "farmtech_iot.db"
METRICS_JSON = TASK_ROOT / "models" / "regression_metrics.json"


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_CSV.is_file():
        raise FileNotFoundError("Execute: python scripts/run_pipeline.py")
    return pd.read_csv(DATA_CSV)


@st.cache_data
def load_db_count() -> int | None:
    if not DATA_DB.is_file():
        return None
    with sqlite3.connect(DATA_DB) as conn:
        return int(conn.execute("SELECT COUNT(*) FROM leituras_sensores").fetchone()[0])


def main() -> None:
    st.set_page_config(page_title="FarmTech Cap 1", layout="wide")
    st.title("Assistente Agrícola Inteligente — Cap 1")
    st.caption("Regressão + métricas + recomendações de irrigação, manejo e fertilização")

    with st.sidebar:
        st.header("Pipeline técnico")
        st.write(
            "Pandas para tratamento, SQLite para armazenamento, Scikit-Learn para "
            "regressão e Streamlit para a interface."
        )
        st.code("python scripts/run_pipeline.py", language="bash")
        st.code("python scripts/ingest_iot.py", language="bash")

    try:
        df = load_data()
    except FileNotFoundError as exc:
        st.error(str(exc))
        return

    if METRICS_JSON.is_file():
        metrics = json.loads(METRICS_JSON.read_text(encoding="utf-8"))
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("MAE", metrics.get("mae", "-"))
        c2.metric("MSE", metrics.get("mse", "-"))
        c3.metric("RMSE", metrics.get("rmse", "-"))
        c4.metric("R²", metrics.get("r2", "-"))
        c5.metric("Linhas", len(df))

    db_count = load_db_count()
    if db_count is not None:
        st.caption(f"Banco SQLite populado: {db_count} leituras em data/farmtech_iot.db")

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
            st.info(
                f"Irrigação: {result['acao_manejo']} "
                f"({result['irrigacao_recomendada']}, aprox. "
                f"{result['irrigacao_litros_estimados']} L)"
            )
            st.warning(f"Manejo/fertilização: {result['manejo_nutrientes']}")

    with tab_corr:
        st.subheader("Correlação entre variáveis")
        st.dataframe(df[FEATURES + ["rendimento_t_ha"]].corr(), use_container_width=True)
        st.subheader("Relação entre umidade do solo e rendimento")
        st.scatter_chart(df, x="umidade_solo", y="rendimento_t_ha", color="talhao_id")
        st.subheader("Tendência de produtividade")
        trend = df.assign(data_hora=pd.to_datetime(df["data_hora"])).set_index("data_hora")
        st.line_chart(
            trend[["umidade_solo", "rendimento_t_ha", "irrigacao_sugerida_l"]].tail(120)
        )

    with tab_raw:
        st.dataframe(df.head(100), use_container_width=True)


if __name__ == "__main__":
    main()
