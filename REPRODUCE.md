# Reproduzir localmente - Cap 1 Fase 4

## Pre-requisitos

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
python scripts/generate_video_notebook.py
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
python scripts/generate_video_notebook.py
python scripts/harness_check.py
streamlit run dashboard/app.py
```

Acesse no navegador:

```text
http://localhost:8501
```

## O que validar na UI

1. Aba **Previsao**: o botao "Prever manejo" retorna rendimento, irrigacao, fertilizacao e recomendacao.
2. Aba **Correlacao**: matriz de correlacao, grafico umidade x rendimento e metricas por alvo.
3. Aba **Tendencias**: graficos de produtividade, irrigacao e fertilizacao.
4. Aba **Dados**: amostra das leituras simuladas.
5. Arquivo `entrega/farmtech_analise_video.html`: graficos essenciais para apoio do video.

## Gate automatico

```bash
python scripts/harness_check.py
```

## Problemas comuns

| Sintoma | Solucao |
|---------|---------|
| Modelo nao encontrado | Rode `python scripts/run_pipeline.py` |
| SQLite vazio | Rode `python scripts/ingest_iot.py` |
| Streamlit nao abre | Confira se o terminal mostra `Local URL: http://localhost:8501` |
| Erro no PowerShell ao ativar venv | Rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e tente ativar novamente |
