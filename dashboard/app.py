"""Dashboard FarmTech Cap 1: integracao ML + Streamlit."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

TASK_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TASK_ROOT))

from ml.predict import FEATURES, predict_yield  # noqa: E402

DATA_CSV = TASK_ROOT / "data" / "leituras_sensores.csv"
DATA_DB = TASK_ROOT / "data" / "farmtech_iot.db"
METRICS_JSON = TASK_ROOT / "models" / "regression_metrics.json"

TARGET_COLS = [
    "rendimento_t_ha",
    "irrigacao_sugerida_l",
    "fertilizacao_sugerida_kg_ha",
]
CHART_OPTIONS = FEATURES + TARGET_COLS
LABELS = {
    "umidade_solo": "Umidade do solo (%)",
    "ph_solo": "pH do solo",
    "nitrogenio": "Nitrogenio",
    "fosforo": "Fosforo",
    "potassio": "Potassio",
    "temperatura_c": "Temperatura (C)",
    "rendimento_t_ha": "Rendimento (t/ha)",
    "irrigacao_sugerida_l": "Irrigacao (L)",
    "fertilizacao_sugerida_kg_ha": "Fertilizacao (kg/ha)",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_CSV.is_file():
        raise FileNotFoundError("Execute: python scripts/run_pipeline.py")
    df = pd.read_csv(DATA_CSV)
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    return df


def load_metrics() -> dict:
    if not METRICS_JSON.is_file():
        return {}
    return json.loads(METRICS_JSON.read_text(encoding="utf-8"))


def sqlite_count() -> int | None:
    if not DATA_DB.is_file():
        return None
    with sqlite3.connect(DATA_DB) as conn:
        return conn.execute("SELECT COUNT(*) FROM leituras_sensores").fetchone()[0]


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: #f6f8f3;
        }
        .block-container {
            max-width: 1180px;
            padding-top: 1.4rem;
            padding-bottom: 2rem;
        }
        .farm-hero {
            border: 1px solid #d9e7d1;
            border-left: 7px solid #2f855a;
            border-radius: 8px;
            padding: 1.05rem 1.25rem;
            background: linear-gradient(135deg, #f7fff4 0%, #edf8f1 56%, #fff7e7 100%);
            margin-bottom: 1rem;
        }
        .farm-hero h1 {
            color: #173d2a;
            font-size: 2rem;
            line-height: 1.15;
            margin: 0 0 .25rem 0;
            letter-spacing: 0;
        }
        .farm-hero p {
            color: #4a5f50;
            margin: 0;
            font-size: .98rem;
        }
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #dfe8d9;
            border-radius: 8px;
            padding: .85rem .9rem;
            box-shadow: 0 1px 2px rgba(24, 60, 42, .06);
        }
        div[data-testid="stMetricLabel"] p {
            color: #54705d;
            font-size: .82rem;
        }
        div[data-testid="stMetricValue"] {
            color: #173d2a;
            font-size: 1.45rem;
        }
        [data-testid="stSidebar"] {
            background: #eef5ea;
            border-right: 1px solid #d8e5d2;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: .35rem;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: .55rem .85rem;
        }
        .stTabs [aria-selected="true"] {
            color: #2f855a;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #2f855a;
        }
        span[data-baseweb="tag"] {
            background-color: #2f855a !important;
            border-radius: 6px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.header("Filtros")
        talhoes = sorted(df["talhao_id"].unique().tolist())
        selected_talhoes = st.multiselect("Talhoes", talhoes, default=talhoes)

        min_date = df["data_hora"].dt.date.min()
        max_date = df["data_hora"].dt.date.max()
        selected_dates = st.date_input("Periodo", value=(min_date, max_date))
        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
        else:
            start_date, end_date = min_date, max_date

        st.divider()
        st.caption("Use os filtros para simular a visao de um gestor por talhao e janela de tempo.")

    filtered = df[df["talhao_id"].isin(selected_talhoes)].copy()
    filtered = filtered[
        (filtered["data_hora"].dt.date >= start_date)
        & (filtered["data_hora"].dt.date <= end_date)
    ]
    return filtered if not filtered.empty else df.copy()


def scatter_chart(df: pd.DataFrame, x_axis: str, y_axis: str, color_axis: str) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_circle(size=58, opacity=0.72, stroke="#ffffff", strokeWidth=0.6)
        .encode(
            x=alt.X(x_axis, title=LABELS[x_axis], scale=alt.Scale(zero=False)),
            y=alt.Y(y_axis, title=LABELS[y_axis], scale=alt.Scale(zero=False)),
            color=alt.Color(color_axis, title=LABELS[color_axis], scale=alt.Scale(scheme="viridis")),
            tooltip=[
                alt.Tooltip("data_hora:T", title="Data"),
                alt.Tooltip("talhao_id:N", title="Talhao"),
                alt.Tooltip(x_axis, title=LABELS[x_axis], format=".2f"),
                alt.Tooltip(y_axis, title=LABELS[y_axis], format=".2f"),
                alt.Tooltip(color_axis, title=LABELS[color_axis], format=".2f"),
            ],
        )
        .properties(height=285)
        .interactive()
    )


def main() -> None:
    st.set_page_config(page_title="FarmTech Cap 1", layout="wide")
    apply_theme()

    st.markdown(
        """
        <div class="farm-hero">
            <h1>Assistente Agricola Inteligente</h1>
            <p>Previsao de rendimento, irrigacao e fertilizacao com dados simulados de sensores IoT.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        df = load_data()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    filtered_df = filter_data(df)
    metrics = load_metrics()
    db_rows = sqlite_count()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("MAE", metrics.get("mae", "-"))
    c2.metric("MSE", metrics.get("mse", "-"))
    c3.metric("RMSE", metrics.get("rmse", "-"))
    c4.metric("R2", metrics.get("r2", "-"))
    c5.metric("Leituras", len(filtered_df), help=f"SQLite total: {db_rows or '-'}")

    tab_prev, tab_corr, tab_trend, tab_raw = st.tabs(
        ["Previsao", "Correlacao", "Tendencias", "Dados"]
    )

    with tab_prev:
        left, right = st.columns([1.35, 1])
        with left:
            st.subheader("Simulador de manejo")
            st.caption("Ajuste os parametros do talhao e clique em simular para gerar uma nova recomendacao.")
            with st.form("form_simulador_manejo"):
                row = {}
                cols = st.columns(2)
                for i, feat in enumerate(FEATURES):
                    default = float(filtered_df[feat].median())
                    min_value = float(df[feat].min())
                    max_value = float(df[feat].max())
                    step = 0.1 if feat != "umidade_solo" else 1.0
                    row[feat] = cols[i % 2].number_input(
                        LABELS[feat],
                        min_value=min_value,
                        max_value=max_value,
                        value=default,
                        step=step,
                    )
                submitted = st.form_submit_button("Simular manejo", type="primary")

            if submitted:
                st.session_state["simulacao_manejo"] = {
                    "inputs": row,
                    "result": predict_yield(row),
                }

        with right:
            st.subheader("Resultado da simulacao")
            simulacao = st.session_state.get("simulacao_manejo")
            if simulacao is None:
                st.info("Preencha os parametros ao lado e clique em **Simular manejo**.")
                st.caption("O resultado fica salvo aqui ate a proxima simulacao.")
            else:
                result = simulacao["result"]
                r1, r2 = st.columns(2)
                r1.metric("Rendimento", f"{result['rendimento_previsto_t_ha']} t/ha")
                r2.metric("Potencial", result["potencial_produtivo"].title())
                r3, r4 = st.columns(2)
                r3.metric("Irrigacao", f"{result['irrigacao_prevista_l']:.0f} L")
                r4.metric("Fertilizacao", f"{result['fertilizacao_prevista_kg_ha']} kg/ha")
                st.info(
                    f"Irrigacao {result['irrigacao_recomendada']} | "
                    f"Fertilizacao {result['fertilizacao_recomendada']}"
                )
                st.success(result["acao_manejo"])

    with tab_corr:
        st.subheader("Analise interativa de correlacao")
        ctrl1, ctrl2, ctrl3 = st.columns(3)
        x_axis = ctrl1.selectbox("Eixo X", CHART_OPTIONS, index=0, format_func=LABELS.get)
        y_axis = ctrl2.selectbox("Eixo Y", CHART_OPTIONS, index=6, format_func=LABELS.get)
        color_axis = ctrl3.selectbox("Cor", CHART_OPTIONS, index=1, format_func=LABELS.get)

        chart_col, table_col = st.columns([1.25, 1])
        with chart_col:
            st.altair_chart(
                scatter_chart(filtered_df, x_axis, y_axis, color_axis),
                use_container_width=True,
            )
            st.caption("Grafico interativo: passe o mouse para detalhes e use scroll/arraste para explorar.")

        with table_col:
            st.dataframe(
                filtered_df[CHART_OPTIONS].corr().round(3),
                use_container_width=True,
                height=285,
            )

        target_metrics = metrics.get("target_metrics", {})
        if target_metrics:
            st.subheader("Metricas por previsao")
            st.dataframe(pd.DataFrame(target_metrics).T, use_container_width=True)

    with tab_trend:
        st.subheader("Tendencias de produtividade e manejo")
        daily = (
            filtered_df.set_index("data_hora")[
                [
                    "rendimento_t_ha",
                    "irrigacao_sugerida_l",
                    "fertilizacao_sugerida_kg_ha",
                ]
            ]
            .resample("D")
            .mean()
            .reset_index()
        )
        trend = (
            alt.Chart(daily)
            .transform_fold(
                ["rendimento_t_ha", "irrigacao_sugerida_l", "fertilizacao_sugerida_kg_ha"],
                as_=["variavel", "valor"],
            )
            .mark_line(point=True)
            .encode(
                x=alt.X("data_hora:T", title="Data"),
                y=alt.Y("valor:Q", title="Media diaria"),
                color=alt.Color("variavel:N", title="Indicador"),
                tooltip=[
                    alt.Tooltip("data_hora:T", title="Data"),
                    alt.Tooltip("variavel:N", title="Indicador"),
                    alt.Tooltip("valor:Q", title="Valor", format=".2f"),
                ],
            )
            .properties(height=320)
            .interactive()
        )
        st.altair_chart(trend, use_container_width=True)

    with tab_raw:
        st.dataframe(filtered_df.head(150), use_container_width=True, height=460)


if __name__ == "__main__":
    main()
