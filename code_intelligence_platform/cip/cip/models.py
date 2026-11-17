from dataclasses import asdict, dataclass
from typing import Any

@dataclass
class Finding:
    rule_id: str
    severity: str
    message: str
    path: str
    line: int
    column: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class FileReport:
    path: str
    language: str
    sha256: str
    lines: int
    functions: int
    classes: int
    findings: list[Finding]
    imports: list[str]
    parse_error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["findings"] = [f.to_dict() for f in self.findings]
        return result
