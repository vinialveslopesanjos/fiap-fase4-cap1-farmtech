# Dicionário de dados — Cap 1 FarmTech

> **Responsável:** Humberto · Fonte: `data/leituras_sensores.csv`

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `data_hora` | datetime | Timestamp da leitura do sensor | 2026-01-01 00:00:00 |
| `talhao_id` | int | Identificador do talhão (1–5) | 3 |
| `umidade_solo` | float | Umidade do solo (%) | 42.5 |
| `ph_solo` | float | pH do solo | 6.2 |
| `nitrogenio` | float | NPK — nitrogênio | 55.0 |
| `fosforo` | float | NPK — fósforo | 30.0 |
| `potassio` | float | NPK — potássio | 120.0 |
| `temperatura_c` | float | Temperatura ambiente (°C) | 28.0 |
| `rendimento_t_ha` | float | Rendimento observado (t/ha) — alvo regressão | 4.8 |
| `irrigacao_sugerida_l` | float | Volume sugerido de irrigação (L) | 450 |

## Tabela SQLite

`leituras_sensores` — espelha o CSV após `python scripts/ingest_iot.py`.
