from fastapi.staticfiles import StaticFiles
from .api import app
from pathlib import Path

WEB = Path(__file__).resolve().parent.parent / "web"
app.mount("/", StaticFiles(directory=WEB, html=True), name="web")
