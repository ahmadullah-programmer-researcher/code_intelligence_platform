"""Project scanner and orchestration layer."""
import hashlib
from pathlib import Path
from .analyzer import analyze_python
from .cache import ResultCache
from .graph import find_cycles

IGNORED = {".git", ".venv", "venv", "node_modules", "__pycache__", ".cip"}

def analyze_project(project: str, cache_path: str | None = None) -> dict:
    root = Path(project).expanduser().resolve()
    if not root.exists() or not root.is_dir(): raise ValueError(f"Project directory does not exist: {root}")
    cache = ResultCache(Path(cache_path) if cache_path else root / ".cip" / "cache.sqlite3")
    reports, graph, cache_hits = [], {}, 0
    try:
        files = sorted(p for p in root.rglob("*.py") if not any(part in IGNORED for part in p.parts))
        for path in files:
            raw = path.read_bytes(); digest = hashlib.sha256(raw).hexdigest()
            cached = cache.get(digest)
            if cached is not None:
                report = cached; cache_hits += 1
                report["path"] = str(path.relative_to(root))
            else:
                report = analyze_python(path, root).to_dict(); cache.put(digest, report)
            reports.append(report)
            module = path.relative_to(root).with_suffix("").as_posix().replace("/", ".")
            graph[module] = []
            for imported in report["imports"]:
                candidates = [m for m in files if m.stem == imported]
                if candidates: graph[module].append(candidates[0].relative_to(root).with_suffix("").as_posix().replace("/", "."))
        findings = [f for r in reports for f in r["findings"]]
        return {"project": root.name, "root": str(root), "files_scanned": len(reports), "cache_hits": cache_hits,
                "metrics": {"lines": sum(r["lines"] for r in reports), "functions": sum(r["functions"] for r in reports), "classes": sum(r["classes"] for r in reports)},
                "finding_count": len(findings), "findings": findings, "files": reports, "dependency_graph": graph, "dependency_cycles": find_cycles(graph)}
    finally: cache.close()
