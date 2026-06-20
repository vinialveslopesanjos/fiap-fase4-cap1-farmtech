# FarmTech Cap 1 - Memorizando e Aprendendo com os Dados

**Turma 1TIAOA - Entrega individual**
**Aluno:** Vinicius Anjos - RM 572814
**Portal:** [assign 614328](https://on.fiap.com.br/mod/assign/view.php?id=614328)
video: https://youtu.be/M3qzcHphM50?is=4l_wPRIBSpeIQLiG
## Visao geral

Projeto desenvolvido para a Fase 4 da FIAP. A solucao simula leituras agricolas, grava os dados em SQLite, treina um pipeline de Machine Learning com Scikit-Learn e apresenta as previsoes em um dashboard Streamlit.

O assistente agricola inteligente usa regressao supervisionada para prever:

1. rendimento esperado em toneladas por hectare;
2. volume sugerido de irrigacao;
3. necessidade estimada de fertilizacao.

Com isso, o dashboard apoia decisoes de irrigacao, fertilizacao e manejo do solo para gestores agricolas.

## Setup local

```bash
git clone https://github.com/vinialveslopesanjos/fiap-fase4-cap1-farmtech.git
cd fiap-fase4-cap1-farmtech
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No Windows PowerShell:

```powershell
git clone https://github.com/vinialveslopesanjos/fiap-fase4-cap1-farmtech.git
cd fiap-fase4-cap1-farmtech
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Rodar pipeline e dashboard

```bash
python scripts/run_pipeline.py
python scripts/harness_check.py
streamlit run dashboard/app.py
```

Depois abra:

```text
http://localhost:8501
```

## O que o projeto entrega

1. Geracao de dataset sintetico de sensores agricolas.
2. Ingestao dos dados em banco SQLite.
3. Treinamento de modelo de regressao multi-saida.
4. Metricas MAE, MSE, RMSE e R2 por alvo em `models/regression_metrics.json`.
5. Dashboard Streamlit com previsoes, correlacoes, tendencias e recomendacoes de manejo.
6. Notebook e HTML de apoio para o video em `entrega/farmtech_analise_video.*`.
7. Scripts de validacao para checar os artefatos antes da entrega.

## Estrutura

```text
fiap-fase4-cap1-farmtech/
|-- README.md
|-- REPRODUCE.md
|-- requirements.txt
|-- scripts/      # pipeline, geracao de dados, ingestao, validacao e notebook
|-- ml/           # treino e predicao do modelo
|-- dashboard/    # aplicacao Streamlit
|-- data/         # CSV e SQLite gerados pelo pipeline
|-- models/       # modelo treinado e metricas
|-- sql/          # schema e consultas SQL
|-- figures/      # imagens auxiliares
`-- entrega/      # checklist, notebook e HTML de apoio
```

## Roteiro sugerido para o video

1. Mostrar o objetivo do projeto e o fluxo sensores -> SQLite -> modelo -> dashboard.
2. Rodar `python scripts/run_pipeline.py`.
3. Rodar `python scripts/harness_check.py`.
4. Abrir `streamlit run dashboard/app.py`.
5. Demonstrar a aba de previsao alterando umidade, pH e nutrientes.
6. Mostrar rendimento, irrigacao, fertilizacao e recomendacoes de manejo.
7. Mostrar correlacao, tendencias e metricas do modelo.
8. Opcional: abrir `entrega/farmtech_analise_video.html` para explicar os graficos em tela cheia.
