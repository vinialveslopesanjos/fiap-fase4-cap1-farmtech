"""Caminhos do projeto FarmTech Cap 1 (task11_fase4_cap1)."""

from pathlib import Path

TASK_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = TASK_ROOT / "scripts"
DATA_DIR = TASK_ROOT / "data"
SQL_DIR = TASK_ROOT / "sql"
DOCS_DIR = TASK_ROOT / "docs"
ML_DIR = TASK_ROOT / "ml"
MODELS_DIR = TASK_ROOT / "models"
DASHBOARD_DIR = TASK_ROOT / "dashboard"
FIGURES_DIR = TASK_ROOT / "figures"
PRINTS_DIR = TASK_ROOT / "prints"
ENTREGA_DIR = TASK_ROOT / "entrega"

DEFAULT_CSV = DATA_DIR / "leituras_sensores.csv"
DEFAULT_DB = DATA_DIR / "farmtech_iot.db"
SCHEMA_SQL = SQL_DIR / "01_schema.sql"
ML_TRAIN = ML_DIR / "train_regression.py"
ML_PREDICT = ML_DIR / "predict.py"
DASHBOARD_APP = DASHBOARD_DIR / "app.py"
METRICS_JSON = MODELS_DIR / "regression_metrics.json"
MODEL_PATH = MODELS_DIR / "regression_model.joblib"

MIN_DATASET_ROWS = 200
