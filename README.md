# FarmTech Cap 1 — Memorizando e Aprendendo (Fase 4)

**Turma 1TIAOA · Grupo 36** · Prazo **19/06/2026 23h59**  
**Portal:** [assign 614328](https://on.fiap.com.br/mod/assign/view.php?id=614328)

| Integrante | RM | Branch
|------------|-----|--------|
| Vinicius Anjos | 572814 | `f4-cap1-vinicius-integracao`

---

## Setup

```bash
cd tasks/task11_fase4_cap1
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Comandos por papel

### Todos — validar ambiente

```bash
python scripts/run_pipeline.py      # dataset → SQLite → modelo
python scripts/harness_check.py     # gates G1–G8
streamlit run dashboard/app.py      # http://localhost:8501
```

### Vini (`f4-cap1-higor-ml`)

```bash
python scripts/generate_dataset.py
python ml/train_regression.py
python scripts/harness_check.py --role Vini
```

Editar: `ml/`, `scripts/run_pipeline.py`, `dashboard/app.py` (trunk)

### Vini (`f4-cap1-igor-dash`)

```bash
# Não precisa rodar pipeline no PC leve — puxar main após Higor
python scripts/harness_check.py --role Vini
streamlit run dashboard/app.py   # se a máquina aguentar; senão só figures/
```

Editar: `dashboard/components/`, `figures/`, `prints/`

### Humberto (`f4-cap1-humberto-dados`)

```bash
python scripts/ingest_iot.py
python scripts/harness_check.py --role Vini
```

Editar: `sql/`, `scripts/ingest_iot.py` — **sem** vídeo/portal (Vini)

---

## Estrutura

```
task11_fase4_cap1/
├── README.md
├── REPRODUCE.md
├── requirements.txt
├── scripts/          # pipeline + harness
├── ml/               # train + predict
├── dashboard/        # Streamlit
├── data/             # CSV + SQLite (gerados)
├── models/           # joblib + metrics.json
├── sql/
├── figures/          # Vini — PNGs para vídeo
├── prints/
└── entrega/
```

---

### Vini — vídeo + portal

- Gravar vídeo → `link_video.txt`
- Submeter assign 614328 — ver `entrega/CHECKLIST_PORTAL.md`

Enunciado: `docs/validation/captures/fases/fase4/tasks/task01_cap_1_.../`
