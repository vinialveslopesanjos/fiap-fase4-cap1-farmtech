#!/usr/bin/env python3
"""Verifica gates do harness Cap 1 antes da entrega."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import pandas as pd

TASK_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TASK_ROOT / "scripts"))
from paths import (  # noqa: E402
    DASHBOARD_APP,
    DEFAULT_CSV,
    DEFAULT_DB,
    METRICS_JSON,
    MODEL_PATH,
    SCHEMA_SQL,
)

REQUIRED_TARGET_COLUMNS = {
    "rendimento_t_ha",
    "irrigacao_sugerida_l",
    "fertilizacao_sugerida_kg_ha",
}


def check_gate(name: str, ok: bool, detail: str = "") -> bool:
    status = "OK" if ok else "FALHA"
    suffix = f" - {detail}" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", choices=["all"], default="all")
    args = parser.parse_args()

    print("Harness Cap 1 - gates\n")
    ok = True

    if args.role == "all":
        print("Pipeline e modelo:")
        ok &= check_gate("G1 dataset", DEFAULT_CSV.is_file(), str(DEFAULT_CSV))
        if DEFAULT_CSV.is_file():
            columns = set(pd.read_csv(DEFAULT_CSV, nrows=0).columns)
            missing = sorted(REQUIRED_TARGET_COLUMNS - columns)
            ok &= check_gate(
                "G1.1 colunas de previsao",
                not missing,
                f"faltando: {', '.join(missing)}"
                if missing
                else "rendimento, irrigacao, fertilizacao",
            )
        ok &= check_gate("G2 modelo", MODEL_PATH.is_file())
        if METRICS_JSON.is_file():
            metrics = json.loads(METRICS_JSON.read_text(encoding="utf-8"))
            ok &= check_gate("G3 metricas", "r2" in metrics, f"R2={metrics.get('r2')}")
            target_metrics = metrics.get("target_metrics", {})
            ok &= check_gate(
                "G3.1 metricas por alvo",
                REQUIRED_TARGET_COLUMNS.issubset(target_metrics),
                ", ".join(target_metrics.keys()) if target_metrics else "rode run_pipeline.py",
            )
        else:
            ok &= check_gate("G3 metricas", False, "rode run_pipeline.py")

    if args.role == "all":
        print("\nDashboard:")
        ok &= check_gate("G4 dashboard/app.py", DASHBOARD_APP.is_file())
        figures = TASK_ROOT / "figures"
        ok &= check_gate("G5 figures/ opcional", figures.is_dir(), "criar PNGs se PC leve")

    if args.role == "all":
        print("\nEntrega:")
        video = TASK_ROOT / "link_video.txt"
        ok &= check_gate("G9 link_video.txt", video.is_file(), "preencher antes do portal")
        ok &= check_gate("G8 checklist portal", (TASK_ROOT / "entrega" / "CHECKLIST_PORTAL.md").is_file())

    if args.role == "all":
        print("\nSQL e dados:")
        ok &= check_gate("G6 schema SQL", SCHEMA_SQL.is_file())
        ok &= check_gate("G7 SQLite", DEFAULT_DB.is_file(), "rode ingest_iot.py")
        if DEFAULT_DB.is_file():
            with sqlite3.connect(DEFAULT_DB) as conn:
                db_count = conn.execute("SELECT COUNT(*) FROM leituras_sensores").fetchone()[0]
            ok &= check_gate("G7.1 leituras SQLite", db_count >= 200, f"{db_count} linhas")
        queries = TASK_ROOT / "sql" / "02_queries.sql"
        ok &= check_gate("G8 queries SQL", queries.is_file())
        ok &= check_gate("G9 data_dictionary", (TASK_ROOT / "docs" / "data_dictionary.md").is_file())

    print()
    if ok:
        print("Todos os gates obrigatorios passaram.")
        return 0
    print("Corrija as falhas acima antes do portal.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
