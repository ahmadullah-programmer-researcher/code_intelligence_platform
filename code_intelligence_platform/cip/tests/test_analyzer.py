from pathlib import Path
from cip.analyzer import analyze_python

def test_security_rules(tmp_path: Path):
    source = 'import subprocess\nSECRET = "abcdef123"\neval("1+1")\nsubprocess.run("x", shell=True)\n'
    p = tmp_path / "sample.py"; p.write_text(source)
    report = analyze_python(p, tmp_path)
    assert {f.rule_id for f in report.findings} == {"CIP001", "CIP002", "CIP003"}

def test_syntax_error_report(tmp_path: Path):
    p = tmp_path / "bad.py"; p.write_text("def broken(:\n")
    assert analyze_python(p, tmp_path).parse_error
