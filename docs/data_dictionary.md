# Dicionário de Dados — Cap 1 FarmTech

Fonte: `data/leituras_sensores.csv`

| Campo | Descrição |
|------|-----------|
| `data_hora` | Data e hora da leitura simulada do sensor |
| `talhao_id` | Identificador do talhão monitorado |
| `umidade_solo` | Umidade do solo em percentual |
| `ph_solo` | pH medido no solo |
| `nitrogenio` | Indicador sintético de nitrogênio |
| `fosforo` | Indicador sintético de fósforo |
| `potassio` | Indicador sintético de potássio |
| `temperatura_c` | Temperatura em graus Celsius |
| `rendimento_t_ha` | Rendimento agrícola estimado em toneladas por hectare |
| `irrigacao_sugerida_l` | Volume sugerido de irrigação em litros |

O dataset é gerado pelo script `scripts/generate_dataset.py` e depois ingerido em SQLite por `scripts/ingest_iot.py`.
