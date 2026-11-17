"""Small SQLite content-addressed result cache."""
import json, sqlite3
from pathlib import Path

class ResultCache:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS results (digest TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        self.db.commit()

    def get(self, digest: str):
        row = self.db.execute("SELECT payload FROM results WHERE digest=?", (digest,)).fetchone()
        return json.loads(row[0]) if row else None

    def put(self, digest: str, payload: dict):
        self.db.execute("INSERT OR REPLACE INTO results(digest,payload) VALUES(?,?)", (digest, json.dumps(payload)))
        self.db.commit()

    def close(self): self.db.close()
