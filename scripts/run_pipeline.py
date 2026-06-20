#!/usr/bin/env python3
"""Pipeline FarmTech Cap 1."""

from __future__ import annotations

import argparse
import subprocess
import sys

from paths import DASHBOARD_APP, DEFAULT_CSV, TASK_ROOT


def _run(rel: str, label: str, *, optional: bool = False) -> bool:
    path = TASK_ROOT / rel
    if not path.is_file():
        msg = f"[pipeline] {label} - ausente: {rel}"
        if optional:
            print(msg, flush=True)
            return False
        print(f"ERRO: {msg}", file=sys.stderr, flush=True)
        sys.exit(1)
    print(f"\n[pipeline] {label}", flush=True)
    subprocess.run([sys.executable, str(path)], cwd=TASK_ROOT, check=True)
    return True


def run_pipeline(*, skip_generate: bool = False, skip_ingest: bool = False) -> None:
    print("=" * 60, flush=True)
    print("FarmTech Cap 1 - run_pipeline.py", flush=True)
    print("=" * 60, flush=True)

    if not skip_generate:
        _run("scripts/generate_dataset.py", "Etapa 1 - dataset sensores")
    elif not DEFAULT_CSV.is_file():
        print(f"ERRO: CSV ausente em {DEFAULT_CSV}", file=sys.stderr, flush=True)
        sys.exit(1)

    if not skip_ingest:
        _run("scripts/ingest_iot.py", "Etapa 2 - ingestao SQLite")

    _run("ml/train_regression.py", "Etapa 3 - regressao + metricas")

    print("\n[pipeline] Concluido.", flush=True)
    if DASHBOARD_APP.is_file():
        print(f"  Dashboard: cd {TASK_ROOT.name} && streamlit run dashboard/app.py", flush=True)
    print("  Gates: python scripts/harness_check.py", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline Cap 1 Fase 4")
    parser.add_argument("--skip-generate", action="store_true")
    parser.add_argument("--skip-ingest", action="store_true")
    args = parser.parse_args()
    run_pipeline(skip_generate=args.skip_generate, skip_ingest=args.skip_ingest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
