import sys
import json

BANDIT_FILE = sys.argv[1]

with open(BANDIT_FILE) as f:
    data = json.load(f)

failed = False
for issue in data.get("results", []):
    if issue.get("issue_severity") == "HIGH":
        print(f"❌ Найдена критическая уязвимость: {issue.get('test_id')} - {issue.get('issue_text')}")
        failed = True

if failed:
    sys.exit(1)
else:
    print("✅ Критических уязвимостей не найдено")
    sys.exit(0)
