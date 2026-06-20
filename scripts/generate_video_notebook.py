#!/usr/bin/env python3
"""Gera notebook e HTML de apoio para a gravacao do video."""

from __future__ import annotations

import base64
import html
import json
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from paths import DEFAULT_CSV, ENTREGA_DIR, METRICS_JSON

OUT_IPYNB = ENTREGA_DIR / "farmtech_analise_video.ipynb"
OUT_HTML = ENTREGA_DIR / "farmtech_analise_video.html"

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
LABELS = {
    "umidade_solo": "Umidade",
    "ph_solo": "pH",
    "nitrogenio": "Nitrogenio",
    "fosforo": "Fosforo",
    "potassio": "Potassio",
    "temperatura_c": "Temperatura",
    "rendimento_t_ha": "Rendimento",
    "irrigacao_sugerida_l": "Irrigacao",
    "fertilizacao_sugerida_kg_ha": "Fertilizacao",
}


def fig_to_base64(fig) -> str:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=145, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def metrics_table(metrics: dict) -> pd.DataFrame:
    target_metrics = metrics.get("target_metrics", {})
    table = pd.DataFrame(target_metrics).T
    table.index = [
        "Rendimento (t/ha)",
        "Irrigacao (L)",
        "Fertilizacao (kg/ha)",
    ]
    return table[["mae", "mse", "rmse", "r2"]].round(4)


def correlation_image(df: pd.DataFrame) -> str:
    cols = FEATURES + TARGETS
    corr = df[cols].corr()
    labels = [LABELS[col] for col in cols]

    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    image = ax.imshow(corr, cmap="YlGn", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)), labels=labels, rotation=45, ha="right")
    ax.set_yticks(range(len(cols)), labels=labels)
    ax.set_title("Matriz de correlacao dos sensores e previsoes")

    for y in range(len(cols)):
        for x in range(len(cols)):
            value = corr.iloc[y, x]
            ax.text(x, y, f"{value:.2f}", ha="center", va="center", fontsize=8)

    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    return fig_to_base64(fig)


def scatter_image(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    points = ax.scatter(
        df["umidade_solo"],
        df["rendimento_t_ha"],
        c=df["ph_solo"],
        cmap="viridis",
        alpha=0.72,
        s=28,
        edgecolors="white",
        linewidths=0.35,
    )
    ax.set_title("Umidade do solo x rendimento previsto")
    ax.set_xlabel("Umidade do solo (%)")
    ax.set_ylabel("Rendimento (t/ha)")
    ax.grid(True, alpha=0.25)
    fig.colorbar(points, ax=ax, label="pH do solo")
    return fig_to_base64(fig)


def trend_image(df: pd.DataFrame) -> str:
    daily = (
        df.set_index("data_hora")[TARGETS]
        .resample("D")
        .mean()
        .rename(
            columns={
                "rendimento_t_ha": "Rendimento (t/ha)",
                "irrigacao_sugerida_l": "Irrigacao (L)",
                "fertilizacao_sugerida_kg_ha": "Fertilizacao (kg/ha)",
            }
        )
    )

    fig, axes = plt.subplots(3, 1, figsize=(8.4, 6.2), sharex=True)
    colors = ["#2f855a", "#2b6cb0", "#b7791f"]
    for ax, column, color in zip(axes, daily.columns, colors):
        ax.plot(daily.index, daily[column], marker="o", linewidth=2, color=color)
        ax.set_ylabel(column)
        ax.grid(True, alpha=0.25)
    axes[0].set_title("Tendencias medias por dia")
    axes[-1].set_xlabel("Data")
    fig.autofmt_xdate()
    return fig_to_base64(fig)


def markdown_cell(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(True)}


def code_cell(source: str, outputs: list[dict], execution_count: int) -> dict:
    return {
        "cell_type": "code",
        "execution_count": execution_count,
        "metadata": {},
        "outputs": outputs,
        "source": source.splitlines(True),
    }


def image_output(base64_png: str) -> dict:
    return {
        "data": {"image/png": base64_png},
        "metadata": {},
        "output_type": "display_data",
    }


def html_output(content: str) -> dict:
    return {
        "data": {"text/html": content, "text/plain": "Tabela de metricas do modelo"},
        "metadata": {},
        "output_type": "display_data",
    }


def build_html(table_html: str, images: dict[str, str]) -> str:
    sections = [
        ("Metricas do modelo", table_html),
        ("Correlacao entre sensores e previsoes", f'<img src="data:image/png;base64,{images["corr"]}">'),
        ("Umidade x rendimento", f'<img src="data:image/png;base64,{images["scatter"]}">'),
        ("Tendencias por dia", f'<img src="data:image/png;base64,{images["trend"]}">'),
    ]
    body = "\n".join(
        f"<section><h2>{html.escape(title)}</h2>{content}</section>"
        for title, content in sections
    )
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>FarmTech - Analise para Video</title>
  <style>
    body {{
      margin: 0;
      background: #f6f8f3;
      color: #173d2a;
      font-family: Arial, sans-serif;
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 32px 24px 48px;
    }}
    header {{
      border-left: 7px solid #2f855a;
      background: linear-gradient(135deg, #f7fff4, #edf8f1 56%, #fff7e7);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 22px;
    }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    h2 {{ margin: 0 0 14px; font-size: 22px; }}
    p {{ color: #4a5f50; }}
    section {{
      background: #fff;
      border: 1px solid #dfe8d9;
      border-radius: 8px;
      padding: 18px 20px;
      margin: 18px 0;
      box-shadow: 0 1px 2px rgba(24, 60, 42, .06);
    }}
    img {{ max-width: 100%; display: block; margin: 0 auto; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #dfe8d9; padding: 8px 10px; text-align: right; }}
    th:first-child, td:first-child {{ text-align: left; }}
    th {{ background: #eef5ea; }}
  </style>
</head>
<body>
<main>
  <header>
    <h1>FarmTech - Analise de apoio para o video</h1>
    <p>Graficos essenciais para explicar o pipeline de ML, as metricas e as recomendacoes de manejo.</p>
  </header>
  {body}
</main>
</body>
</html>
"""


def main() -> int:
    if not DEFAULT_CSV.is_file() or not METRICS_JSON.is_file():
        raise SystemExit("Rode antes: python scripts/run_pipeline.py")

    ENTREGA_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DEFAULT_CSV, parse_dates=["data_hora"])
    metrics = json.loads(METRICS_JSON.read_text(encoding="utf-8"))
    table = metrics_table(metrics)
    table_html = table.to_html(classes="metrics", border=0)
    images = {
        "corr": correlation_image(df),
        "scatter": scatter_image(df),
        "trend": trend_image(df),
    }

    cells = [
        markdown_cell(
            "# FarmTech - Analise para o video\n\n"
            "Notebook de apoio com os graficos essenciais da entrega: metricas, "
            "correlacao, dispersao e tendencias."
        ),
        code_cell(
            "import pandas as pd\n"
            "df = pd.read_csv('data/leituras_sensores.csv', parse_dates=['data_hora'])\n"
            "df.head()",
            [],
            1,
        ),
        markdown_cell("## Metricas do modelo\n\nUse esta tabela para comentar MAE, MSE, RMSE e R2."),
        code_cell("metricas_por_alvo", [html_output(table_html)], 2),
        markdown_cell("## Correlacao\n\nMostra a relacao entre sensores, rendimento e recomendacoes."),
        code_cell("matriz_correlacao", [image_output(images["corr"])], 3),
        markdown_cell("## Umidade x rendimento\n\nGrafico simples para explicar como a umidade influencia a produtividade."),
        code_cell("dispersao_umidade_rendimento", [image_output(images["scatter"])], 4),
        markdown_cell("## Tendencias\n\nResumo diario de rendimento, irrigacao e fertilizacao."),
        code_cell("tendencias_diarias", [image_output(images["trend"])], 5),
    ]

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    OUT_IPYNB.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_HTML.write_text(build_html(table_html, images), encoding="utf-8")
    print(f"[ok] notebook -> {OUT_IPYNB.relative_to(ENTREGA_DIR.parent)}")
    print(f"[ok] html -> {OUT_HTML.relative_to(ENTREGA_DIR.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
