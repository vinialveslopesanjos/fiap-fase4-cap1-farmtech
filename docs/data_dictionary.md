# Dicionario de Dados - Cap 1 FarmTech

Fonte: `data/leituras_sensores.csv`

| Campo | Descricao |
|------|-----------|
| `data_hora` | Data e hora da leitura simulada do sensor |
| `talhao_id` | Identificador do talhao monitorado |
| `umidade_solo` | Umidade do solo em percentual |
| `ph_solo` | pH medido no solo |
| `nitrogenio` | Indicador sintetico de nitrogenio |
| `fosforo` | Indicador sintetico de fosforo |
| `potassio` | Indicador sintetico de potassio |
| `temperatura_c` | Temperatura em graus Celsius |
| `rendimento_t_ha` | Rendimento agricola estimado em toneladas por hectare |
| `irrigacao_sugerida_l` | Volume sugerido de irrigacao em litros |
| `fertilizacao_sugerida_kg_ha` | Necessidade estimada de fertilizacao em kg/ha |

O dataset e gerado pelo script `scripts/generate_dataset.py` e depois ingerido em SQLite por `scripts/ingest_iot.py`.
