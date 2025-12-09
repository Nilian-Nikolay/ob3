import json
import sys

report_path = sys.argv[1]

with open(report_path, "r") as f:
    data = json.load(f)

issues = data.get("results", [])
high_issues = [i for i in issues if i.get("issue_severity") == "HIGH"]

if high_issues:
    print("❌ Найдены HIGH уязвимости!")
    for issue in high_issues:
        print(f"{issue['filename']}:{issue['line_number']} {issue['issue_text']}")
    sys.exit(1)
else:
    print("✅ HIGH уязвимости не найдены, можно мержить.")
    sys.exit(0)
