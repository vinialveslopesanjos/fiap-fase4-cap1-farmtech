#!/usr/bin/env python3
"""Gera CSV simulado de sensores agrícolas para regressão (Cap 1 Fase 4)."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from paths import DEFAULT_CSV, MIN_DATASET_ROWS, TASK_ROOT


def generate_dataset(rows: int = 500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    umidade = rng.uniform(18, 85, rows)
    ph = rng.uniform(4.5, 8.0, rows)
    nitrogenio = rng.uniform(10, 120, rows)
    fosforo = rng.uniform(5, 80, rows)
    potassio = rng.uniform(20, 200, rows)
    temperatura = rng.uniform(15, 38, rows)
    # Rendimento sintético com relação interpretável
    rendimento = (
        2.5
        + 0.04 * umidade
        + 0.35 * ph
        + 0.008 * nitrogenio
        + 0.006 * potassio
        - 0.02 * np.maximum(0, temperatura - 32)
        + rng.normal(0, 0.25, rows)
    )
    irrigacao_litros = np.clip(800 - 6 * umidade + rng.normal(0, 40, rows), 50, 1200)

    return pd.DataFrame(
        {
            "data_hora": pd.date_range("2026-01-01", periods=rows, freq="h"),
            "talhao_id": rng.integers(1, 6, rows),
            "umidade_solo": np.round(umidade, 2),
            "ph_solo": np.round(ph, 2),
            "nitrogenio": np.round(nitrogenio, 1),
            "fosforo": np.round(fosforo, 1),
            "potassio": np.round(potassio, 1),
            "temperatura_c": np.round(temperatura, 1),
            "rendimento_t_ha": np.round(rendimento, 2),
            "irrigacao_sugerida_l": np.round(irrigacao_litros, 0),
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Gerar leituras_sensores.csv")
    parser.add_argument("--rows", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()

    if args.rows < MIN_DATASET_ROWS:
        raise SystemExit(f"Mínimo {MIN_DATASET_ROWS} linhas (enunciado pede volume útil).")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df = generate_dataset(rows=args.rows, seed=args.seed)
    df.to_csv(args.output, index=False)
    print(f"[ok] {len(df)} linhas → {args.output.relative_to(TASK_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
