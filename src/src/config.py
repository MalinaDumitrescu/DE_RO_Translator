from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = ROOT / "models"
DATA_DIR = ROOT / "data"

VOSK_MODEL_DIR = MODELS_DIR / "vosk-model-small-de"
SAMPLE_RATE = 16_000
BLOCK_SECONDS = 4

DB_PATH = DATA_DIR / "fraze_de_ro.sqlite"
EXCEL_PATH = DATA_DIR / "fraze_de_ro.xlsx"

DATA_DIR.mkdir(parents=True, exist_ok=True)