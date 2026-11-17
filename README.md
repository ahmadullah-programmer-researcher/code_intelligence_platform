# Code Intelligence Platform (CIP)

**An independent code intelligence platform for Python static analysis, security detection, dependency graph analysis, and incremental code inspection.**

CIP is an open-source software engineering project designed to help developers understand their codebases, identify potentially unsafe coding patterns, inspect module dependencies, and improve software reliability.

The project combines Python Abstract Syntax Tree (AST) analysis, graph algorithms, content-based caching, and a REST API into a unified developer tool.

## Project Overview

Code Intelligence Platform explores the intersection of:

- Static program analysis
- Software security
- Programming language engineering
- Graph theory and algorithms
- Incremental computation
- Developer tooling

The initial release focuses on Python projects, with an architecture intended to support additional programming languages and more advanced analysis techniques.

## Features

### 1. Python Static Analysis

Uses Python's built-in Abstract Syntax Tree (AST) to inspect source files without executing the analyzed code.

Current capabilities:
- Python source parsing
- Function and class extraction
- Basic code metrics
- Syntax error reporting
- Security-related pattern detection

### 2. Security Analysis

CIP implements four initial heuristic security rules.

| Rule | Description | Severity |
|---|---|---|
| CIP001 | Detects potentially unsafe `eval()` and `exec()` calls | High |
| CIP002 | Detects subprocess execution with `shell=True` | High |
| CIP003 | Identifies potentially hardcoded credentials | Medium |
| CIP004 | Detects potentially unsafe pickle deserialization | High |

These findings are indicators for manual investigation, not proof that a vulnerability is exploitable.

### 3. Dependency Graph Analysis

CIP extracts Python import relationships and represents them as a directed dependency graph.

The graph engine uses **Tarjan's Strongly Connected Components (SCC) algorithm** to identify circular dependencies.

Applications include:
- Dependency inspection
- Circular import detection
- Module relationship analysis
- Graph-based software architecture exploration

### 4. Incremental Analysis

CIP calculates SHA-256 fingerprints for source files.

When a file has not changed, its cached analysis result can be reused instead of performing the same analysis again.

This reduces unnecessary repeated processing.

### 5. Persistent Caching

SQLite provides persistent storage for cached analysis results.

The cache is designed to separate analysis logic from result persistence.

### 6. Web Dashboard and REST API

The application includes:
- FastAPI backend
- Browser-based dashboard
- Project analysis endpoint
- Health-check endpoint
- JSON analysis reporting

### 7. Command-Line Interface

CIP can also be executed directly from a terminal, allowing developers to integrate analysis into their local development workflows.

## Architecture

```text
                  Developer
                      |
             +--------+--------+
             |                 |
          Web UI              CLI
             |                 |
             +--------+--------+
                      |
                 FastAPI
                      |
               Analysis Engine
                      |
       +--------------+--------------+
       |              |              |
   File Scanner   AST Analyzer   SHA-256
       |              |              |
       |         +----+----+         |
       |         |         |         |
       |      Security   Metrics     |
       |       Rules                 |
       |                             |
       +------ Import Extraction ----+
                      |
                Dependency Graph
                      |
                 Tarjan SCC
                      |
               SQLite Cache
                      |
                JSON Reports
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| FastAPI | REST API |
| Python AST | Source code analysis |
| SQLite | Persistent result caching |
| SHA-256 | Content fingerprinting |
| Tarjan's Algorithm | Strongly connected components |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Frontend interaction |
| pytest | Automated testing |

## Repository Structure

```text
code_intelligence_platform/
│
├── cip/
│   ├── __init__.py
│   ├── main.py
│   ├── api.py
│   ├── analyzer.py
│   ├── engine.py
│   ├── graph.py
│   ├── cache.py
│   ├── models.py
│   └── cli.py
│
├── web/
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── tests/
│   ├── test_analyzer.py
│   ├── test_engine.py
│   └── test_graph.py
│
├── examples/
│   └── sample_project/
│       ├── app.py
│       └── unsafe.py
│
├── example-report.json
├── pyproject.toml
├── LICENSE
└── README.md
```

## Installation

### Requirements

- Python 3.10 or newer
- pip
- Windows, Linux, or macOS

### 1. Clone the repository

```bash
git clone https://github.com/ahmadullah-programmer-researcher/code_intelligence_platform.git
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Enter the project directory

```bash
cd code_intelligence_platform
```

### 3. Create a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn cip.main:app --reload
```

Open the dashboard:

```text
http://127.0.0.1:8000
```

Enter the absolute path of a Python project directory and start the analysis.

The included sample project can be used to explore the initial security detection rules.

## Command-Line Usage

Analyze the included example:

```bash
cip ./examples/sample_project
```

Save the analysis report:

```bash
cip ./examples/sample_project --output report.json
```

Alternatively, execute the CLI as a Python module:

```bash
python -m cip.cli ./examples/sample_project
```

## REST API

The initial API exposes the following endpoints.

### Health Check

```http
GET /api/health
```

### Analyze a Project

```http
POST /api/analyze
Content-Type: application/json
```

Example request:

```json
{
  "path": "/absolute/path/to/your/project"
}
```

The endpoint returns the project's analysis results as JSON.

## Running Tests

Run the automated test suite:

```bash
pytest -q
```

The tests cover the implemented analysis, dependency graph, and engine functionality.

## Design Inspiration

CIP is independently developed and takes architectural inspiration from several open-source engineering projects.

| Project | Engineering inspiration |
|---|---|
| [Meta Infer](https://github.com/facebook/infer) | Static analysis and structured findings |
| [Meta Buck2](https://github.com/facebook/buck2) | Dependency graphs and incremental computation |
| [Meta Pyrefly](https://github.com/facebook/pyrefly) | Python analysis architecture |
| [Meta RocksDB](https://github.com/facebook/rocksdb) | Storage-engine design considerations |

**Important:** CIP does not contain copied implementations from these repositories. It is an independent educational and research-oriented implementation. It is not affiliated with or endorsed by Meta.

## Current Limitations

The current release is an early-stage research prototype.

Known limitations include:

- Python-only source analysis.
- Limited heuristic security detection.
- No complete type inference engine.
- No interprocedural data-flow analysis.
- No symbolic execution.
- Simplified Python import resolution.
- No distributed analysis engine.
- No C++, Rust, JavaScript, or TypeScript support yet.
- No production-grade authentication or API access controls.

Security findings may include false positives and false negatives.

CIP should not be used as the sole security control for production applications.

## Development Roadmap

The following capabilities are planned, not implemented in the initial release.

### Version 0.2 — Advanced Analysis Engine
- Typed intermediate representation
- More sophisticated Python type analysis
- Control-flow graph construction
- Data-flow analysis
- Improved vulnerability detection

### Version 0.3 — Multi-Language Support
- C and C++ analysis through Clang tooling
- Rust source analysis
- JavaScript and TypeScript support
- Shared intermediate representation

### Version 0.4 — Advanced Dependency Engine
- Dependency-aware invalidation
- Parallel file analysis
- Improved incremental computation
- Large repository support

### Version 0.5 — Developer Integration
- Language Server Protocol (LSP)
- Editor integration
- Git integration
- Continuous integration workflows

### Version 1.0 — Research and Production Evaluation
- Performance benchmarking
- Precision and recall evaluation
- Security hardening
- Scalability evaluation
- Reproducible research experiments

## Research Directions

CIP provides a foundation for exploring several computer science research areas:

1. Incremental static program analysis.
2. Scalable dependency graph algorithms.
3. Interprocedural vulnerability detection.
4. Explainable software security analysis.
5. Multi-language intermediate representations.
6. Efficient analysis of large software repositories.
7. Correctness and reliability of automated code analysis.

Potential future research will require comparison against established tools and reproducible evaluation datasets.

## Contributing

Contributions and technical discussions are welcome.

Possible contribution areas include:

- New Python security rules
- AST analysis improvements
- Graph algorithm optimization
- Performance testing
- Documentation
- Automated test coverage
- Additional language support

For substantial changes, please open an issue to discuss the proposed implementation before submitting a pull request.

## Security

Please do not expose the development server to untrusted networks.

The initial API accepts filesystem paths from requests. Before deployment, the application needs authentication, strict path allowlists, request limits, process isolation, resource quotas, and audit logging.

If you discover a security issue in CIP, please report it privately to the repository maintainers rather than publishing an exploit.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Independent Software Engineering Project**

Research interests:
- Computer Science
- Programming Languages
- Systems Programming
- Software Security
- Compiler Engineering
- Static Program Analysis

---

**Code Intelligence Platform (CIP)**

*Building tools for deeper code understanding, safer software, and more reliable engineering.*
