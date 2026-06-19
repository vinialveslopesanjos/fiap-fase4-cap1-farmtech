# Roteiro de falas — Vídeo Cap 1 (≤ 5 min)

Objetivo do vídeo: demonstrar o Assistente Agrícola Inteligente da FarmTech, conectando dados de sensores, banco SQL, modelo de regressão e dashboard Streamlit.

| Tempo | Quem | Fala sugerida |
|-------|------|----------------|
| 0:00–0:30 | Abertura | "Este projeto implementa um assistente agrícola que usa leituras de sensores para prever rendimento em toneladas por hectare e sugerir ações de manejo." |
| 0:30–1:20 | Pipeline | "O fluxo começa com um dataset de 500 leituras de sensores. As variáveis usadas no modelo são umidade do solo, pH, nitrogênio, fósforo, potássio e temperatura." |
| 1:20–2:00 | Banco SQL | "As leituras são persistidas em SQLite. O projeto inclui schema e consultas SQL para apoiar análise operacional, como alertas de baixa umidade e resumo por cultura." |
| 2:00–2:50 | Modelo | "Treinamos um RandomForestRegressor com Scikit-learn. O resultado foi R² de 0.8727, MAE de 0.2527 e RMSE de 0.3242, indicando boa capacidade de previsão no dataset sintético." |
| 2:50–4:10 | Dashboard | "No Streamlit, o produtor consegue ver métricas do modelo, correlação entre variáveis e simular novos cenários. Ao clicar em Prever rendimento, o sistema retorna a previsão e uma recomendação de manejo." |
| 4:10–4:45 | Demonstração prática | "Aqui alteramos a umidade, pH e nutrientes. O assistente recalcula o rendimento previsto e sugere se a irrigação ou correção de manejo é necessária." |
| 4:45–5:00 | Encerramento | "A solução integra dados, aprendizado de máquina e visualização para apoiar decisões mais rápidas no campo." |

## Checklist de gravação

1. Rodar `python scripts/run_pipeline.py` antes de abrir o dashboard.
2. Abrir `streamlit run dashboard/app.py`.
3. Mostrar as métricas MAE, RMSE e R².
4. Mostrar a aba Correlação.
5. Na aba Previsão, alterar pelo menos 2 valores e clicar em **Prever rendimento**.
6. Após publicar o vídeo, colar o link em `link_video.txt` e no portal FIAP.
