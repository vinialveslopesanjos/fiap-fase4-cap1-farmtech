# Reproduzir localmente — Cap 1 Fase 4

## Pré-requisitos

- Python 3.10+
- Git

## Passo a passo (≤ 5 min)

```bash
cd tasks/task11_fase4_cap1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/run_pipeline.py
streamlit run dashboard/app.py
```

## O que validar na UI

1. Aba **Previsão** — botão "Prever rendimento" retorna t/ha + ação de manejo
2. Aba **Correlação** — matriz e gráfico umidade vs rendimento
3. Métricas MAE / RMSE / R² no topo

## Gates automáticos

```bash
python scripts/harness_check.py
```

## Problemas comuns

| Sintoma | Solução |
|---------|---------|
| Modelo não encontrado | `python scripts/run_pipeline.py` |
| SQLite vazio | `python scripts/ingest_iot.py` |
| Streamlit lento | Igor gera `figures/` estáticos; Higor grava demo |
