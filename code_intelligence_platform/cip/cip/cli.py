import argparse, json
from pathlib import Path
from .engine import analyze_project

def main():
    parser = argparse.ArgumentParser(prog="cip", description="Analyze a Python project")
    parser.add_argument("path", help="Project directory")
    parser.add_argument("--output", "-o", help="Write JSON report to this file")
    args = parser.parse_args()
    report = analyze_project(args.path)
    rendered = json.dumps(report, indent=2)
    if args.output: Path(args.output).write_text(rendered, encoding="utf-8")
    else: print(rendered)

if __name__ == "__main__": main()
