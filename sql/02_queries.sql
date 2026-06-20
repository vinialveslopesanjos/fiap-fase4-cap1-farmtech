-- FarmTech Cap 1 — 5 queries analíticas
-- Rodar após: python scripts/ingest_iot.py

-- Q1: Contagem de leituras por talhão
SELECT talhao_id, COUNT(*) AS total_leituras
FROM leituras_sensores
GROUP BY talhao_id
ORDER BY talhao_id;

-- Q2: Média de umidade e pH por talhão
SELECT talhao_id,
       ROUND(AVG(umidade_solo), 2) AS media_umidade,
       ROUND(AVG(ph_solo), 2) AS media_ph
FROM leituras_sensores
GROUP BY talhao_id;

-- Q3: Alertas de umidade baixa (< 35%)
SELECT data_hora, talhao_id, umidade_solo, ph_solo
FROM leituras_sensores
WHERE umidade_solo < 35
ORDER BY data_hora DESC
LIMIT 20;

-- Q4: Top 10 maiores rendimentos registrados
SELECT data_hora, talhao_id, rendimento_t_ha, umidade_solo, nitrogenio
FROM leituras_sensores
ORDER BY rendimento_t_ha DESC
LIMIT 10;

-- Q5: Correlação simplificada — média diária de rendimento (SQLite)
SELECT DATE(data_hora) AS dia,
       ROUND(AVG(rendimento_t_ha), 2) AS rendimento_medio,
       ROUND(AVG(umidade_solo), 2) AS umidade_media
FROM leituras_sensores
GROUP BY DATE(data_hora)
ORDER BY dia
LIMIT 30;
