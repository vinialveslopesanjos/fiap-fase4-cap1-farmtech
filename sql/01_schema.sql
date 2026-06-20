-- FarmTech Cap 1 — schema IoT
CREATE TABLE IF NOT EXISTS leituras_sensores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT NOT NULL,
    talhao_id INTEGER NOT NULL,
    umidade_solo REAL NOT NULL,
    ph_solo REAL NOT NULL,
    nitrogenio REAL,
    fosforo REAL,
    potassio REAL,
    temperatura_c REAL,
    rendimento_t_ha REAL,
    irrigacao_sugerida_l REAL
);

CREATE INDEX IF NOT EXISTS idx_leituras_talhao ON leituras_sensores(talhao_id);
CREATE INDEX IF NOT EXISTS idx_leituras_data ON leituras_sensores(data_hora);
