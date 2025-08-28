from datetime import datetime
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from .config import DB_PATH, EXCEL_PATH

class Storage:
    def __init__(self, db_path: Path = DB_PATH, excel_path: Path = EXCEL_PATH):
        self.db_path = db_path
        self.excel_path = excel_path
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        self._init_schema()

    def _init_schema(self):
        with self.engine.begin() as conn:
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fraze (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                germana   TEXT NOT NULL,
                romana    TEXT NOT NULL,
                sursa     TEXT DEFAULT 'offline_vosk',
                confidence REAL
            );
            """))

    def save_phrase(self, germana: str, romana: str, sursa: str = "offline_vosk", confidence: float | None = None):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        df = pd.DataFrame([{
            "timestamp": ts, "germana": germana, "romana": romana,
            "sursa": sursa, "confidence": confidence
        }])
        df.to_sql("fraze", self.engine, if_exists="append", index=False)
        if self.excel_path.exists():
            old = pd.read_excel(self.excel_path)
            out = pd.concat([old, df], ignore_index=True)
        else:
            out = df
        out.to_excel(self.excel_path, index=False)
        return ts

    def list_last(self, limit=10):
        query = f"SELECT * FROM fraze ORDER BY id DESC LIMIT {limit}"
        return pd.read_sql(query, self.engine)
