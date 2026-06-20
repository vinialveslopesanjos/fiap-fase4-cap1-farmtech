#!/usr/bin/env python3
"""Verifica gates do harness Cap 1 (rodar antes de PR ou entrega)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

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


def check_gate(name: str, ok: bool, detail: str = "") -> bool:
    status = "OK" if ok else "FALHA"
    suffix = f" — {detail}" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", choices=["higor", "igor", "humberto", "all"], default="all")
    args = parser.parse_args()

    print("Harness Cap 1 — gates\n")
    ok = True

    if args.role in ("all", "higor"):
        print("Higor (ML + pipeline):")
        ok &= check_gate("G1 dataset", DEFAULT_CSV.is_file(), str(DEFAULT_CSV))
        ok &= check_gate("G2 modelo", MODEL_PATH.is_file())
        if METRICS_JSON.is_file():
            metrics = json.loads(METRICS_JSON.read_text(encoding="utf-8"))
            ok &= check_gate("G3 métricas", "r2" in metrics, f"R²={metrics.get('r2')}")
        else:
            ok &= check_gate("G3 métricas", False, "rode run_pipeline.py")

    if args.role in ("all", "igor"):
        print("\nIgor (dashboard):")
        ok &= check_gate("G4 dashboard/app.py", DASHBOARD_APP.is_file())
        figures = TASK_ROOT / "figures"
        ok &= check_gate("G5 figures/ (opcional)", figures.is_dir(), "criar PNGs se PC leve")

    if args.role in ("all", "higor"):
        print("\nHigor (entrega):")
        video = TASK_ROOT / "link_video.txt"
        ok &= check_gate("G9 link_video.txt", video.is_file(), "preencher antes do portal")
        ok &= check_gate("G8 checklist portal", (TASK_ROOT / "entrega" / "CHECKLIST_PORTAL.md").is_file())

    if args.role in ("all", "humberto"):
        print("\nHumberto (SQL):")
        ok &= check_gate("G6 schema SQL", SCHEMA_SQL.is_file())
        ok &= check_gate("G7 SQLite", DEFAULT_DB.is_file(), "rode ingest_iot.py")
        queries = TASK_ROOT / "sql" / "02_queries.sql"
        ok &= check_gate("G8 queries SQL", queries.is_file())
        ok &= check_gate("G9 data_dictionary", (TASK_ROOT / "docs" / "data_dictionary.md").is_file())

    print()
    if ok:
        print("Todos os gates obrigatórios passaram.")
        return 0
    print("Corrija as falhas acima antes do merge/portal.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
