# Reproduzir localmente — Cap 1 Fase 4

## Pré-requisitos

- Python 3.10 ou superior
- Git
- Navegador atualizado

## Passo a passo no Linux/macOS

```bash
git clone https://github.com/vinialveslopesanjos/fiap-fase4-cap1-farmtech.git
cd fiap-fase4-cap1-farmtech
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/run_pipeline.py
python scripts/harness_check.py
streamlit run dashboard/app.py
```

## Passo a passo no Windows PowerShell

```powershell
git clone https://github.com/vinialveslopesanjos/fiap-fase4-cap1-farmtech.git
cd fiap-fase4-cap1-farmtech
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts/run_pipeline.py
python scripts/harness_check.py
streamlit run dashboard/app.py
```

Acesse no navegador:

```text
http://localhost:8501
```

## O que validar na UI

1. Aba **Previsão** — botão “Prever rendimento” retorna t/ha e recomendação de manejo.
2. Aba **Correlação** — matriz de correlação e gráfico umidade vs rendimento.
3. Métricas MAE, RMSE e R² no topo.

## Gates automáticos

```bash
python scripts/harness_check.py
```

## Problemas comuns

| Sintoma | Solução |
|---------|---------|
| Modelo não encontrado | Rode `python scripts/run_pipeline.py` |
| SQLite vazio | Rode `python scripts/ingest_iot.py` |
| Streamlit não abre | Confira se o terminal mostra `Local URL: http://localhost:8501` |
| Erro no PowerShell ao ativar venv | Rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e tente ativar novamente |
