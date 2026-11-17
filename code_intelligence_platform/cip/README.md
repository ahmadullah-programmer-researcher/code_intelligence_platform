# Code Intelligence Platform (CIP)

An original, extensible code-intelligence workbench. The initial release scans Python projects, reports a small set of security-relevant patterns, extracts basic code metrics, builds an import dependency graph, detects dependency cycles, and caches file analysis by SHA-256 content fingerprint.

## Design inspiration and boundaries

CIP is an independent educational implementation. It does not contain copied Meta source code and is not affiliated with Meta.

- **Pyrefly:** module-oriented analysis, explicit phases, incremental checking. CIP currently uses Python's standard AST and file-level content caching; it is not a replacement type checker.
- **Buck2:** declared dependency graphs and deterministic build concepts. CIP currently extracts Python imports; it is not a hermetic build system.
- **Infer:** static-analysis findings with stable rule identifiers and source locations. CIP's four rules are deliberately small syntactic checks, not Infer's symbolic execution or interprocedural analysis.
- **RocksDB:** storage-engine design trade-offs informed the decision to isolate persistence behind a cache interface. CIP currently uses SQLite, not an LSM-tree engine.

## Architecture

```text
Browser UI / CLI
       |
       v
FastAPI + orchestration engine
       |
       +--> File discovery --> Python AST analyzer --> findings + metrics
       |                              |
       |                              +--> import extraction --> dependency graph --> Tarjan SCC
       |
       +--> SHA-256 fingerprint --> SQLite result cache
```

## Requirements

- Python 3.10+
- pip

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, or run `.venv\Scripts\python.exe` directly.

## Run the web application

```powershell
uvicorn cip.main:app --reload
```

Open http://127.0.0.1:8000. Enter an absolute path to a project directory accessible to the server. For the included example, use the absolute path to `examples/sample_project`.

## Run from the command line

```powershell
cip .\examples\sample_project --output report.json
```

Or without installing the console script:

```powershell
python -m cip.cli .\examples\sample_project
```

## Run tests

```powershell
pytest -q
```

## Current analysis rules

| Rule | Description | Severity |
|---|---|---|
| CIP001 | `eval` or `exec` call | High |
| CIP002 | `subprocess`-style call with `shell=True` | High |
| CIP003 | Credential-like variable assigned a sufficiently long string literal | Medium |
| CIP004 | `pickle.load(s)` or `pickle.loads(...)` | High |

These are heuristic signals, not proof of exploitability. False positives and false negatives are expected. Do not use this prototype as the sole security control for production software.

## API

- `GET /api/health`
- `POST /api/analyze` with JSON body `{"path":"/absolute/project/path"}`

## Limitations

- Python source files only; no C++, Rust, JavaScript, or TypeScript frontend yet.
- Import resolution is intentionally simple and does not model packages, namespace packages, conditional imports, or dynamic imports fully.
- The analyzer does not perform taint analysis, symbolic execution, type inference, or interprocedural data-flow analysis.
- Cache invalidation is content-based per file. The report includes current relative paths, but does not yet implement dependency-aware invalidation.
- The API analyzes directories visible to the host process. Do not expose this service to untrusted networks: arbitrary local paths are accepted.
- Tarjan's implementation is recursive and may hit Python's recursion limit on very deep graphs.

## Security notes

Run locally and only analyze trusted directories. Before exposing the API, add authentication, path allowlists, request limits, process isolation, resource quotas, and audit logging. The sample project intentionally contains unsafe patterns for testing.

## Roadmap

1. Add a typed intermediate representation and explicit analysis passes.
2. Add interprocedural data-flow and taint analysis with explainable paths.
3. Add C/C++ parsing through Clang tooling and Rust support through compiler metadata.
4. Add a language-server protocol (LSP) service and editor integration.
5. Add a build graph with declared inputs, hermetic execution, and remote cache support.
6. Benchmark precision, recall, throughput, memory use, and incremental latency against labeled datasets and established tools.
7. Evaluate storage backends independently before considering an LSM-based implementation.

## License

MIT. See `LICENSE`.
