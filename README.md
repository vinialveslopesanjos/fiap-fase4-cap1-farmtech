# FarmTech Cap 1 — Memorizando e Aprendendo (Fase 4)

**Turma 1TIAOA · Entrega individual** · Prazo **19/06/2026 23h59**  
**Aluno:** Vinicius Anjos · RM 572814  
**Portal:** [assign 614328](https://on.fiap.com.br/mod/assign/view.php?id=614328)

---

## Visão geral

Projeto individual desenvolvido para a Fase 4 da FIAP. A solução simula uma base de leituras agrícolas, grava os dados em SQLite, treina um modelo de regressão para prever rendimento e apresenta os resultados em um dashboard Streamlit.

O objetivo é demonstrar, em um fluxo reproduzível, como dados de sensores podem apoiar decisões de irrigação e manejo na FarmTech Solutions.

---

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

---

## Rodar pipeline e dashboard

```bash
python scripts/run_pipeline.py
python scripts/harness_check.py
streamlit run dashboard/app.py
```

Após o último comando, abrir no navegador:

```text
http://localhost:8501
```

---

## O que o projeto entrega

1. Geração de dataset sintético de sensores agrícolas.
2. Ingestão dos dados em banco SQLite.
3. Treinamento de modelo de regressão supervisionada.
4. Métricas do modelo em `models/regression_metrics.json`.
5. Dashboard Streamlit com previsão, análise de correlação, tendência de produtividade e indicadores.
6. Recomendação de irrigação, manejo e fertilização a partir dos inputs agrícolas.
7. Scripts de validação para checar os artefatos antes da entrega.

---

## Estrutura

```text
fiap-fase4-cap1-farmtech/
├── README.md
├── REPRODUCE.md
├── requirements.txt
├── scripts/          # pipeline, geração de dados, ingestão e validação
├── ml/               # treino e predição do modelo
├── dashboard/        # aplicação Streamlit
├── data/             # CSV e SQLite gerados pelo pipeline
├── models/           # modelo treinado e métricas
├── sql/              # schema e consultas SQL
├── figures/          # imagens auxiliares
├── prints/           # evidências visuais
└── entrega/          # checklist de entrega
```

---

## Roteiro sugerido para o vídeo

1. Mostrar rapidamente o repositório e explicar que é uma entrega individual.
2. Rodar `python scripts/run_pipeline.py` para gerar dados, SQLite e modelo.
3. Rodar `python scripts/harness_check.py` para validar os arquivos.
4. Abrir o dashboard com `streamlit run dashboard/app.py`.
5. Demonstrar a aba de previsão, alterando os inputs e clicando em “Prever rendimento”.
6. Mostrar os indicadores e gráficos de correlação.
7. Concluir explicando como o modelo apoia decisões de irrigação e manejo.

---

## Reprodução rápida

Também existe um passo a passo resumido em [`REPRODUCE.md`](REPRODUCE.md).
