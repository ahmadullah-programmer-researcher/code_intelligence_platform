"""Python AST analyzer. Rules are intentionally transparent and deterministic."""
import ast
import hashlib
from pathlib import Path
from .models import Finding, FileReport

RULES = {
    "CIP001": "Use of eval/exec can execute untrusted code.",
    "CIP002": "Subprocess invoked with shell=True can enable command injection.",
    "CIP003": "Hard-coded credential-like value detected.",
    "CIP004": "Pickle deserialization can execute attacker-controlled payloads.",
}

class PythonAnalyzer(ast.NodeVisitor):
    def __init__(self, path: str):
        self.path = path
        self.findings: list[Finding] = []
        self.functions = 0
        self.classes = 0
        self.imports: list[str] = []

    def add(self, rule: str, node: ast.AST, message: str | None = None):
        self.findings.append(Finding(rule, "high" if rule in {"CIP001", "CIP002", "CIP004"} else "medium", message or RULES[rule], self.path, getattr(node, "lineno", 1), getattr(node, "col_offset", 0)))

    def visit_FunctionDef(self, node):
        self.functions += 1
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        self.classes += 1
        self.generic_visit(node)

    def visit_Import(self, node):
        self.imports.extend(alias.name.split('.')[0] for alias in node.names)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module.split('.')[0])
        self.generic_visit(node)

    def visit_Call(self, node):
        name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
        if name in {"eval", "exec"}:
            self.add("CIP001", node)
        if name in {"run", "Popen", "call"} and any(k.arg == "shell" and isinstance(k.value, ast.Constant) and k.value.value is True for k in node.keywords):
            self.add("CIP002", node)
        if name in {"loads", "load"} and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
            self.add("CIP004", node)
        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = [n.id.lower() for t in node.targets for n in ast.walk(t) if isinstance(n, ast.Name)]
        if any(any(word in t for word in ("password", "secret", "api_key", "token")) for t in targets) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str) and len(node.value.value) >= 6:
            self.add("CIP003", node)
        self.generic_visit(node)


def analyze_python(path: Path, root: Path) -> FileReport:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    rel = str(path.relative_to(root))
    source = raw.decode("utf-8", errors="replace")
    try:
        tree = ast.parse(source, filename=rel)
    except SyntaxError as exc:
        return FileReport(rel, "python", digest, len(source.splitlines()), 0, 0, [], [], f"{exc.msg} at line {exc.lineno}")
    visitor = PythonAnalyzer(rel)
    visitor.visit(tree)
    return FileReport(rel, "python", digest, len(source.splitlines()), visitor.functions, visitor.classes, visitor.findings, sorted(set(visitor.imports)))
