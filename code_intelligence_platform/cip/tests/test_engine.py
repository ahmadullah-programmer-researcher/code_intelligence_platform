from pathlib import Path
from cip.engine import analyze_project

def test_scan_and_cache(tmp_path: Path):
    (tmp_path / "main.py").write_text("def hello():\n    return 'hi'\n")
    first = analyze_project(str(tmp_path))
    second = analyze_project(str(tmp_path))
    assert first["files_scanned"] == 1
    assert second["cache_hits"] == 1
