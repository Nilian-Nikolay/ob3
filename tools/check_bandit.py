#!/usr/bin/env python3
"""
tools/check_bandit.py

Простой анализатор bandit JSON-отчёта.
Выход 0 — если нет уязвимостей с severity HIGH.
Выход 1 — если есть хотя бы одна HIGH.
"""

import sys
import json

def main(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: cannot read {path}: {e}")
        return 2

    issues = data.get('results', [])
    high = [i for i in issues if i.get('issue_severity','').upper() == 'HIGH']

    print(f"Bandit total issues: {len(issues)}, HIGH: {len(high)}")
    if len(high):
        print("High severity issues found:")
        for h in high:
            print(f"- {h.get('test_id')} | {h.get('issue_text')} (file: {h.get('filename')}:{h.get('line_number')})")
        sys.exit(1)
    else:
        print("No HIGH severity issues found. OK.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_bandit.py <bandit-json-file>")
        sys.exit(2)
    main(sys.argv[1])
