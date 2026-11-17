from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .engine import analyze_project

app = FastAPI(title="Code Intelligence Platform", version="0.1.0", description="Static analysis, dependency inspection and incremental project scanning.")
class AnalyzeRequest(BaseModel):
    path: str = Field(min_length=1, description="Absolute or relative path to a local project directory")

@app.get("/api/health")
def health(): return {"status": "ok", "service": "cip"}

@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    try: return analyze_project(request.path)
    except ValueError as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc
